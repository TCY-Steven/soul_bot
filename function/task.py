import discord
from discord.ext import commands
from classes import Cog_Extension
from datetime import datetime, timedelta, timezone
from replit import db
import asyncio
import json
import time

with open("boss.json", "r", encoding="utf8") as f:
    boss = json.load(f)


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0
        '''
        async def interval():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(997535621184761876)
            while not self.bot.is_closed():
                await self.channel.send("HIIIIII~~~~~")
                await asyncio.sleep(5)  # seconds

        self.int_task = self.bot.loop.create_task(interval())
        '''

        async def time_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1003677200400269363)
            while not self.bot.is_closed():
                dt = datetime.utcnow().replace(tzinfo=timezone.utc)
                now_time = dt.astimezone(timezone(timedelta(hours=8)))
                week_day = now_time.weekday()
                HM = now_time.strftime("%H%M")
                try:
                    guild = self.bot.get_guild(289481126760939520)
                    role = guild.get_role(1003322198058086510)
                    boss_now = boss[str(week_day)][HM]
                    await self.channel.send(f"{role.mention} 五分鐘後出世界王 ： {boss_now}")
                except KeyError:
                    pass

                # Update each hour
                if HM[2:] == "00":
                    soul_db = db["soul_db"]
                    BG_channel = self.bot.get_channel(1012028546060931164)
                    await BG_channel.send(f"Update coin per hour.")
                    for s in soul_db:
                        if soul_db[s]["connect_now"] == "join":

                            daily_coin = soul_db[s]["daily_coin"]
                            if daily_coin < 120:
                                add_coin = int((time.time() - soul_db[s]["join_time"]) / 180)
                                daily_coin += add_coin
                                if daily_coin > 120:
                                    add_coin = add_coin - (daily_coin - 120)
                                soul_db[s]["daily_coin"] = daily_coin
                            else:
                                add_coin = 0

                            soul_db[s]["soul_coin"] += add_coin
                            soul_db[s]["join_time"] = time.time()
                            soul_db[s]["leave_time"] = time.time()
                            soul_db[s]["connection_time"] = 0
                            await BG_channel.send(f"<:love:586814470005719050> Update: {soul_db[s]['name']} ")
                            await BG_channel.send(f"current coins: {soul_db[s]['soul_coin']} ")
                            await BG_channel.send(f"Daily coins: {soul_db[s]['daily_coin']} ")
                            await BG_channel.send(f"Daily msg: {soul_db[s]['msg_num']} ")

                    db["soul_db"] = soul_db
                    await BG_channel.send(f"Update finished.")

                    db["bot_off"] = time.time()

                # Reset daily max
                if HM == "0000":
                    soul_db = db["soul_db"]
                    for member in soul_db.keys():
                        soul_db[member]["msg_num"] = 0
                        soul_db[member]["daily_coin"] = 0
                    db["soul_db"] = soul_db

                await asyncio.sleep(60)

        self.time_task = self.bot.loop.create_task(time_task())


def setup(bot):
    bot.add_cog(Task(bot))

