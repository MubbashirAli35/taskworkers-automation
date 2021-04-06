import psycopg2
import pandas as pd
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

conn = psycopg2.connect(dbname='greencanvas',
                        user='gcp_read_only',
                        password='gc$$2929%',
                        host='35.223.254.139',
                        port=5432)

cur = conn.cursor()

cur.execute("select count (queue_state), queue_state, queue_type "
            "from task_manager_queue tmq "
            "where creation_date > now() - interval '10days'"
            "group by queue_state, queue_type")

list_of_queue = cur.fetchall()

tasks_queue = pd.DataFrame(list_of_queue, columns=['Number', 'Status', 'Task Type'])


def start_colab_server(gcloud_login_credentials):
    service = discovery.build('compute', 'v1', credentials=gcloud_login_credentials)
    project = 'april-25-2020-test'
    zone = 'us-central1-a'
    instance = 'colab-server-1'

    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()

    pprint(response)


def stop_colab_server(gcloud_login_credentials):
    service = discovery.build('compute', 'v1', credentials=gcloud_login_credentials)
    project = 'april-25-2020-test'
    zone = 'us-central1-a'
    instance = 'colab-server-1'

    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()

    pprint(response)


if __name__ == '__main__':
    credentials = GoogleCredentials.get_application_default()

    num_of_pending_backtests = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
    num_of_pending_training_tasks = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']

    num_of_backtests_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
    num_of_training_tasks_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']

    if num_of_pending_backtests.count() > 0 or num_of_pending_training_tasks.count() > 0 or num_of_backtests_running.count() > 0 or num_of_training_tasks_running.count():
        start_colab_server(credentials)
    else:
        stop_colab_server(credentials)
