# BTC/USD Latest Exchange Rate ETL
This is simple ETL process to get the latest exchange rate for pair
BTC/USD. This ETL process gets data from [exchangerate.host](https://exchangerate.host/#/)
via REST API and loads it to postgres database every three hours. It is 
written by python and apache airflow.

## Requirements:
Because this process runs in docker using docker compose, there is one 
requirement: [docker engine](https://docs.docker.com/engine/install/) 
and [docker compose](https://docs.docker.com/compose/)  have to be installed 
on your workstation.

## How to use:
When satisfying all requirements, process can be run. To do this:
1. Download this repo to your workstation.
2. In terminal go to folder with project root.
3. Create folder **./logs** to save future logs. 
4. Run `docker-compose up airflow-init` to initialize.
5. Run `docker-compose up` to start all airflow services.
6. After all services have started up, the web UI will be available 
at: http://localhost:8080. The default account has the username **airflow** 
and the password **airflow**.
7. After logging in connection to postgres has to be created. To do this go
select **Connections** from admin menu and then click the plus sign to add a new record.
Fill in the fields as shown below and after that save it:
    - Connection Id: postgres_default
    - Connection Type: postgres
    - Host: postgres
    - Schema: airflow
    - Login: airflow
    - Password: airflow
    - Port: 5432
8. Finally, you can find **btc_usd_etl** dag on DAGs page and run it with play button.