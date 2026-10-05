import asyncio
from timeit import default_timer as timer


async def run_task(name, second):
    print(f'{name} started at : {timer()}')
    await asyncio.sleep(second)
    print(f'{name} Completed at : {timer()}')


async def main():
    start = timer()
    await asyncio.gather(
        run_task('', 2),
        run_task('', 1),
        run_task('' ,3)
    )

    print(f'\nTotal time taken: {timer() - start:.2f} s')

asyncio.run(main())