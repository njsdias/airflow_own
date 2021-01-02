"""

Source: https://www.youtube.com/watch?v=XfK1KajB8dI&list=PLcoE64orFoVsyzbvfgiY5iNKo30fJ4IWm&index=7&ab_channel=RocketMan


USe hooks to retrieve files that's the sensor sensed and o something with this files.
Maybe print its contents and then delete it and then reschedule a tag and this will
kind of happen all over again.

"""
import os
from datetime import timedelta

from airflow.hooks.filesystem import FSHook
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(dag_id='my_first_hook',
          default_args=args,
          schedule_interval=None)


fs_conn_id = 'my_file_system'
file_name = 'test.txt'


def print_file_content(file_system_conn_id, file_name):
    # it was copied from FileSensor code
    hook = FSHook(file_system_conn_id)
    # get the file path
    path = os.path.join(hook.get_path(), file_name)
    print('Path of file is: ', path)
    # read the content file
    with open(path, 'r') as fp:
        print('Print out the content of the file')
        print(fp.read())

    # remove file
    os.remove(path)


sensing_task = FileSensor(task_id='sensing_task',
                          filepath=file_name,
                          fs_conn_id=fs_conn_id,
                          poke_interval=10,
                          dag=dag
                          )

read_file_content_task = PythonOperator(task_id='read_file_content_task_id',
                                        python_callable=print_file_content,
                                        op_args=[fs_conn_id, file_name],
                                        provide_context=True,
                                        retries=10,
                                        retry_delay=timedelta(seconds=1),
                                        dag=dag
                                        )

sensing_task >> read_file_content_task


