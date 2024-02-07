# RUN data modeling I
1. RUN cd 01-data-modeling-i to direct in folder
2. Open etl.py file and run python library to connect postgres (install package) by "pip install psycopg2" 
3. Run docker compose file (popstgres) with > $ docker compose up
4. Add another teminal to run python file that connect to postgres
5. Run create_table.py with > $ python create_table.py
6. Run etl.py with > $ python etl.py