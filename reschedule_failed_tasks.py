import psycopg2
import datetime as dt

# def update_error_session_closed(connection):
#     query_to_use = """update task_manager_queue
#                         set queue_state='New' , queue_status = 'Waiting For Task Manager'
#                         where experiment_id in (
#                         select experiment_id from task_manager_queue
#                         where  (queue_type='BackTestTask' or queue_type = 'TrainingTask') and queue_state='Failed' and
#                         task_start_time::date > (now()-interval '1 day')::date
#                              and extract(epoch from (now()- task_heartbeat_time ))/60 > 15
#                         and (queue_status = 'Error Session Closed'))"""
#     curr = connection.cursor()
#     curr.execute(query_to_use)
#     curr.close()


def update_error_session_closed(connection):
    query_to_use = """update task_manager_queue 
                      set queue_state = (%s), queue_status = (%s),
                      created_by = (%s) 
                      where experiment_id in (
                        select experiment_id from task_manager_queue 
                        where (queue_type = 'BackTestTask' or queue_type = 'TrainingTask')
                        and queue_state = 'Failed' 
                        and task_start_time >= now() - interval '1 Day'
                        and queue_status = 'Error Session Closed')"""

    curr = connection.cursor()
    curr.execute(query_to_use,
                 ('New',
                  'Waiting For Task Manager',
                  'Error Session Closed reset by Colab Manager at ' + str(dt.datetime.utcnow())))
    print(curr.rowcount)
    connection.commit()
    curr.close()


def set_backtest_master_done_to_New(connection):
    curr = connection.cursor()
    curr.execute("""update task_manager_queue
                    set queue_state = 'New' , queue_status='Waiting For Task Manager'
                    where queue_type='BackTestMaster' and queue_state = 'Done' and  parent_exp_id IN 
                    (select distinct parent_exp_id from task_manager_queue
                    where queue_type = 'BackTestTask' and queue_state='New')""")
    print(curr.rowcount)
    connection.commit()
    curr.close()


def set_training_master_done_to_new(connection):
    curr = connection.cursor()
    curr.execute("""update task_manager_queue set
                    queue_state = 'New', 
                    queue_status = 'Waiting For Task Manager' where
                    queue_type = 'TrainingMaster' and
                    queue_state = 'Done' and 
                    parent_exp_id in 
                    (select distinct
                    parent_exp_id from task_manager_queue where 
                    queue_type = 'TrainingTask' and
                    queue_state = 'New')""")
    print(curr.rowcount)
    connection.commit()
    curr.close()


if __name__ == '__main__':
    conn = psycopg2.connect(dbname='greencanvas',
                            user='gcp_read_only',
                            password='gc$$2929%',
                            host='35.223.254.139',
                            port=5432)

    update_error_session_closed(conn)

    set_backtest_master_done_to_New(conn)
    set_training_master_done_to_new(conn)
    conn.close()
