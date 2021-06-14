import psycopg2
import pandas as pd
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

conn = psycopg2.connect(dbname='greencanvas',
                        user='gcpv1_colab_server',
                        password='gc$%#798w',
                        host='gcp01.dynamic-dns.net',
                        port=5432)

cur = conn.cursor()

cur.execute("SELECT count(*) FROM task_manager_queue where queue_type = 'Parent' and "
            "queue_status = 'Waiting(No NoteBook)' and process_type='ParentConfig' and "
            "queue_state='New'")

parent_count = cur.fetchall()

cur.execute("select count (queue_state), queue_state, queue_type "
            "from task_manager_queue tmq "
            "where creation_date > now() - interval '10days'"
            "group by queue_state, queue_type")

list_of_queue = cur.fetchall()

tasks_queue = pd.DataFrame(list_of_queue, columns=['Number', 'Status', 'Task Type'])

gcloud_login_credentials = GoogleCredentials.get_application_default()


def start_instance():
    service = discovery.build('compute', 'v1', credentials=gcloud_login_credentials)
    project = 'april-25-2020-test'
    zone = 'us-central1-a'
    instance = 'instance-for-managers-train-backtest'

    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()

    pprint(response)


def stop_instance():
    service = discovery.build('compute', 'v1', credentials=gcloud_login_credentials)
    project = 'april-25-2020-test'
    zone = 'us-central1-a'
    instance = 'instance-for-managers-train-backtest'

    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()

    pprint(response)


if __name__ == '__main__':
    num_of_pending_backtests = \
        tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
    num_of_pending_training_tasks = \
        tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']
    num_of_pending_kmeans_tasks = \
        tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'KmeansTask')]['Number']

    num_of_backtests_running = \
        tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
    num_of_training_tasks_running = \
        tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']
    num_of_kmeans_tasks_running = \
        tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'KmeansTask')]['Number']

    print(parent_count[0][0])
    if num_of_pending_backtests.count() > 0 or num_of_pending_training_tasks.count() > 0 \
        or num_of_backtests_running.count() > 0 or num_of_training_tasks_running.count() > 0 \
            or num_of_pending_kmeans_tasks.count() > 0 or num_of_kmeans_tasks_running.count() > 0 \
            or parent_count[0][0] != 0:
        start_instance()
    else:
        stop_instance()
