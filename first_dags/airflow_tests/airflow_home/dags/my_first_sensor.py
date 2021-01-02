"""
Using sensors to sense files

It is required that a file exists ina  folder to proceed with
the next task.
Usually we don't know when this file is available.
For this we can use a sensor that will check at every time
(poke in seconds) if the file exists in the folder (path).
When the files is detected the next task is executed.

Source: https://www.youtube.com/watch?v=I7Mhs4W3Whs&list=PLcoE64orFoVsyzbvfgiY5iNKo30fJ4IWm&index=6&ab_channel=RocketMan

To pass values between tasks we can use XCom

FileSensor receives:
    - filepath : it is the file name
    - fs_conn_id: it is the path where the file needs to be.
                  It is configure in webserver UI(Admin-Connections)

To configure a connection we need to provide a
    - Conn ID: give a name for your connection
    - Conn Type: choose the connection type. If the file is in your filesystem choose the option File(path)
    - Extra: type the file path like this: {"path": "\path_to_the_file"

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

dag = DAG(dag_id='my_first_sensor_2',
          default_args=args,
          schedule_interval=None)


def say_hi(**context):
    print('hi')


file_name = 'test.txt'

sensing_task = FileSensor(task_id='sensing_task',
                          filepath=file_name,
                          fs_conn_id='my_file_system',
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
