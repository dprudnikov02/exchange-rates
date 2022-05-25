from json import loads, dumps
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from btc_usd_dag_utils import get_response, transform_response

URL = 'https://api.exchangerate.host/latest'
PAYLOAD = {'base': 'BTC', 'symbols': 'USD', 'source': 'crypto'}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 5, 24),
    'retries': 0
}

with DAG(
        dag_id='btc_usd_etl',
        description='This dag get latest btc/usd rate every 3 hours',
        schedule_interval=timedelta(hours=3),
        default_args=default_args,
        tags=['exchange_rate', 'btc', 'usd']
) as dag:
    create_exchange_rates_table_task = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql='sql/ddl/tables/exchange_rates.sql'
    )


    def extract(**kwargs):
        ti = kwargs['ti']
        ti.xcom_push('response', dumps(get_response(URL, PAYLOAD)))


    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )


    def transform(**kwargs):
        ti = kwargs['ti']
        response = loads(ti.xcom_pull(task_ids='extract', key='response'))
        ti.xcom_push('latest_rate', transform_response(response, PAYLOAD))


    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_task = PostgresOperator(
        task_id='load',
        postgres_conn_id='postgres_default',
        sql='sql/dml/insert/exchange_rates.sql'
    )

    create_exchange_rates_table_task >> extract_task >> transform_task >> load_task
