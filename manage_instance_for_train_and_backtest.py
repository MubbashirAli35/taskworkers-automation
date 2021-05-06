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

cur.execute("SELECT count(*) FROM task_manager_queue where queue_type = 'Parent' and "
            "queue_status = 'Waiting(No NoteBook)' and process_type='ParentConfig' and "
            "queue_state='New'")

parent_count = cur.fetchall()
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
    print(parent_count[0][0])
    if parent_count[0][0] == 0:
        stop_instance()
    else:
        start_instance()
