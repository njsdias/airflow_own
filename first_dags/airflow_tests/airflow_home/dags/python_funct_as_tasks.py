from airflow.operators.python import task
from airflow.models import DAG
from airflow.utils.dates import days_ago


@task
def numbers():
    return list(range(10))


@task
def show(xs):
    print(xs)


with DAG(dag_id="tasks_are_awesome",
         default_args={'owner': 'airflow'},
         start_date=days_ago(2),
         schedule_interval=None,
         ) as dag:
            xs = numbers()
            show(xs)

