# Instruction 

> Run Docker Compose
```
$ docker compose up
```

> Add data to dags folder (or API)

> Open Apache Airflow web server from port 8080

> Open elt.py 
to config script and automate with airflow

> To excecute postgres on bash shell
to access postgres and be able to query with bash
```
$ docker compose exec postgres bash
```

# Documentation

## Configuration for Docker Compose

### Mounting volumes into the container, including dags, logs, config, and plugins

```
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
```

### Managing Apache Airflow's web server

Mapping Apache Airflow's web server to port 8080 and setting helthcheck

```
airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
```

## Configuration for etl.py file

### Creating functions
> get files
```
get_files = PythonOperator(
        task_id="get_files",
        python_callable=_get_files,
        op_kwargs={
            "filepath": "/opt/airflow/dags/data"
        },
        # op_args=["/opt/airflow/dags/data"] # for list
    )
```

> create tables
```
create_tables = PythonOperator(
        task_id="create_tables",
        python_callable=_create_tables,
    )
```

> process
```
process = PythonOperator(
        task_id="process",
        python_callable=_process,
    )
```

### Creating connection with hook and applying on create tables and process function
This process is for maintaining the credentiallity
```
# connect to postgres
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    conn = hook.get_conn()
    cur = conn.cursor()
```

### Creating DAG to automate workflow with Airflow
> Creating DAG
```
with DAG(
    "etl",
    start_date=timezone.datetime(2024, 4, 2),
    schedule="@daily",
    tags=["swu"],
):
```
> Creating operators and assigning tasks based on functions
```
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
```
> Setting workflow
```
start >> [get_files, create_tables] >> process >> end
```