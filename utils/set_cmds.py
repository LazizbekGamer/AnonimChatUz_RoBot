import requests
from loader import db, bot, dp
from data import config



TOKEN = config.BOT_TOKEN

async def set_cmds(dp):
    print("\n\033[91m\033[1mThe bot has been launched!\n \033[97m")
    command_api_url = f'https://api.telegram.org/bot{TOKEN}/setMyCommands'
    commands = [
        {'command': 'start', 'description': '💠 Botni ishga tushirish'},
        {'command': 'accaunt', 'description': '👤 Accaunt'},
        {'command': 'help', 'description': '🆘 Yordam'},
        {'command': 'admin', 'description': '👮‍♂️ Admin Panel'},
        {'command': 'dev', 'description': '👨‍💻 Dasturchi'},
    ]

    response = requests.post(command_api_url, json={'commands': commands})
    if response.status_code == 200:
        print('\033[94m\033[1mBot commands set successfully! \n \n\033[93mBot Logs:\033[97m')
    else:
        print('\n\033[91mError: Bot commands not set\n \n\033[97m')