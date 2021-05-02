from actions_on_notebook import run_notebook
from multiprocessing import Queue

ret_val = Queue()
run_notebook('gctw11E', ret_val)
print('Status returned', ret_val.get())