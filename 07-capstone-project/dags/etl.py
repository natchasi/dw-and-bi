import glob
import os
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone

def _get_files(filepath: str):
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files

def _create_tables():
    table_create_actors = """
        CREATE TABLE IF NOT EXISTS actors (
            id int,
            login text,
            url text,
            PRIMARY KEY(id)
        )
    """
    table_create_events = """
        CREATE TABLE IF NOT EXISTS events (
            id text,
            type text,
            actor_id int,
            PRIMARY KEY(id),
            CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id)
        )
    """
    table_create_repositories = """
        CREATE TABLE IF NOT EXISTS repositories (
            id text,
            name text,
            actor_id int,
            created_at timestamp,
            PRIMARY KEY(id),
            CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id)
        )
    """
    create_table_queries = [
        table_create_actors,
        table_create_events,
        table_create_repositories,
    ]

    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    conn = hook.get_conn()
    cur = conn.cursor()
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def _process(**context):
    # Get list of files from filepath
    # all_files = get_files(filepath)
    # print(all_files) 

    print(context)

    ti = context["ti"]
    all_files = ti.xcom_pull(task_ids="get_files", key="return_value")
    print(all_files)

    # connect to postgres
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    conn = hook.get_conn()
    cur = conn.cursor()

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                
                if each["type"] == "IssueCommentEvent": # this is how we store data
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # Insert data into "actors" tables here
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login,
                        url
                    ) VALUES ({each["actor"]["id"]}, '{each["actor"]["login"]}', '{each["actor"]["url"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into "events" tables here
                insert_statement = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id
                    ) VALUES ('{each["id"]}', '{each["type"]}', '{each["actor"]["id"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into "repositories" tables here
                insert_statement = f"""
                    INSERT INTO repositories (
                        id,
                        name,
                        actor_id,
                        created_at
                    ) VALUES ('{each["repo"]["id"]}', '{each["repo"]["name"]}', '{each["actor"]["id"]}', '{each["created_at"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                conn.commit()


with DAG(
    "etl",
    start_date=timezone.datetime(2024, 4, 2),
    schedule="@daily",
    tags=["swu"],
):

    start = EmptyOperator(task_id="start")

    get_files = PythonOperator(
        task_id="get_files",
        python_callable=_get_files,
        op_kwargs={
            "filepath": "/opt/airflow/dags/data"
        },
        # op_args=["/opt/airflow/dags/data"] # for list
    )

    create_tables = PythonOperator(
        task_id="create_tables",
        python_callable=_create_tables,
    )

    process = PythonOperator(
        task_id="process",
        python_callable=_process,
    )

    end = EmptyOperator(task_id="end")

    start >> [get_files, create_tables] >> process >> end