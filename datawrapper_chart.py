import requests
import json
import pandas as pd

# Your Datawrapper API token
API_TOKEN = 'fLvzFOkhThQjJ6cePG5ZdzmamZ8T4ZHfuydRfIHfXXwNp3WPnCmNMzKP5Mkv0K1l'


# Define the headers for API requests
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

def create_chart(chart_title):
    # Create chart configuration
    chart_config = {
        "title": chart_title,
        "type": "d3-bars",  # Set chart type
        "metadata": {
            "visualize": {
                "x-axis": {
                    "title": "Categories"
                },
                "y-axis": {
                    "title": "Values"
                }
            }
        }
    }

    create_chart_url = "https://api.datawrapper.de/v3/charts"
    response = requests.post(create_chart_url, headers=headers, data=json.dumps(chart_config))

    if response.status_code == 201:
        chart_id = response.json().get('id')
        print(f"Chart created with ID: {chart_id}")
        return chart_id
    else:
        print(f"Error creating chart: {response.status_code}, {response.text}")
        return None

def upload_data_to_chart(chart_id, df):
    # Convert DataFrame to CSV format without index
    csv_data = df.to_csv(index=False)

    # Update the headers for CSV upload
    upload_headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'text/csv'  # Important: Content-Type should be text/csv when uploading data
    }

    upload_data_url = f"https://api.datawrapper.de/v3/charts/{chart_id}/data"
    response = requests.put(upload_data_url, headers=upload_headers, data=csv_data)

    # Expect a 204 No Content response for a successful data upload
    if response.status_code == 204:
        print("Data successfully uploaded to chart.")
    else:
        print(f"Error uploading data: {response.status_code}, {response.text}")

def publish_chart(chart_id):
    # API URL for publishing the chart
    publish_chart_url = f"https://api.datawrapper.de/v3/charts/{chart_id}/publish"
    
    response = requests.post(publish_chart_url, headers=headers)
    
    if response.status_code == 200:
        print(f"Chart published successfully. View it at: https://www.datawrapper.de/_/{chart_id}/")
    else:
        print(f"Error publishing chart: {response.status_code}, {response.text}")

# Example usage
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 30, 40]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a chart, upload data, and publish it
chart_id = create_chart("My Sample Chart")
if chart_id:
    upload_data_to_chart(chart_id, df)
    publish_chart(chart_id)