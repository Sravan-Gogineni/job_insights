def bronze_layer_etl():
    import requests
    import pandas as pd
    import io
    import boto3
    from datetime import datetime
    import os
    print(os.getuid())
    session = boto3.Session(profile_name='sravan')
    client = session.client('s3', region_name='us-west-2')

    url = "https://api.apify.com/v2/datasets"
    params = {
        "token": "apify_api_Hix0y29ddpgD9PoOahbMHWsTKs8Hiy4xYXN7",
        "unnamed": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Request successful!")
        
        if 'data' in data and 'items' in data['data'] and data['data']['items']:
            first_id = data['data']['items'][-1]['id']
            print(f"Dataset ID: {first_id}")
        else:
            print("No items found in the response.")
            exit()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        exit()

    csv_url = f"https://api.apify.com/v2/datasets/{first_id}/items"
    params = {
        "token": "apify_api_Hix0y29ddpgD9PoOahbMHWsTKs8Hiy4xYXN7",
        "format": "csv"
    }

    response = requests.get(csv_url, params=params)

    if response.status_code == 200:
        print("CSV download successful!")
        
        csv_content = io.StringIO(response.text)
        df = pd.read_csv(csv_content)
        
        print("\nFirst few rows of the DataFrame:")
        print(df)
        
        print("\nDataFrame Info:")
        print(df.info())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    if len(df) > 0:
        csv_file_path = '/home/ubuntu/airflow/downloaded_files/all_jobs.csv'
        
        df.to_csv(csv_file_path, index=False)
        
        client.upload_file(csv_file_path, 'jobsproject', f'bronze_layer_all_jobs/all_jobs.csv')
        print("File uploaded")
    else:
        print("No data to upload.")
bronze_layer_etl()