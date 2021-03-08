import psycopg2
import pandas as pd
import datetime as dt
import os
import re

def run_notebook(notebook_name):
    if re.match('[0-9]', notebook_name[5:6]) == None:
        print('python ' + notebook_name[0:5] + '/' + notebook_name + '.py' + ' ' + notebook_name)
    else:
        print('python ' + notebook_name[0:6] + '/' + notebook_name + '.py' + ' ' + notebook_name)

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

cur.execute("select "
                "distinct notebooks, "
                "max(last_beat_time) max_last_beat_time, "
                "nnm.seq_tw seq_no "
            "from "
                "public.notebook_names nnm "
            "right join "
                "heartbeat hbt "
            "on lower "
                "(replace(substring (hbt.notebook_name from 1 for (position('_' in hbt.notebook_name))),'_','')) = lower (notebooks)group by notebooks, seq_tw order by 3 asc")

list_of_notebooks = cur.fetchall()
notebooks = pd.DataFrame(list_of_notebooks, columns=['Notebook', 'Max Last Beat Time', 'Seq no'])
notebooks['Max Last Beat Time'] = pd.to_datetime(notebooks['Max Last Beat Time'])
notebooks.dropna(inplace=True)

backtests_notebooks = notebooks[~notebooks['Notebook'].str.contains('GPU')]
training_notebooks = notebooks[notebooks['Notebook'].str.contains('GPU')]

backtests_notebooks['Alive Status'] = dt.datetime.now() - backtests_notebooks['Max Last Beat Time'] < dt.timedelta(minutes=20)
training_notebooks['Alive Status'] = dt.datetime.now() - training_notebooks['Max Last Beat Time'] < dt.timedelta(minutes=20)

backtests_notebooks_sorted_on_last_beat_time = backtests_notebooks.sort_values(by='Max Last Beat Time', ignore_index=True)
training_notebooks_sorted_on_last_beat_time = training_notebooks.sort_values(by='Max Last Beat Time', ignore_index=True)

# print(backtests_notebooks)

# Only keep notebooks that ran not more than two hours ago
backtests_notebooks_sorted_on_last_beat_time = backtests_notebooks_sorted_on_last_beat_time.loc[
    (dt.datetime.now() - backtests_notebooks_sorted_on_last_beat_time['Max Last Beat Time'] < dt.timedelta(hours=17))
]

training_notebooks_sorted_on_last_beat_time = training_notebooks_sorted_on_last_beat_time.loc[
    (dt.datetime.now() - training_notebooks_sorted_on_last_beat_time['Max Last Beat Time'] < dt.timedelta(hours=17))
]

backtest_workers = backtests_notebooks_sorted_on_last_beat_time['Notebook']
training_workers = training_notebooks_sorted_on_last_beat_time['Notebook']



num_of_pending_backtests = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_pending_training_tasks = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'Training')]['Number']

num_of_backtests_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_training_tasks_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'Training')]['Number']
