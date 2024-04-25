document.addEventListener('DOMContentLoaded', function () {
    // Function to handle state selection change
    document.getElementById('state').addEventListener('change', function () {
        var stateSelect = document.getElementById('state');
        var citySelect = document.getElementById('city');
        var selectedState = stateSelect.value;

        // Clear existing city options
        citySelect.innerHTML = '<option value="">-- Select City --</option>';
        // Populate city options based on selected state
        var cities = citiesByStateJson[selectedState];
        if (cities) {
            cities.forEach(function (city) {
                var option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        }
    });

    // Function to handle form submission
    document.getElementById('submit-btn').addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default form submission

        // Retrieve CSRF token
        var csrftoken = getCookie('csrftoken');

        // Retrieve selected state, city, and datapoint category
        var selectedState = document.getElementById('state').value;
        var selectedCity = document.getElementById('city').value;
        var selectedDatapoint = document.getElementById('datapoint').value;

        // Send AJAX request to retrieve data for Chart.js graph
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/buildtrack/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set CSRF token in request header
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                // Update Chart.js graph
                updateChart(data, selectedDatapoint);
            }
        };
        xhr.send('state=' + selectedState + '&city=' + selectedCity + '&datapoint=' + selectedDatapoint);
    });
});

// Function to retrieve CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches the expected CSRF token cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to update Chart.js graph
function updateChart(data, selectedDatapoint) {
    var canvas = document.getElementById('graph-container');
    var ctx = canvas.getContext('2d');

    // Check if a chart already exists
    if (window.myChart) {
        window.myChart.destroy(); // Destroy existing chart
    }

    // Determine chart title and y-axis label based on selected datapoint category
    var chartTitle =  selectedDatapoint;
    var yAxisLabel = '';
    switch (selectedDatapoint) {
        case 'Sales Count':
            yAxisLabel = 'New Construction Sales Count (All homes)';
            break;
        case 'Median Sale Price':
            yAxisLabel = 'Median Sale Price';
            break;
        case 'Median Sale Price Persqft':
            yAxisLabel = 'Median Sale Price Per Square Foot';
            break;
        case 'Median Mean Sales Price':
            yAxisLabel = 'Median Mean Sales Price';
            break;
        default:
            yAxisLabel = '';
            break;
    }

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: '',
                data: data.values,
                fill: true,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: chartTitle
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: ''
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: yAxisLabel
                    }
                }
            }
        }
    });
}
