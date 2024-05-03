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

def _get_accident_api():
    
    api_key = "ceT50TBxKgnMdanDpv7DMW4dQzBim76H"

    headers = {
    "api-key": api_key,
    }

    params = {"resource_id": "d1ab8a36-c5f7-4efb-b613-63310054b0bc", "limit": 10000}

    response = requests.get(
        "https://opend.data.go.th/get-ckan/datastore_search", params, headers=headers
    )

    data = response.json()
    records = data.get("result", {}).get("records", [])
    logging.info(records)

    # Save records to a JSON file
    with open("/opt/airflow/dags/RoadAccident_2566.json", "w") as f:
        json.dump(records, f)  # Use indent for better readability

with DAG(
    "accident_api_pipeline", #dag_id should be same as filename
    start_date=timezone.datetime(2024, 4, 16),
    schedule="@yearly", # Cron Expression
    tags=["DS525"],
):

    start = EmptyOperator(task_id="start")

    install_pip_packages = BashOperator(
        task_id="install_pip_packages",
        bash_command='pip install -r requirement.txt',
    )

    get_accident_api = PythonOperator(
        task_id="get_accident_api",
        python_callable=_get_accident_api,
    )

    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/opt/airflow/dags/RoadAccident_2566.json",
        dst="RoadAccident_2566.json",
        bucket="07project_cap",
        gcp_conn_id="my_gcp_conn"
        #move_object=True
    )

    end = EmptyOperator(task_id="end")

    start >> get_accident_api >> upload_to_gcs >> end
