from loader import dp, db
from .notify_admins import on_start_notify
from .set_cmds import set_cmds
from .create_tables import create_table
import asyncio



async def update_custom_balance_task():
    while True:
        await asyncio.sleep(60) # Sleep for 24 hours
        db.update_custom_balance()




async def on_startup(dp):
	await set_cmds(dp)
	await on_start_notify(dp)
	await create_table(dp)
	asyncio.create_task(update_custom_balance_task())

    
