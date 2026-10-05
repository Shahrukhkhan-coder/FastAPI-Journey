import time
from timeit import default_timer as timer


def run_task(name, second):
    print(f'{name} started at : {timer()}')
    time.sleep(second)
    print(f'{name} Completed at : {timer()}')



start = timer()
run_task('', 2)
run_task('', 1)
run_task('' ,3)

print(f'\nTotal time taken: {timer() - start:.2f} s')
