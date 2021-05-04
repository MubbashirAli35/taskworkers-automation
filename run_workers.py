import psycopg2
import pandas as pd
import datetime as dt
from multiprocessing import Process, Queue
import sys
from actions_on_notebook import run_notebook, ping_notebook, terminate_notebook_session

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

backtests_notebooks_to_interact = backtests_notebooks_to_interact['Notebook']
training_notebooks_to_interact = training_notebooks_to_interact['Notebook']

num_of_pending_backtests = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_pending_training_tasks = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']
num_of_pending_kmeans_tasks = tasks_queue.loc[(tasks_queue['Status'] == 'New') & (tasks_queue['Task Type'] == 'KmeansTask')]['Number']

num_of_backtests_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'BackTestTask')]['Number']
num_of_training_tasks_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'TrainingTask')]['Number']
num_of_kmeans_tasks_running = tasks_queue.loc[(tasks_queue['Status'] == 'Running') & (tasks_queue['Task Type'] == 'KmeansTask')]['Number']


if __name__ == '__main__':
    print(dt.datetime.now())
    print('\n\n')
    print(training_notebooks_to_run.count())

    if sys.argv[1].lower() == 'terminate':
        for i in range(0, backtests_notebooks_to_interact.count(), 5):
            if i < backtests_notebooks_to_interact.count():
                notebook_1 = Process(target=terminate_notebook_session, args=(backtests_notebooks_to_interact.iloc[i],))
                notebook_1.start()
            if i + 1 < backtests_notebooks_to_interact.count():
                notebook_2 = Process(target=terminate_notebook_session,
                                     args=(backtests_notebooks_to_interact.iloc[i + 1],))
                notebook_2.start()
            if i + 2 < backtests_notebooks_to_interact.count():
                notebook_3 = Process(target=terminate_notebook_session,
                                     args=(backtests_notebooks_to_interact.iloc[i + 2],))
                notebook_3.start()
            if i + 3 < backtests_notebooks_to_interact.count():
                notebook_4 = Process(target=terminate_notebook_session,
                                     args=(backtests_notebooks_to_interact.iloc[i + 3],))
                notebook_4.start()
            if i + 4 < backtests_notebooks_to_interact.count():
                notebook_5 = Process(target=terminate_notebook_session,
                                     args=(backtests_notebooks_to_interact.iloc[i + 4],))
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
                notebook_1 = Process(target=terminate_notebook_session,
                                     args=(training_notebooks_to_interact.iloc[i],))
                notebook_1.start()
            if i + 1 < training_notebooks_to_interact.count():
                notebook_2 = Process(target=terminate_notebook_session,
                                     args=(training_notebooks_to_interact.iloc[i + 1],))
                notebook_2.start()
            if i + 2 < training_notebooks_to_interact.count():
                notebook_3 = Process(target=terminate_notebook_session,
                                     args=(training_notebooks_to_interact.iloc[i + 2],))
                notebook_3.start()
            if i + 3 < training_notebooks_to_interact.count():
                notebook_4 = Process(target=terminate_notebook_session,
                                     args=(training_notebooks_to_interact.iloc[i + 3],))
                notebook_4.start()
            if i + 4 < training_notebooks_to_interact.count():
                notebook_5 = Process(target=terminate_notebook_session,
                                     args=(training_notebooks_to_interact.iloc[i + 4],))
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

    elif sys.argv[1].lower() == 'interact':
        for i in range(0, training_notebooks_to_interact.count(), 5):
            if i < training_notebooks_to_interact.count():
                notebook_1 = Process(target=ping_notebook,
                                     args=(training_notebooks_to_interact.iloc[i],))
                notebook_1.start()
            if i + 1 < training_notebooks_to_interact.count():
                notebook_2 = Process(target=ping_notebook,
                                     args=(training_notebooks_to_interact.iloc[i + 1],))
                notebook_2.start()
            if i + 2 < training_notebooks_to_interact.count():
                notebook_3 = Process(target=ping_notebook,
                                     args=(training_notebooks_to_interact.iloc[i + 2],))
                notebook_3.start()
            if i + 3 < training_notebooks_to_interact.count():
                notebook_4 = Process(target=ping_notebook,
                                     args=(training_notebooks_to_interact.iloc[i + 3],))
                notebook_4.start()
            if i + 4 < training_notebooks_to_interact.count():
                notebook_5 = Process(target=ping_notebook,
                                     args=(training_notebooks_to_interact.iloc[i + 4],))
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

        try:
            for i in range(0, backtests_notebooks_to_interact.count(), 5):
                if i < backtests_notebooks_to_interact.count():
                    notebook_1 = Process(target=ping_notebook, args=(backtests_notebooks_to_interact.iloc[i],))
                    notebook_1.start()
                if i + 1 < backtests_notebooks_to_interact.count():
                    notebook_2 = Process(target=ping_notebook,
                                         args=(backtests_notebooks_to_interact.iloc[i + 1],))
                    notebook_2.start()
                if i + 2 < backtests_notebooks_to_interact.count():
                    notebook_3 = Process(target=ping_notebook,
                                         args=(backtests_notebooks_to_interact.iloc[i + 2],))
                    notebook_3.start()
                if i + 3 < backtests_notebooks_to_interact.count():
                    notebook_4 = Process(target=ping_notebook,
                                         args=(backtests_notebooks_to_interact.iloc[i + 3],))
                    notebook_4.start()
                if i + 4 < backtests_notebooks_to_interact.count():
                    notebook_5 = Process(target=ping_notebook,
                                         args=(backtests_notebooks_to_interact.iloc[i + 4],))
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
        except:
            print('All running Backtest notebooks pinged')

    else:
        notebook_1_ret_val = Queue()
        notebook_2_ret_val = Queue()
        notebook_3_ret_val = Queue()
        notebook_4_ret_val = Queue()
        notebook_5_ret_val = Queue()
        notebooks_index = 0

        if num_of_pending_training_tasks.count() > 0 and num_of_pending_training_tasks.iloc[0] > 0  \
                and (sys.argv[2] == 'train' or sys.argv[2] == 'both'):
            print('Number of Training Tasks pending ', num_of_pending_training_tasks.iloc[0])
            if num_of_training_tasks_running.count() > 0:
                i = num_of_training_tasks_running.iloc[0]

                print('Number of Running Training Tasks ', num_of_training_tasks_running.iloc[0])
                if num_of_training_tasks_running.iloc[0] < num_of_pending_training_tasks.iloc[0]:
                    if sys.argv[1].lower() == 'run':
                        while i < num_of_pending_training_tasks:
                            if i < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                notebook_1 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[notebooks_index],
                                                           notebook_1_ret_val,))
                                notebook_1.start()
                            if i + 1 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                notebook_2 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[notebooks_index + 1],
                                                           notebook_2_ret_val,))
                                notebook_2.start()
                            if i + 2 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                notebook_3 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[notebooks_index + 2],
                                                           notebook_3_ret_val,))
                                notebook_3.start()
                            if i + 3 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                notebook_4 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[notebooks_index + 3],
                                                           notebook_4_ret_val,))
                                notebook_4.start()
                            if i + 4 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                notebook_5 = Process(target=run_notebook,
                                                     args=(training_notebooks_to_run[notebooks_index + 4],
                                                           notebook_5_ret_val,))
                                notebook_5.start()

                            if i < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                if notebook_1_ret_val.get() == 1:
                                    if i - 1 < num_of_training_tasks_running.iloc[0]:
                                        i = num_of_training_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_1.join()
                            if i + 1 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                if notebook_2_ret_val.get() == 1:
                                    if i - 1 < num_of_training_tasks_running.iloc[0]:
                                        i = num_of_training_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_2.join()
                            if i + 2 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                if notebook_3_ret_val.get() == 1:
                                    if i - 1 < num_of_training_tasks_running.iloc[0]:
                                        i = num_of_training_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_3.join()
                            if i + 3 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                if notebook_4_ret_val.get() == 1:
                                    if i - 1 < num_of_training_tasks_running.iloc[0]:
                                        i = num_of_training_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_4.join()
                            if i + 4 < num_of_pending_training_tasks.iloc[0] or \
                            i < num_of_training_tasks_running.iloc[0] + 5:
                                if notebook_5_ret_val.get() == 1:
                                    if i - 1 < num_of_training_tasks_running.iloc[0]:
                                        i = num_of_training_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_5.join()

                            notebooks_index += 5
                            i += 5
            else:
                notebook_1_ret_val = Queue()
                notebook_2_ret_val = Queue()
                notebook_3_ret_val = Queue()
                notebook_4_ret_val = Queue()
                notebook_5_ret_val = Queue()
                notebooks_index = 0
                i = 0

                if sys.argv[1].lower() == 'run':
                    while i < num_of_pending_training_tasks:
                        if i < num_of_pending_training_tasks.iloc[0] or i < 5:
                            notebook_1 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[notebooks_index],
                                                       notebook_1_ret_val,))
                            notebook_1.start()
                        if i + 1 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            notebook_2 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[notebooks_index + 1],
                                                       notebook_2_ret_val,))
                            notebook_2.start()
                        if i + 2 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            notebook_3 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[notebooks_index + 2],
                                                       notebook_3_ret_val,))
                            notebook_3.start()
                        if i + 3 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            notebook_4 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[notebooks_index + 3],
                                                       notebook_4_ret_val,))
                            notebook_4.start()
                        if i + 4 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            notebook_5 = Process(target=run_notebook,
                                                 args=(training_notebooks_to_run[notebooks_index + 4],
                                                       notebook_5_ret_val,))
                            notebook_5.start()

                        if i < num_of_pending_training_tasks.iloc[0] or i < 5:
                            if notebook_1_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 1

                            notebook_1.join()
                        if i + 1 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            if notebook_2_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 1

                            notebook_2.join()
                        if i + 2 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            if notebook_3_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 1

                            notebook_3.join()
                        if i + 3 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            if notebook_4_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 1

                            notebook_4.join()
                        if i + 4 < num_of_pending_training_tasks.iloc[0] or i < 5:
                            if notebook_5_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 1

                            notebook_5.join()

                        notebooks_index += 5
                        i += 5
        else:
            print('No training tasks pending')

        if num_of_pending_kmeans_tasks.count() > 0 and num_of_pending_kmeans_tasks.iloc[0] > 0 \
                and (sys.argv[2] == 'train' or sys.argv[2] == 'both'):
            notebook_1_ret_val = Queue()
            notebook_2_ret_val = Queue()
            notebook_3_ret_val = Queue()
            notebook_4_ret_val = Queue()
            notebook_5_ret_val = Queue()
            notebooks_index = 0

            print('Pending Kmeans Tasks: ', num_of_pending_kmeans_tasks.iloc[0])

            if num_of_kmeans_tasks_running.count() > 0:
                i = num_of_kmeans_tasks_running.iloc[0]
                print('Num of Kmeans Tasks running: ', num_of_kmeans_tasks_running.iloc[0])

                if num_of_kmeans_tasks_running.iloc[0] < num_of_pending_kmeans_tasks.iloc[0]:
                    if sys.argv[1].lower() == 'run':
                        while i < num_of_pending_kmeans_tasks:
                            if i < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                                notebook_1 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index],
                                                           notebook_1_ret_val,))
                                notebook_1.start()
                            if i + 1 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                                notebook_2 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 1],
                                                           notebook_2_ret_val,))
                                notebook_2.start()
                            if i + 2 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                                notebook_3 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 2],
                                                           notebook_3_ret_val,))
                                notebook_3.start()
                            if i + 3 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                                notebook_4 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 3],
                                                           notebook_4_ret_val,))
                                notebook_4.start()
                            if i + 4 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                                notebook_5 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 4],
                                                           notebook_5_ret_val,))
                                notebook_5.start()

                            if i < num_of_pending_kmeans_tasks.iloc[0]:
                                if notebook_1_ret_val.get() == 1:
                                    if i - 1 < num_of_kmeans_tasks_running.iloc[0]:
                                        i = num_of_kmeans_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_1.join()
                            if i + 1 < num_of_pending_kmeans_tasks.iloc[0]:
                                if notebook_2_ret_val.get() == 1:
                                    if i - 1 < num_of_kmeans_tasks_running.iloc[0]:
                                        i = num_of_kmeans_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_2.join()
                            if i + 2 < num_of_pending_kmeans_tasks.iloc[0]:
                                if notebook_3_ret_val.get() == 1:
                                    if i - 1 < num_of_kmeans_tasks_running.iloc[0]:
                                        i = num_of_kmeans_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_3.join()
                            if i + 3 < num_of_pending_kmeans_tasks.iloc[0]:
                                if notebook_4_ret_val.get() == 1:
                                    if i - 1 < num_of_kmeans_tasks_running.iloc[0]:
                                        i = num_of_kmeans_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_4.join()
                            if i + 4 < num_of_pending_kmeans_tasks.iloc[0]:
                                if notebook_5_ret_val.get() == 1:
                                    if i - 1 < num_of_kmeans_tasks_running.iloc[0]:
                                        i = num_of_kmeans_tasks_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_5.join()

                            notebooks_index += 5
                            i += 5
            else:
                if sys.argv[1].lower() == 'run':
                    notebook_1_ret_val = Queue()
                    notebook_2_ret_val = Queue()
                    notebook_3_ret_val = Queue()
                    notebook_4_ret_val = Queue()
                    notebook_5_ret_val = Queue()
                    notebooks_index = 0
                    i = 0

                    while i < num_of_pending_kmeans_tasks.iloc[0]:
                        if i < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            notebook_1 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index],
                                                       notebook_1_ret_val,))
                            notebook_1.start()
                        if i + 1 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            notebook_2 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 1],
                                                       notebook_2_ret_val,))
                            notebook_2.start()
                        if i + 2 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            notebook_3 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 2],
                                                       notebook_3_ret_val,))
                            notebook_3.start()
                        if i + 3 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            notebook_4 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 3],
                                                       notebook_4_ret_val,))
                            notebook_4.start()
                        if i + 4 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            notebook_5 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 4],
                                                       notebook_5_ret_val,))
                            notebook_5.start()

                        if i < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            if notebook_1_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_1.join()
                        if i + 1 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            if notebook_2_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_2.join()
                        if i + 2 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            if notebook_3_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_3.join()
                        if i + 3 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            if notebook_4_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_4.join()
                        if i + 4 < num_of_pending_kmeans_tasks.iloc[0] or i < 5:
                            if notebook_5_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_5.join()

                        notebooks_index += 5

                        if i == 0 and num_of_pending_kmeans_tasks <= 5:
                            i = 0
                        else:
                            i += 5
        else:
            print('No Kmeans tasks pending')

        if num_of_pending_backtests.count() > 0 and num_of_pending_backtests.iloc[0] > 0 \
                and (sys.argv[2] == 'backtest' or sys.argv[2] == 'both'):
            notebook_1_ret_val = Queue()
            notebook_2_ret_val = Queue()
            notebook_3_ret_val = Queue()
            notebook_4_ret_val = Queue()
            notebook_5_ret_val = Queue()

            if not num_of_pending_kmeans_tasks.count() > 0 and num_of_kmeans_tasks_running.count() > 0:
                notebooks_index = 0

            print('Pending backtests: ', num_of_pending_backtests.iloc[0])
            if num_of_backtests_running.count() > 0:
                i = num_of_backtests_running.iloc[0]
                print('Num of Backtests running: ', num_of_backtests_running.iloc[0])

                if num_of_backtests_running.iloc[0] < num_of_pending_backtests.iloc[0]:
                    if sys.argv[1].lower() == 'run':
                        while i < num_of_pending_backtests:
                            if i < num_of_pending_backtests.iloc[0] or i < 5:
                                notebook_1 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index],
                                                           notebook_1_ret_val,))
                                notebook_1.start()
                            if i + 1 < num_of_pending_backtests.iloc[0] or i < 5:
                                notebook_2 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 1],
                                                           notebook_2_ret_val,))
                                notebook_2.start()
                            if i + 2 < num_of_pending_backtests.iloc[0] or i < 5:
                                notebook_3 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 2],
                                                           notebook_3_ret_val,))
                                notebook_3.start()
                            if i + 3 < num_of_pending_backtests.iloc[0] or i < 5:
                                notebook_4 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 3],
                                                           notebook_4_ret_val,))
                                notebook_4.start()
                            if i + 4 < num_of_pending_backtests.iloc[0] or i < 5:
                                notebook_5 = Process(target=run_notebook,
                                                     args=(backtests_notebooks_to_run[notebooks_index + 4],
                                                           notebook_5_ret_val,))
                                notebook_5.start()

                            if i < num_of_pending_backtests.iloc[0]:
                                if notebook_1_ret_val.get() == 1:
                                    if i - 1 < num_of_backtests_running.iloc[0]:
                                        i = num_of_backtests_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_1.join()
                            if i + 1 < num_of_pending_backtests.iloc[0]:
                                if notebook_2_ret_val.get() == 1:
                                    if i - 1 < num_of_backtests_running.iloc[0]:
                                        i = num_of_backtests_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_2.join()
                            if i + 2 < num_of_pending_backtests.iloc[0]:
                                if notebook_3_ret_val.get() == 1:
                                    if i - 1 < num_of_backtests_running.iloc[0]:
                                        i = num_of_backtests_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_3.join()
                            if i + 3 < num_of_pending_backtests.iloc[0]:
                                if notebook_4_ret_val.get() == 1:
                                    if i - 1 < num_of_backtests_running.iloc[0]:
                                        i = num_of_backtests_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_4.join()
                            if i + 4 < num_of_pending_backtests.iloc[0]:
                                if notebook_5_ret_val.get() == 1:
                                    if i - 1 < num_of_backtests_running.iloc[0]:
                                        i = num_of_backtests_running.iloc[0]
                                    else:
                                        i -= 1

                                notebook_5.join()

                            notebooks_index += 5
                            i += 5
            else:
                if sys.argv[1].lower() == 'run':
                    notebook_1_ret_val = Queue()
                    notebook_2_ret_val = Queue()
                    notebook_3_ret_val = Queue()
                    notebook_4_ret_val = Queue()
                    notebook_5_ret_val = Queue()

                    if not num_of_pending_kmeans_tasks.count() > 0 and num_of_kmeans_tasks_running.count() > 0:
                        notebooks_index = 0

                    i = 0

                    while i < num_of_pending_backtests.iloc[0]:
                        if i < num_of_pending_backtests.iloc[0] or i < 5:
                            notebook_1 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index],
                                                       notebook_1_ret_val,))
                            notebook_1.start()
                        if i + 1 < num_of_pending_backtests.iloc[0] or i < 5:
                            notebook_2 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 1],
                                                       notebook_2_ret_val,))
                            notebook_2.start()
                        if i + 2 < num_of_pending_backtests.iloc[0] or i < 5:
                            notebook_3 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 2],
                                                       notebook_3_ret_val,))
                            notebook_3.start()
                        if i + 3 < num_of_pending_backtests.iloc[0] or i < 5:
                            notebook_4 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 3],
                                                       notebook_4_ret_val,))
                            notebook_4.start()
                        if i + 4 < num_of_pending_backtests.iloc[0] or i < 5:
                            notebook_5 = Process(target=run_notebook,
                                                 args=(backtests_notebooks_to_run[notebooks_index + 4],
                                                       notebook_5_ret_val,))
                            notebook_5.start()

                        if i < num_of_pending_backtests.iloc[0] or i < 5:
                            if notebook_1_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_1.join()
                        if i + 1 < num_of_pending_backtests.iloc[0] or i < 5:
                            if notebook_2_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_2.join()
                        if i + 2 < num_of_pending_backtests.iloc[0] or i < 5:
                            if notebook_3_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_3.join()
                        if i + 3 < num_of_pending_backtests.iloc[0] or i < 5:
                            if notebook_4_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_4.join()
                        if i + 4 < num_of_pending_backtests.iloc[0] or i < 5:
                            if notebook_5_ret_val.get() == 1:
                                if i - 1 < 0:
                                    i = 0
                                else:
                                    i -= 5

                            notebook_5.join()

                        notebooks_index += 5
                        i += 5
        else:
            print('No backtest tasks pending')
