import pandas as pd
import boto3
import os

def load_and_process_merged_data():
    print("Loading CSV...")
    # data = pd.read_csv("merged_data.csv")
    s3 = boto3.client('s3')
    bucket_name = 'usecases-data'
    url = s3.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={'Bucket': bucket_name, 'Key': 'merged_data.csv.zip'},
                    ExpiresIn=7200  # URL expiration time in seconds (adjust as needed)
                )
    print(url)
    url_response = requests.get(url)
    with zipfile.ZipFile(BytesIO(url_response.content)) as z:
        z.extractall('.')
    print("Loaded CSV!")

    # Convert timestamp from object to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S.%f")

    # Dropped 'P-JUS-CKGL', 'T-JUS-CKGL', 'QGL', too many null values
    data.drop(['P-JUS-CKGL', 'T-JUS-CKGL', 'QGL'], axis=1, inplace=True)

    # Drop any rows with null values
    data.dropna(axis=0, how='any', inplace=True)
        
    # Convert class from float to int
    data['class'] = data['class'].astype(int, copy=False)

    # Drop rows with steady faulty states, except events 3 and 4 which are continously in transient faulty states
    values = [1, 2, 5, 6, 8]
    data = data[~data['class'].isin(values)]

    # Replace class values with single digit values for ease of reading
    data = data.replace({'class': {101:1, 102:2, 105:5, 106:6, 108:8}})

    print("Processed DataFrame.")
  
    return data

# load_and_process_merged_data()
