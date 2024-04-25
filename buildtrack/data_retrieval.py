import requests
import csv
import logging
from buildtrack.models import RegCon
import datetime

# Base URL for Zillow data
BASE_URL = "https://files.zillowstatic.com/research/public_csvs/"

# File names for different categories of data
NEW_CON_SALES_COUNT = "Metro_new_con_sales_count_raw_uc_sfrcondo_month.csv"
NEW_CON_MEDIAN_SALES_PRICE = "Metro_new_con_median_sale_price_uc_sfrcondo_month.csv"
NEW_CON_MEDIAN_SALES_PRICE_PERSQFT = "Metro_new_con_median_sale_price_per_sqft_uc_sfrcondo_month.csv"
NEW_CON_MEAN_SALES_PRICE = "Metro_new_con_mean_sale_price_uc_sfrcondo_month.csv"

# Function to construct the request URL based on timestamp and category
def setup_request(timestamp, category):
    if category == "Sales Count":
        sub_category = "new_con_sales_count_raw/"
        FILE_NAME = NEW_CON_SALES_COUNT
    elif category == "Median Sales Price":
        sub_category = "new_con_median_sale_price/"
        FILE_NAME = NEW_CON_MEDIAN_SALES_PRICE
    elif category == "Median Sales Price Persqft":
        sub_category = "new_con_median_sale_price_per_sqft/"
        FILE_NAME = NEW_CON_MEDIAN_SALES_PRICE_PERSQFT
    elif category == "Mean Sales Price":
        sub_category = "new_con_mean_sale_price/"
        FILE_NAME = NEW_CON_MEAN_SALES_PRICE
    else:
        raise ValueError("Unrecognized category!")
    timestamp_parameter = "?t=" + str(timestamp)
    return BASE_URL + sub_category + FILE_NAME + str(timestamp_parameter)

# Function to pull monthly count from the database
def pull_monthly_count(state, city):
    return RegCon.objects.filter(city=city, state=state).first()

# Function to update records in the database
def update_records(state, city, category, monthly_data_value):
    obj, created = RegCon.objects.get_or_create(city=city, state=state)
    if created:
        logging.info("New record! - Category: %s", category)
    else:
        logging.info("Already exists, updating! - Category: %s", category)
    setattr(obj, f"monthly_{category.lower().replace(' ', '_')}_blob", monthly_data_value)
    obj.save()

# Function to retrieve data from Zillow API
def retrieve_data(timestamp, category):
    final_url = setup_request(timestamp, category)
    try:
        req_data = requests.get(final_url)
        req_data.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to retrieve data: {e}")
        return

    csv_data = req_data.text.splitlines()
    csv_reader = csv.DictReader(csv_data)
    for row in csv_reader:
        state = row.get("StateName")
        city = row.get("RegionName").split(',')[0]
        trim_keys = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
        monthly_blob = {key: value for key, value in row.items() if key not in trim_keys}
        update_records(state, city, category, monthly_blob)

# Function to run the update process for all categories
def run_update():
    current_datetime = datetime.datetime.now()
    epoch_time = int(current_datetime.timestamp())
    categories = ["Sales Count", "Median Sales Price", "Median Sales Price Persqft", "Mean Sales Price"]
    for category in categories:
        retrieve_data(epoch_time, category)