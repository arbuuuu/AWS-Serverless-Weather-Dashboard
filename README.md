# AWS-Serverless-Weather-Dashboard
A dynamic, serverless weather dashboard powered by AWS Lambda, API Gateway, S3, and OpenWeatherMap.

# AWS Serverless Weather Dashboard

[![Serverless](https://img.shields.io/badge/serverless-AWS-f90.svg)](https://aws.amazon.com/serverless/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A dynamic, serverless weather dashboard built from scratch using AWS Lambda, API Gateway, and S3. This project fetches and displays the current weather, a 5-day forecast, and detailed metrics for any city in the world.


*(**Pro-tip:** Take a screenshot of your working app and upload it to your repo. Then, edit this line and replace the text with the image link, like `![App Screenshot](screenshot.png)`)*

---

## ✨ Features

* **Dynamic City Search:** Instantly fetch weather data for any city.
* **Current Weather:** Displays the current temperature, description, and "feels like" temp.
* **5-Day Forecast:** Shows a 5-day outlook with calculated max/min temperatures and conditions.
* **Detailed Weather Grid:** A professional grid layout showing:
    * Feels Like
    * Wind Speed & Direction
    * Humidity
    * Visibility
    * Air Pressure
    * Cloudiness
* **Dynamic Day/Night Theme:** The UI automatically switches between a "day" and "night" theme based on the city's local sunrise/sunset times.
* **Fully Serverless:** No servers to manage. The entire application runs on the AWS free tier.

## 🏛️ Architecture

This project uses a classic serverless "pull" architecture. The frontend is decoupled from the backend, and the backend only runs when it's needed (i.e., when a user searches).

`[User's Browser (S3)]` -> `[API Gateway Endpoint]` -> `[AWS Lambda Function]` -> `[OpenWeatherMap API]`



* **Frontend (Amazon S3):** A single, static `index.html` file (with all CSS/JS) is hosted in an S3 bucket configured for static website hosting.
* **API (Amazon API Gateway):** An HTTP API Gateway provides a single, public-facing REST endpoint (`GET /weather`).
* **Backend (AWS Lambda):** The API Gateway triggers a Python Lambda function (`lambda_function.py`). This function:
    1.  Parses the `city` from the request.
    2.  Calls the OpenWeatherMap `/forecast` API.
    3.  Processes the 40-entry list into a clean 5-day forecast, calculating daily min/max temps.
    4.  Calculates the wind direction (e.g., "NNW").
    5.  Returns a clean, simple JSON response to the frontend.
* **Data Source:** [OpenWeatherMap 5 Day / 3 Hour Forecast API](https://openweathermap.org/forecast5).

---

## 🚀 Setup & Deployment

To deploy this project yourself, you will need an AWS account and a free OpenWeatherMap API key.

### 1. Backend (Lambda & API)

1.  **Create Lambda Function:**
    * Go to the AWS Lambda console and create a new function (e.g., `weather-search-function`) using the `Python 3.12` (or newer) runtime.
    * Copy the code from `backend/lambda_function.py` into the Lambda code editor.
    * Go to **Configuration > Environment variables** and add your OpenWeatherMap key:
        * **Key:** `API_KEY`
        * **Value:** `your-openweathermap-api-key-here`
    * Click **Deploy**.

2.  **Create API Gateway:**
    * Go to the API Gateway console and create a new **HTTP API**.
    * Create a new route: `GET /weather`.
    * Attach an integration to this route that points to your `weather-search-function` Lambda.
    * Note the **Invoke URL** once it's created (e.g., `https://abcdef.execute-api.us-region-1.amazonaws.com`).

### 2. Frontend (S3)

1.  **Create S3 Bucket:**
    * Go to the S3 console and create a new public bucket (e.g., `my-weather-dashboard-123`).
    * **Uncheck** "Block all public access" and acknowledge the warning.
    * Go to the **Properties** tab, scroll to the bottom, and enable **Static website hosting**. Set the index document to `index.html`.
    * Go to the **Permissions** tab and add this **Bucket Policy** (replace `YOUR-BUCKET-NAME-HERE` with your bucket's name):
        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME-HERE/*"
                }
            ]
        }
        ```

2.  **Configure & Upload:**
    * Open the `frontend/index.html` file in a text editor.
    * Find the `const API_URL = ...` line in the `<script>` tag.
    * Replace the placeholder URL with your **API Gateway Invoke URL** from step 1, making sure to add `/weather` to the end.
        ```javascript
        // Before:
        // const API_URL = '[https://abcdef.execute-api.us-region-1.amazonaws.com/weather](https://abcdef.execute-api.us-region-1.amazonaws.com/weather)';

        // After (example):
        const API_URL = '[https://fj8fyttluf.execute-api.ap-south-1.amazonaws.com/weather](https://fj8fyttluf.execute-api.ap-south-1.amazonaws.com/weather)';
        ```
    * Save the file and **upload** the modified `index.html` to your S3 bucket.

### 3. Launch!

* Go back to your S3 bucket's **Properties** tab, find the **Static website hosting** URL, and click it. Your app is live.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
