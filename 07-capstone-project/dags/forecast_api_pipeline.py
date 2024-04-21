import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils import timezone

import requests
import json
from datetime import datetime


def _get_forecast_api():

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"

    querystring = {"formatType":"test"}

    headers = {
	"X-RapidAPI-Key": "e411c4b8b0msh76a56596db09506p178066jsn2356223ed8eb",
	"X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    logging.info(data)

    # Extract specific columns: id, rank, name, country
    selected_data = [{"id": player["id"], "rank": player["rank"], "name": player["name"], 
                    "country": player["country"], "rating": player["rating"], "lastUpdatedOn": player["lastUpdatedOn"]} 
                    for player in data["rank"]
                    ]

    # # Create a unique filename based on the current timestamp
    # timestamp = datetime.now().strftime("%Y-%m-%d")
    # filename = f"/opt/airflow/dags/prov_forecast_{timestamp}.json"
    
    # with open(filename, "w") as f: # write python file // for append use "a" but need to assign to start new line
    #     json.dump(selected_data, f, indent=2)  # Use indent for better readability
    
    with open("/opt/airflow/dags/prov_forecast.json", "w") as f: # write python file // for append use "a" but need to assign to start new line
        json.dump(selected_data, f, indent=2)  # Use indent for better readability


with DAG(
    "forecast_api_pipeline", #dag_id should be same as filename
    start_date=timezone.datetime(2024, 4, 14),
    schedule="@daily", # Cron Expression
    tags=["DS525"],
):
    start = EmptyOperator(task_id="start")

    get_forecast_api = PythonOperator(
        task_id="get_forecast_api",
        python_callable=_get_forecast_api,
    )

    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/opt/airflow/dags/prov_forecast.json",
        dst="prov_forecast.json",
        bucket="swu-ds525-8888",
        gcp_conn_id="my_gcp_conn"
        #move_object=True
    )

    end = EmptyOperator(task_id="end")

    start >> get_forecast_api >> upload_to_gcs >> end