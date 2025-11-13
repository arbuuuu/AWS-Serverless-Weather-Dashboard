# AWS-Serverless-Weather-Dashboard
A dynamic, serverless weather dashboard powered by AWS Lambda, API Gateway, S3, and OpenWeatherMap.

The dashboard features:

Live temperature, humidity, and wind speed.

A dynamic weather icon that matches the current conditions.

An automatic day/night theme with a light sky or animated night-sky background.

Core Architecture

The project works on a simple, event-driven data pipeline:

Amazon EventBridge (Scheduler): A rule is set to trigger every 15 minutes.

AWS Lambda (The Worker): The EventBridge rule invokes a Python Lambda function. This function:

Calls the OpenWeatherMap API to get current weather data.

Saves the data as a weather.json file in an S3 bucket.

Amazon S3 (Storage & Website): The S3 bucket is configured for static website hosting.

It stores the weather.json data file.

It hosts the index.html (this dashboard), which fetches the weather.json file to display the data.

AWS Services Used

AWS Lambda: For running the Python code to fetch data.

Amazon S3: For storing the data file (weather.json) and hosting the index.html website.

Amazon EventBridge: For scheduling the Lambda function to run automatically.

AWS IAM: For creating a role to give Lambda permission to write to S3.

How to Set This Up

S3 Bucket:

Create a new S3 bucket.

Disable "Block all public access" in the Permissions tab.

Enable "Static website hosting" in the Properties tab and set the index document to index.html.

Copy the Bucket website endpoint URL.

Lambda Function:

Create a new Lambda function (e.g., getWeatherFunction with Python 3.11).

Increase the Timeout to 15 seconds.

In Permissions, find the function's Role and attach the AmazonS3FullAccess policy.

Copy the code from lambda_function.py into the editor.

CRITICAL: Fill in your API_KEY and BUCKET_NAME at the top of the lambda_function.py file.

Deploy and Test the function. You should see weather.json appear in your S3 bucket.

EventBridge Rule:

Create a new EventBridge Rule.

Set the Rule type to Schedule.

Set the schedule (e.g., "A schedule that runs at a regular rate" of 15 minutes).

Set the Target to your getWeatherFunction Lambda function.

Dashboard Frontend:

Copy the code from index.html.

Upload this file to your S3 bucket.

In the S3 bucket, select both index.html and weather.json, click Actions > Make public using ACL.

Paste your Bucket website endpoint URL from Step 1 into your browser. Your dashboard is live!
