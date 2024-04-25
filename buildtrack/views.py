from django.shortcuts import render
import json
from django.http import HttpResponse
from buildtrack.models import RegCon
from buildtrack.data_retrieval import *


# View function for the homepage
def homepage_view(request):
    return render(request, 'homepage.html', context={})  # Rendering the homepage.html template


# View function for handling AJAX requests and returning JSON response
def index(request):
    if request.method == 'POST':  # If the request method is POST
        selected_state = request.POST.get('state')  # Get selected state from POST data
        selected_city = request.POST.get('city')  # Get selected city from POST data
        selected_datapoint = request.POST.get('datapoint')  # Get selected datapoint from POST data

        # Retrieve the appropriate monthly data based on the selected datapoint
        if selected_datapoint == 'Sales Count':
            monthly_data_json = pull_monthly_count(selected_state, selected_city).monthly_sales_count_blob
        elif selected_datapoint == 'Median Sale Price':
            monthly_data_json = pull_monthly_count(selected_state, selected_city).monthly_median_sales_price_blob
        elif selected_datapoint == 'Median Sale Price Persqft':
            monthly_data_json = pull_monthly_count(selected_state,
                                                   selected_city).monthly_median_sales_price_persqft_blob
        elif selected_datapoint == 'Median Mean Sales Price':
            monthly_data_json = pull_monthly_count(selected_state, selected_city).monthly_mean_sales_price_blob
        else:
            # Handle the case when the selected datapoint is not recognized
            monthly_data_json = None

        # Extracting dates and counts from monthly data
        monthly_dates_labels = [str(date) for date in monthly_data_json.keys()]
        monthly_dates_count = [str(count) for count in monthly_data_json.values()]

        # Format data as JSON
        data = {
            'labels': monthly_dates_labels,
            'values': monthly_dates_count
        }
        return HttpResponse(json.dumps(data), content_type='application/json')  # Return JSON response
    else:
        # If request method is GET, prepare data for rendering records.html template
        records = RegCon.objects.all()  # Query all records from RegCon model
        cities_by_state = {}  # Initialize dictionary to store cities by state
        for record in records:
            state = record.state
            city = record.city
            if state in cities_by_state:
                cities_by_state[state].append(city)
            else:
                cities_by_state[state] = [city]
            cities_by_state[state] = sorted(cities_by_state[state])

        states = sorted(records.values_list('state', flat=True).distinct())  # Get sorted list of unique states
        cities_by_state_json = json.dumps(cities_by_state)  # Convert cities_by_state dictionary to JSON
        return render(request, 'records.html', {'states': states,
                                                'cities_by_state_json': cities_by_state_json})  # Render records.html template with data
