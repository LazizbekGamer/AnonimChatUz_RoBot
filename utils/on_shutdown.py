from .notify_admins import on_shutdown_notify
import os
from loader import *



async def on_shutdown(dp):
    await on_shutdown_notify(dp)
    await dp.storage.close()
    await dp.storage.wait_closed()
    dp.stop_polling()
