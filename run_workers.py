import psycopg2
import pandas as pd
import datetime as dt
import os
import re
from multiprocessing import Process
import sys


def run_notebook(notebook_name, action):
    if re.match('[0-9]', notebook_name[5:6]) == None:
        os.system('python ' + notebook_name[0:5] + '/' + notebook_name + '.py' + ' ' + notebook_name + ' ' + action)
    else:
        os.system('python ' + notebook_name[0:6] + '/' + notebook_name + '.py' + ' ' + notebook_name + ' ' + action)

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

# Only keep notebooks that ran not more than two hours ago
# backtests_notebooks_sorted_on_last_beat_time = backtests_notebooks_sorted_on_last_beat_time.loc[
#     (dt.datetime.now() - backtests_notebooks_sorted_on_last_beat_time['Max Last Beat Time'] < dt.timedelta(hours=17))
# ]
#
# training_notebooks_sorted_on_last_beat_time = training_notebooks_sorted_on_last_beat_time.loc[
#     (dt.datetime.now() - training_notebooks_sorted_on_last_beat_time['Max Last Beat Time'] < dt.timedelta(hours=17))
# ]

backtests_notebooks_to_run = backtests_notebooks_sorted_on_last_beat_time.loc[
    backtests_notebooks_sorted_on_last_beat_time['Alive Status'] == False
]

backtests_notebooks_to_interact = backtests_notebooks_sorted_on_last_beat_time.loc[
    backtests_notebooks_sorted_on_last_beat_time['Alive Status'] == True
]

training_notebooks_to_run = training_notebooks_sorted_on_last_beat_time.loc[
    training_notebooks_sorted_on_last_beat_time['Alive Status'] == False
]

training_notebooks_to_interact = training_notebooks_sorted_on_last_beat_time.loc[
    training_notebooks_sorted_on_last_beat_time['Alive Status'] == True
]

backtests_notebooks_to_run = backtests_notebooks_to_run['Notebook']
training_notebooks_to_run = training_notebooks_to_run['Notebook']

# for notebook in training_notebooks_to_run:
#     print(notebook)

backtests_notebooks_to_interact = backtests_notebooks_to_interact['Notebook']
training_notebooks_to_interact = training_notebooks_to_interact['Notebook']

# print(backtests_notebooks_to_run[0])
# print(training_notebooks_to_run[1])

# run_notebook(backtests_notebooks_to_run[0])
# run_notebook(backtests_notebooks_to_run[1])

num_of_pending_backtests = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_pending_training_tasks = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']

num_of_backtests_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_training_tasks_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']

