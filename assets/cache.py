import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def my_function():
    print("Running my function")
    await asyncio.sleep(2)
    print("Finished my function")


async def schedule(func, interval: int):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func, 'interval', seconds=interval)
    scheduler.start()

    # run forever
    while True:
        await asyncio.sleep(0)

# asyncio.run(schedule(my_function, 3))
