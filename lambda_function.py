import json
import urllib3
import boto3 # This is the AWS SDK, already included!

# --- 1. SET YOUR DETAILS HERE ---
API_KEY = '' # Paste your key from Step 1
CITY = 'New Delhi,India' # Or any city
BUCKET_NAME = 'yourname-weather-dash-12345' # Your S3 bucket from Step 2
# --- ------------------------ ---

FILE_NAME = 'weather.json' # The data file your website will read
http = urllib3.PoolManager()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    # --- 2. Get Weather Data ---
    print("Fetching weather data...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    try:
        r = http.request('GET', url)
        data = json.loads(r.data.decode('utf-8'))
        print(f"Successfully fetched data: {data}")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error fetching data: {e}")}
    
    # --- 3. Save Data to S3 ---
    print(f"Saving {FILE_NAME} to S3 bucket {BUCKET_NAME}...")
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_NAME,
            Body=json.dumps(data), # Convert the Python dict back to a JSON string
            ContentType='application/json', # So browsers know it's JSON
            ACL='public-read' # CRITICAL: Make the file public
        )
        print("Successfully saved to S3")
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error uploading to S3: {e}")}


    return {'statusCode': 200, 'body': json.dumps('Weather data updated!')}
