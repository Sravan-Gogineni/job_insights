def silver_layer_etl():
    import boto3
    import botocore
    import pandas as pd
    import datetime
    import re
    import numpy as np

    session = boto3.Session(profile_name='sravan')
    s3 = session.client('s3')

    def download_file_from_s3(bucket_name, object_key, local_file_path):
        try:
            s3.download_file(bucket_name, object_key, local_file_path)
            print(f"File downloaded successfully to {local_file_path}")
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist in S3.")
            else:
                print(f"An error occurred: {e}")

    bucket_name = 'jobsproject'
    object_key = 'bronze_layer_all_jobs/all_jobs.csv'
    local_file_path = '/home/ubuntu/airflow/downloaded_files/downloaded_all_jobs.csv' 

    download_file_from_s3(bucket_name, object_key, local_file_path)

    df = pd.read_csv('/home/ubuntu/airflow/downloaded_files/downloaded_all_jobs.csv')

    columns_to_select = ['company','companyOverviewLink','companyRating','companyReviewCount','displayTitle','extractedSalary/max','extractedSalary/min','extractedSalary/type','feedId','formattedLocation','formattedRelativeTime','jobDescription','jobLocationCity','jobLocationState','jobTypes/0','jobTypes/1','normTitle','pubDate','salarySnippet/currency','salarySnippet/text','snippet','taxonomyAttributes/0/attributes/0/label','taxonomyAttributes/2/attributes/0/label','taxonomyAttributes/2/label','taxonomyAttributes/3/attributes/1/label','taxonomyAttributes/3/attributes/2/label','taxonomyAttributes/3/attributes/3/label','taxonomyAttributes/3/attributes/4/label','taxonomyAttributes/3/attributes/5/label','taxonomyAttributes/3/attributes/6/label','taxonomyAttributes/3/attributes/7/label','taxonomyAttributes/3/attributes/8/label','taxonomyAttributes/3/attributes/9/label','taxonomyAttributes/3/attributes/10/label','taxonomyAttributes/3/attributes/11/label','taxonomyAttributes/4/attributes/0/label','thirdPartyApplyUrl','title','truncatedCompany']
    df_selected = pd.read_csv(local_file_path, usecols=columns_to_select)

    df_selected['converted_datetime'] = pd.to_datetime(df_selected['pubDate'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    df_selected['zipcode'] = df_selected['formattedLocation'].str.extract(r'(\d{5})$')

    state_names = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    } 
    df_selected['jobLocationState_full'] = df_selected['jobLocationState'].map(state_names)

    df_selected['job_type'] = df_selected['taxonomyAttributes/4/attributes/0/label'].fillna(df_selected['jobTypes/0']).fillna(df_selected['jobTypes/1']).fillna(df_selected['taxonomyAttributes/2/attributes/0/label']).fillna(df_selected['taxonomyAttributes/2/label']).fillna('w2')

    df_selected['average_expected_salary'] = df_selected.apply(lambda row: 
        f"{(np.mean([row['extractedSalary/max'], row['extractedSalary/min']]) * (2080 if row['extractedSalary/type'] == 'hourly' else 1)):.2f}"
        if pd.notnull(row['extractedSalary/max']) and pd.notnull(row['extractedSalary/min']) else np.nan, axis=1)

    columns_to_be_dropped = [
        'taxonomyAttributes/4/attributes/0/label',
        'jobTypes/0',
        'jobTypes/1',
        'pubDate',
        'taxonomyAttributes/0/attributes/0/label',
        'taxonomyAttributes/2/attributes/0/label',
        'extractedSalary/max',
        'extractedSalary/min',
        'formattedRelativeTime',
        'salarySnippet/currency',
        'salarySnippet/text',
        'taxonomyAttributes/2/label'
    ]

    df_selected = df_selected.drop(columns=columns_to_be_dropped)

    benefit_columns = [
        'taxonomyAttributes/3/attributes/1/label',
        'taxonomyAttributes/3/attributes/2/label',
        'taxonomyAttributes/3/attributes/3/label',
        'taxonomyAttributes/3/attributes/4/label',
        'taxonomyAttributes/3/attributes/5/label',
        'taxonomyAttributes/3/attributes/6/label',
        'taxonomyAttributes/3/attributes/7/label',
        'taxonomyAttributes/3/attributes/8/label',
        'taxonomyAttributes/3/attributes/9/label',
        'taxonomyAttributes/3/attributes/10/label',
        'taxonomyAttributes/3/attributes/11/label'
    ]

    column_names = [
        'company',
        'companyOverviewLink',
        'companyRating',
        'companyReviewCount',
        'displayTitle',
        'extractedSalary/type',
        'feedId',
        'formattedLocation',
        'jobDescription',
        'jobLocationCity',
        'jobLocationState',
        'normTitle',
        'snippet',
        'thirdPartyApplyUrl',
        'title',
        'truncatedCompany',
        'converted_datetime',
        'zipcode',
        'jobLocationState_full',
        'job_type',
        'average_expected_salary'
    ]

    df_benefits = df_selected.melt(id_vars=column_names,
                                    value_vars=benefit_columns,
                                    var_name='attribute_label', value_name='benefits_offered')

    df_benefits = df_benefits.dropna(subset=['benefits_offered'])

    df_benefits.reset_index(drop=True, inplace=True)
    columns_to_be_dropped = ["attribute_label","formattedLocation","truncatedCompany"]

    df_benefits = df_benefits.drop(columns=columns_to_be_dropped)
    df_benefits = df_benefits.where(pd.notnull(df_benefits), None) 
    df_benefits.to_csv('/home/ubuntu/airflow/downloaded_files/cleaned_job_file.csv', index=False)
silver_layer_etl()