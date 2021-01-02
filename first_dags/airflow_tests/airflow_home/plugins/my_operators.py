# https://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/

import logging
from datetime import datetime
from airflow.models import BaseOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)


class MyFirstOperator(BaseOperator):
    """
        An Operator is an atomic block of workflow logic,
        which performs a single action
    """

    @apply_defaults
    def __init__(self, my_operator_param, *args, **kwargs):
        self.operator_param = my_operator_param
        super(MyFirstOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        # Remember that since the execute method can retry many times, it should be idempotent.
        log.info('Hello World!')
        log.info('operator_param: %s', self.operator_param)


class MyFirstSensor(BaseSensorOperator):
    """
        Sensor: typically used to monitor a long running task on another system.
        Description: This sensor which will wait until the the current minute is a number divisible by 3.
        When this happens, the sensor’s condition will be satisfied and it will exit.
    """

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(MyFirstSensor, self).__init__(*args, **kwargs)

    def poke(self, context):
        current_minute = datetime.now().minute
        if current_minute % 3 != 0:
            log.info("Current minute (%s), not is divisible by 3, sensor will retry.", current_minute)
            return False
        log.info("Current minute (%s), is divisible by 3, sensor finishing.", current_minute)
        return True


class MyFirstPlugin(AirflowPlugin):
    name = 'my_first_operator'
    operators = [MyFirstOperator, MyFirstSensor]
