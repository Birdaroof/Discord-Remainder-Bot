from nextcord import Intents
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import datetime
import math

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("channel_id")

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name = "hi")
async def SendMessage(context):
    await context.send("Hello")

async def schedule_message():
    while True:
        now = datetime.datetime.now()
        then = now+datetime.timedelta(minutes=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = bot.get_channel(1233911974778109995)
        await channel.send("message")
        await asyncio.sleep(1)



@bot.command(name = "reminder")
async def reminder(context, message:str, timeframe:str, repeat_delay:float, repeat_amount:float):
    timeframe = timeframe.lower()
    now = datetime.datetime.now()
    then = datetime.timedelta(days =1)
    repeat_delay = int(math.floor(repeat_delay))
    repeat_amount = int(math.floor(repeat_amount))
    valid_timeframes = ["days", "hours", "minutes", "seconds"]
    if timeframe not in valid_timeframes:
        raise commands.BadArgument()
    #await context.send(f"Reminder has been set for every {repeat_delay} {timeframe}")
    if timeframe == "days":
        await context.send(f"Reminder has been set for every {repeat_delay} days\nReminder Message: \"{message}\"\nRepeating {repeat_amount} times\nConfirm by saying: 'yes'")

    elif timeframe == "hours":
        await context.send(f"Reminder has been set for every {repeat_delay} hours\nReminder Message: \"{message}\"\nRepeating {repeat_amount} times\nConfirm by saying: 'yes'")

    elif timeframe == "minutes":
        await context.send(f"Reminder has been set for every {repeat_delay} minutes\nReminder Message: \"{message}\"\nRepeating {repeat_amount} times\nConfirm by saying: 'yes'")

    elif timeframe == "seconds":
        await context.send(f"Reminder has been set for every {repeat_delay} seconds\nReminder Message: \"{message}\"\nRepeating {repeat_amount} times\nConfirm by saying: 'yes'")

    try:
       msg = await bot.wait_for("message", timeout=10, check = lambda message: message.author == context.author) 
    except asyncio.TimeoutError:
        await context.send("You took too long to respond! ")
        return
    
    if msg.content == "yes":
        await context.send(f"Reminder message has been set for every {repeat_delay} {timeframe}")
        while True:
            now = datetime.datetime.now()
            if timeframe == "days":
                then = now+datetime.timedelta(days=1)
            elif timeframe == "minutes":
                then = now+datetime.timedelta(minutes=1)
            elif timeframe == "seconds":
                then = now+datetime.timedelta(seconds=1)
            elif timeframe == "hours":
                then = now+datetime.timedelta(hours=1)
            wait_time = (then-now).total_seconds()
            await asyncio.sleep(wait_time)
            await context.send(message)
            await asyncio.sleep(1)
    else:
        await context.send("Reminder message cancelled")


    
@reminder.error
async def reminder_error(context, error):
    if isinstance(error, commands.BadArgument):
        await context.send("Please enter command in following format:\n !reminder \"message\" timeframe repeat_delay repeat_amount\n valid timeframes are: hours, days, minutes, seconds")

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    #await schedule_message()

if __name__ == "__main__":
    bot.run(token)
