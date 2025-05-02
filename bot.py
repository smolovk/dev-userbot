from pyrogram import Client
from dotenv import load_dotenv
import psutil
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def command_chatid(_client, message):
    await message.edit(message.chat.id)

async def command_eval(_client, message):
    expr = message.text.replace(".eval", "")
    await message.edit(eval(expr))

async def command_reply_test(_client, message):
    print(message)
    await message.edit("asdf")

async def command_stats(_client, message):
    res = []
    res.append(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

    mem = psutil.virtual_memory()
    res.append(f"Memory usage: {mem.percent}%")
    await message.edit("\n".join(res))

commands = {
    "chatid": command_chatid,
    # "eval": command_eval,
    "reply_test": command_reply_test,
    "stats": command_stats
}

@app.on_message()
async def my_handler(_client, message):
    if  not message.from_user or not message.from_user.is_self or not message.text:
        return

    text = message.text

    if text.startswith("."):
        for c in commands.keys():
            if text[1:].startswith(c):
                await commands[c](_client, message)


print("running...")
app.run()
print("shit")
