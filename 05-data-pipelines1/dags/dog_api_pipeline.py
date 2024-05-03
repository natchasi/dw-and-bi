import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils import timezone

import requests
import json

def _get_dog_api():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    logging.info(data)
    with open("/opt/airflow/dags/dog.json", "w") as f: # write python file // for append use "a" but need to assign to start new line
        json.dump(data, f)

with DAG(
    "dog_api_pipeline", #dag_id should be same as filename
    start_date=timezone.datetime(2024, 3, 23),
    schedule="@daily", # Cron Expression
    tags=["DS525"],
):
    start = EmptyOperator(task_id="start")

    get_dog_api = PythonOperator(
        task_id="get_dog_api",
        python_callable=_get_dog_api,
    )

    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/opt/airflow/dags/dog.json",
        dst="dog.json",
        bucket="swu-ds525-8888",
        gcp_conn_id="my_gcp_conn"
        #move_object=True
    )

    end = EmptyOperator(task_id="end")

    start >> get_dog_api >> upload_to_gcs >> end