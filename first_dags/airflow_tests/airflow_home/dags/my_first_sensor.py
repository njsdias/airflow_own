"""
Sensoring Files.

It is required that a file exists ina  folder to proceed with
the next task.
Usually we don't know when this file is available.
For this we can use a sensor that will check at every time
(poke in seconds) if the file exists in the folder (path).
When the files is detected the next task is executed.

Source: https://www.youtube.com/watch?v=I7Mhs4W3Whs&list=PLcoE64orFoVsyzbvfgiY5iNKo30fJ4IWm&index=6&ab_channel=RocketMan

To pass values between tasks we can use XCom
"""
from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(dag_id='my_first_sensor',
          default_args=args,
          schedule_interval=None)


def say_hi(**context):
    print('hi')


file_path = '/Documents/airflow_tests/'
file_name = 'test.txt'
full_filepath = file_path + file_name

sensing_task = FileSensor(task_id='sensing_task',
                          filepath=full_filepath,
                          poke_interval=10,
                          dag=dag
                          )

run_this_task = PythonOperator(task_id='run_this_task',
                               python_callable=say_hi,
                               provide_context=True,
                               retries=10,
                               retry_delay=timedelta(seconds=1),
                               dag=dag
                               )

sensing_task >> run_this_task
