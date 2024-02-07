# RUN data modeling II
1. RUN cd 02-data-modeling-ii to direct in folder
2. Open etl.py file and run python library to connect cassandra (install package) by "$ pip install cqlsh" 
3. Run docker compose file (popstgres) with > $ docker compose up
4. Add another teminal to run python file that connect to cassandra
5. Run etl.py with > $ python etl.py
6. RUN $ cqlsh for connect to the Test Cluster
7. RUN cqlsh> select * FROM github_events.events ; for verify connection of database
8. RUN cqlsh> exit to workspaces