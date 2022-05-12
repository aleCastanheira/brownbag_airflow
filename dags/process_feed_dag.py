from datetime import datetime
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from helpers.tsk_process_feed import parse_feed, compile_data, create_report

dag = DAG(
    'process_feed',
    description='Processa vários feeds de notícias e compila em um relatório.',
    schedule_interval='@once',
    start_date=datetime(2022, 2, 24),
    catchup=False
)

_get_tech_feed = PythonOperator(
    task_id='get_tech_feed',
    python_callable=parse_feed,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "feed_url": Variable.get("feed_tech")
    }
)

_get_sports_feed = PythonOperator(
    task_id='get_sports_feed',
    python_callable=parse_feed,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "feed_url": Variable.get("feed_sports")
    }
)

_get_cinema_feed = PythonOperator(
    task_id='get_cinema_feed',
    python_callable=parse_feed,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "feed_url": Variable.get("feed_cinema")
    }
)

_compile_feed = PythonOperator(
    task_id='compile_data',
    python_callable=compile_data,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "task_list": [
            "get_cinema_feed",
            "get_sports_feed",
            "get_tech_feed"
        ]
    }
)

_create_report = PythonOperator(
    task_id='create_report',
    python_callable=create_report,
    provide_context=True,
    dag=dag,
    op_kwargs={
        "entries": "{{ ti.xcom_pull(key='compiled_entries', task_ids='compile_data') }}"
    }
)

(_get_tech_feed, _get_sports_feed, _get_cinema_feed) >> _compile_feed >> _create_report