if __name__ == '__main__':
    print(dt.datetime.now())
    print('\n\n')
    # print(num_of_pending_training_tasks.count())
    # print(num_of_pending_training_tasks.iloc[0])

    if sys.argv[1].lower() == 'interact':
        for i in range(0, backtests_notebooks_to_interact.count(), 5):
            if i < backtests_notebooks_to_interact.count():
                notebook_1 = Process(target=run_notebook, args=(backtests_notebooks_to_interact.iloc[i], sys.argv[1],))
                notebook_1.start()
            if i + 1 < backtests_notebooks_to_interact.count():
                notebook_2 = Process(target=run_notebook,
                                     args=(backtests_notebooks_to_interact.iloc[i + 1], sys.argv[1],))
                notebook_2.start()
            if i + 2 < backtests_notebooks_to_interact.count():
                notebook_3 = Process(target=run_notebook,
                                     args=(backtests_notebooks_to_interact.iloc[i + 2], sys.argv[1],))
                notebook_3.start()
            if i + 3 < backtests_notebooks_to_interact.count():
                notebook_4 = Process(target=run_notebook,
                                     args=(backtests_notebooks_to_interact.iloc[i + 3], sys.argv[1],))
                notebook_4.start()
            if i + 4 < backtests_notebooks_to_interact.count():
                notebook_5 = Process(target=run_notebook,
                                     args=(backtests_notebooks_to_interact.iloc[i + 4], sys.argv[1],))
                notebook_5.start()

            if i < backtests_notebooks_to_interact.count():
                notebook_1.join()
            if i + 1 < backtests_notebooks_to_interact.count():
                notebook_2.join()
            if i + 2 < backtests_notebooks_to_interact.count():
                notebook_3.join()
            if i + 3 < backtests_notebooks_to_interact.count():
                notebook_4.join()
            if i + 4 < backtests_notebooks_to_interact.count():
                notebook_5.join()

        for i in range(0, training_notebooks_to_interact.count(), 5):
            if i < training_notebooks_to_interact.count():
                notebook_1 = Process(target=run_notebook,
                                     args=(training_notebooks_to_interact[i], sys.argv[1],))
                notebook_1.start()
            if i + 1 < training_notebooks_to_interact.count():
                notebook_2 = Process(target=run_notebook,
                                     args=(training_notebooks_to_interact[i + 1], sys.argv[1],))
                notebook_2.start()
            if i + 2 < training_notebooks_to_interact.count():
                notebook_3 = Process(target=run_notebook,
                                     args=(training_notebooks_to_interact[i + 2], sys.argv[1],))
                notebook_3.start()
            if i + 3 < training_notebooks_to_interact.count():
                notebook_4 = Process(target=run_notebook,
                                     args=(training_notebooks_to_interact[i + 3], sys.argv[1],))
                notebook_4.start()
            if i + 4 < training_notebooks_to_interact.count():
                notebook_5 = Process(target=run_notebook,
                                     args=(training_notebooks_to_interact[i + 4], sys.argv[1],))
                notebook_5.start()

            if i < training_notebooks_to_interact.count():
                notebook_1.join()
            if i + 1 < training_notebooks_to_interact.count():
                notebook_2.join()
            if i + 2 < training_notebooks_to_interact.count():
                notebook_3.join()
            if i + 3 < training_notebooks_to_interact.count():
                notebook_4.join()
            if i + 4 < training_notebooks_to_interact.count():
                notebook_5.join()

    else:
        # if num_of_pending_backtests.count() > 0 and num_of_pending_backtests.iloc[0] > 0:
        #     print('Pending backtests: ', num_of_pending_backtests.iloc[0])
        #     if num_of_backtests_running.count() > 0:
        #         print('Num of Backtests running: ', num_of_backtests_running.iloc[0])
        #         if num_of_backtests_running.iloc[0] < 100 and num_of_backtests_running.iloc[0] < num_of_pending_backtests.iloc[0]:
        #             if sys.argv[1].lower() == 'run':
        #                 for i in range(num_of_backtests_running.iloc[0], 100, 5):
        #                     if i < backtests_notebooks_to_run.count():
        #                         notebook_1 = Process(target=run_notebook, args=(backtests_notebooks_to_run[i], sys.argv[1],))
        #                         notebook_1.start()
        #                     if i + 1 < backtests_notebooks_to_run.count():
        #                         notebook_2 = Process(target=run_notebook,
        #                                              args=(backtests_notebooks_to_run[i + 1], sys.argv[1],))
        #                         notebook_2.start()
        #                     if i + 2 < backtests_notebooks_to_run.count():
        #                         notebook_3 = Process(target=run_notebook,
        #                                              args=(backtests_notebooks_to_run[i + 2], sys.argv[1],))
        #                         notebook_3.start()
        #                     if i + 3 < backtests_notebooks_to_run.count():
        #                         notebook_4 = Process(target=run_notebook,
        #                                              args=(backtests_notebooks_to_run[i + 3], sys.argv[1],))
        #                         notebook_4.start()
        #                     if i + 4 < backtests_notebooks_to_run.count():
        #                         notebook_5 = Process(target=run_notebook,
        #                                              args=(backtests_notebooks_to_run[i + 4], sys.argv[1],))
        #                         notebook_5.start()
        #
        #                     if i < backtests_notebooks_to_run.count():
        #                         notebook_1.join()
        #                     if i + 1 < backtests_notebooks_to_run.count():
        #                         notebook_2.join()
        #                     if i + 2 < backtests_notebooks_to_run.count():
        #                         notebook_3.join()
        #                     if i + 3 < backtests_notebooks_to_run.count():
        #                         notebook_4.join()
        #                     if i + 4 < backtests_notebooks_to_run.count():
        #                         notebook_5.join()
        #     else:
        #         if sys.argv[1].lower() == 'run':
        #             for i in range(0, num_of_pending_backtests.iloc[0], 5):
        #                 if i < num_of_pending_backtests.iloc[0]:
        #                     notebook_1 = Process(target=run_notebook, args=(backtests_notebooks_to_run[i], sys.argv[1],))
        #                     notebook_1.start()
        #                 if i + 1 < num_of_pending_backtests.iloc[0]:
        #                     notebook_2 = Process(target=run_notebook,
        #                                          args=(backtests_notebooks_to_run[i + 1], sys.argv[1],))
        #                     notebook_2.start()
        #                 if i + 2 < num_of_pending_backtests.iloc[0]:
        #                     notebook_3 = Process(target=run_notebook,
        #                                          args=(backtests_notebooks_to_run[i + 2], sys.argv[1],))
        #                     notebook_3.start()
        #                 if i + 3 < num_of_pending_backtests.iloc[0]:
        #                     notebook_4 = Process(target=run_notebook,
        #                                          args=(backtests_notebooks_to_run[i + 3], sys.argv[1],))
        #                     notebook_4.start()
        #                 if i + 4 < num_of_pending_backtests.iloc[0]:
        #                     notebook_5 = Process(target=run_notebook,
        #                                          args=(backtests_notebooks_to_run[i + 4], sys.argv[1],))
        #                     notebook_5.start()
        #
        #                 if i < num_of_pending_backtests.iloc[0]:
        #                     notebook_1.join()
        #                 if i + 1 < num_of_pending_backtests.iloc[0]:
        #                     notebook_2.join()
        #                 if i + 2 < num_of_pending_backtests.iloc[0]:
        #                     notebook_3.join()
        #                 if i + 3 < num_of_pending_backtests.iloc[0]:
        #                     notebook_4.join()
        #                 if i + 4 < num_of_pending_backtests.iloc[0]:
        #                     notebook_5.join()
        # else:
        #     print('No backtest tasks pending')

        if num_of_pending_training_tasks.count() > 0 and num_of_pending_training_tasks.iloc[0] > 0:
            print('Number of Training Tasks pending ', num_of_pending_training_tasks.iloc[0])
            if num_of_training_tasks_running.count() > 0:
                print('Number of Running Training Tasks ', num_of_training_tasks_running.iloc[0])
                if num_of_training_tasks_running.iloc[0] < 100:
                    if sys.argv[1].lower() == 'run':
                        for i in range(num_of_training_tasks_running.iloc[0], 100, 5):
                            if i < training_notebooks_to_run.count():
                                notebook_1 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[i], sys.argv[1],))
                                notebook_1.start()
                            if i + 1 < training_notebooks_to_run.count():
                                notebook_2 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[i + 1], sys.argv[1],))
                                notebook_2.start()
                            if i + 2 < training_notebooks_to_run.count():
                                notebook_3 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[i + 2], sys.argv[1],))
                                notebook_3.start()
                            if i + 3 < training_notebooks_to_run.count():
                                notebook_4 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[i + 3], sys.argv[1],))
                                notebook_4.start()
                            if i + 4 < training_notebooks_to_run.count():
                                notebook_5 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[i + 4], sys.argv[1],))
                                notebook_5.start()

                            if i < training_notebooks_to_run.count():
                                notebook_1.join()
                            if i + 1 < training_notebooks_to_run.count():
                                notebook_2.join()
                            if i + 2 < training_notebooks_to_run.count():
                                notebook_3.join()
                            if i + 3 < training_notebooks_to_run.count():
                                notebook_4.join()
                            if i + 4 < training_notebooks_to_run.count():
                                notebook_5.join()
            else:
                if sys.argv[1].lower() == 'run':
                    for i in range(0, 50, 5):
                        if i < training_notebooks_to_run.count():
                            notebook_1 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[i], sys.argv[1],))
                            notebook_1.start()
                        if i + 1 < training_notebooks_to_run.count():
                            notebook_2 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[i + 1], sys.argv[1],))
                            notebook_2.start()
                        if i + 2 < training_notebooks_to_run.count():
                            notebook_3 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[i + 2], sys.argv[1],))
                            notebook_3.start()
                        if i + 3 < training_notebooks_to_run.count():
                            notebook_4 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[i + 3], sys.argv[1],))
                            notebook_4.start()
                        if i + 4 < training_notebooks_to_run.count():
                            notebook_5 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[i + 4], sys.argv[1],))
                            notebook_5.start()

                        if i < training_notebooks_to_run.count():
                            notebook_1.join()
                        if i + 1 < training_notebooks_to_run.count():
                            notebook_2.join()
                        if i + 2 < training_notebooks_to_run.count():
                            notebook_3.join()
                        if i + 3 < training_notebooks_to_run.count():
                            notebook_4.join()
                        if i + 4 < training_notebooks_to_run.count():
                            notebook_5.join()
        else:
            print('No training tasks pending')
