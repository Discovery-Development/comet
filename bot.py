#################################

# At first this bot is only available for the 'Discovery Development' guild.

#################################

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler # pip3 install apscheduler
import datetime

# configuration - later in config file:

token = "HIDDEN"
reminder_channel = 946764623837814854
trigger_user = 302050872383242240
trigger_content = "👍"
success_reaction = "🚀"
time_delta = 7260
ping_role = 946763389563195443
# end

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.listening, name="in development")
bot = discord.Bot(intents=intents, activity=activity)

scheduler = AsyncIOScheduler()
scheduler.start()

# message function when timer is expired
async def reminder():
    channel = bot.get_channel(reminder_channel)
    embed = discord.Embed(color=discord.Color.red(), title="New bump!", description="Please enter `!d bump` as soon as possible to support this server.")
    await channel.send(embed=embed, content=f"<@&{ping_role}>")

@bot.event
async def on_ready():
    # print a message when the bot is ready to use
    print("Bot logged in as {0} with the ID {0.id}".format(bot.user))

@bot.event
async def on_message(m):
    # event for checking every message
    if m.guild is None:
        return
    if m.embeds \
    and m.author.id == trigger_user \
    and trigger_content in m.embeds[0].description:
        await m.add_reaction(success_reaction)
        # get target time

        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(seconds=time_delta)



        scheduler.add_job(reminder, 'date', next_run_time=target_time)

bot.run(token)