# Running Airflow with Docker Compose

1. Start the Airflow environment:
```
$ docker compose up
```

2. (Optional) Add data to DAGs folder:
add data file to `dags` This folder is mounted inside the container at `/opt/airflow/dags` by Docker Compose

3. Access Airflow web UI:
Open your web browser and navigate to `http://localhost:8080`. This opens the Apache Airflow web interface where you can monitor and manage your workflows.

4. Configure DAG with `etl.py`:
Edit the etl.py file located in your `DAGs` folder. This script defines the Python functions for your data processing tasks.

5. Access Postgres from container:
`docker compose exec postgres bash`

# Explanation of configurations:

Mounting volumes: The configuration snippet defines how your local directories (dags, logs, config, and plugins) are mapped to directories inside the container for persistence.
Airflow web server: This section configures the airflow-webserver service. It specifies the command to run (webserver), maps the container port 8080 to your host machine's port 8080, defines a health check for the service, and sets restart behavior.
