from actions_on_notebook import run_notebook
from multiprocessing import Queue

ret_val = Queue()
run_notebook('gctw5H', ret_val)
print('Status returned', ret_val.get())
