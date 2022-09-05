import discord
from discord.ext import commands
from classes import Cog_Extension
from replit import db
import random
import asyncio
import time


class event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, msg):
        '''
        if '交易' in msg.content and msg.author != self.bot.user:
            if msg.content.startswith('!') is False:
                await msg.channel.send('幹你的交易所壞掉')
        '''
        msg_channel = [
            624647819957108750,  # 鎮魂尬廣
            993158172044959845,  # 副本卷軸
            849625484416516107,  # 裝備健檢
            1002145346870329415  # 前世今生
            # 1003320850784727120  #機器人
        ]
        if str(msg.author.id) in db["soul_db"].keys() and msg.channel.id in msg_channel:
            max_msg = 100
            msg_now = time.time()
            time_interval = random.randint(30, 90)
            if (msg_now - db["soul_db"][str(msg.author.id)]["prev_msg"]) / time_interval >= 1:
                db["soul_db"][str(msg.author.id)]["prev_msg"] = msg_now
                if db["soul_db"][str(msg.author.id)]["msg_num"] <= max_msg:
                    db["soul_db"][str(msg.author.id)]["soul_coin"] += 2
                    db["soul_db"][str(msg.author.id)]["msg_num"] += 1

        if db["quiz"]["mode"] == 1:
            msg_ans = msg.content.upper()
            if msg.author.id == db["quiz"]["member"] and msg_ans in "ABCD":
                db["quiz"]["ans"] += msg_ans  # get the answer from user
                db["quiz"]["question"] += 1  # next question
                if db["quiz"]["question"] > len(db["class_ques"]):
                    await msg.channel.send("職業測驗結束～")
                    await msg.channel.send(db["quiz"]["ans"])
                    db["quiz"]["mode"] = 0
                    db["quiz"]["question"] = 1
                    db["quiz"]["ans"] = ''
                    db["quiz"]["member"] = 0
                else:
                    await msg.channel.send(db["class_ques"][str(db["quiz"]["question"])]["question"])
                    await asyncio.sleep(1)
                    for an in db["class_ques"][str(db["quiz"]["question"])]["ans"]:
                        await msg.channel.send(an)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        respond_list = [
            '不要玩我好嗎<:e04:602847726065156116>', '沒有這個指令啦',  # '九陶是渣男', '敏敏肝很黑'
            '是不是忘了在前面加小秘訣？', '不要鬧了～', '喔齁 又輸入錯囉!'
        ]

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Missing argument.")
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(random.choice(respond_list))
        elif isinstance(error, commands.errors.CommandError):
            await ctx.send("Sorry, you dont have permission.")
        else:
            await ctx.send("Error occur.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1003678281305964584:
            if str(payload.emoji) == "<:mushroom:701447975469318261>":
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(1003322198058086510)
                await payload.member.add_roles(role)
                # await payload.member.send("You got the role.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1003678281305964584:
            if str(payload.emoji) == "<:mushroom:701447975469318261>":
                guild = self.bot.get_guild(payload.guild_id)
                user = await guild.fetch_member(payload.user_id)
                role = guild.get_role(1003322198058086510)
                await user.remove_roles(role)
                # await user.send("You remove the role.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if str(member.id) in db["soul_db"].keys():
            print(member)
            print(member.id)

            channel = self.bot.get_channel(1012028546060931164)

            connect_server = [
                853678452674527242,  # 鎮魂寶寶說話
                796033848692703253,  # 鎮魂寶寶聊天
                964905633210060871,  # 鎮魂打副本區
                1006211312126263367,  # 鎮魂其他遊戲
                1001030083793928243  # 鎮魂射槍槍區
            ]
            # print(before.self_deaf)
            # print(before.self_mute)
            # print(after.self_deaf)
            # print(after.self_mute)
            try:
                connect_bf = before.channel.id
            except AttributeError:
                connect_bf = None
            try:
                connect_af = after.channel.id
            except AttributeError:
                connect_af = None

            connect_condition = None
            channel_connect = None

            if (
                    connect_bf == None or connect_bf == 289487195381694465 or connect_bf == 610126264899993600) and connect_af in connect_server:
                channel_connect = 'join'
            elif connect_bf in connect_server and (
                    connect_af == None or connect_af == 289487195381694465 or connect_af == 610126264899993600):
                channel_connect = 'leave'

            if channel_connect == "join" and after.self_deaf == False:
                connect_condition = 'join'
            elif channel_connect == None and after.self_deaf == True:
                connect_condition = 'leave'
            elif channel_connect == None and after.self_deaf == False and before.self_deaf == True:
                connect_condition = 'join'
            elif channel_connect == None and after.self_deaf == False:
                connect_condition = None
            elif channel_connect == 'leave' and after.self_deaf == False:
                connect_condition = 'leave'
            elif channel_connect == 'leave' and after.self_deaf == True:
                connect_condition = None

            print(connect_condition)

            soul_db = db["soul_db"]

            if connect_condition == 'join':
                now = time.time()
                soul_db[str(member.id)]["join_time"] = now

                await channel.send(f'<:BD3:915512606423392266> Member: {member}')
                await channel.send(f'Member id: {member.id}')
                await channel.send(f'Connect condition: {connect_condition}')
                await channel.send(f'Join time: {time.ctime(now + 28800)}')

                soul_db[str(member.id)]["connect_now"] = connect_condition

            elif connect_condition == 'leave':
                try:
                    now = time.time()
                    soul_db[str(member.id)]["leave_time"] = now
                    soul_db[str(member.id)]["connection_time"] = soul_db[str(member.id)]["leave_time"] - \
                                                                 soul_db[str(member.id)]["join_time"]

                    daily_coin = soul_db[str(member.id)]["daily_coin"]
                    if daily_coin < 120:
                        add_coin = int(soul_db[str(member.id)]["connection_time"] / 180)
                        daily_coin += add_coin
                        if daily_coin > 120:
                            add_coin = add_coin - (daily_coin - 120)
                        soul_db[str(member.id)]["daily_coin"] = daily_coin
                    else:
                        add_coin = 0
                    soul_db[str(member.id)]["soul_coin"] += add_coin

                    soul_db[str(member.id)]["connection_time"] = 0

                    soul_db[str(member.id)]["connect_now"] = connect_condition

                    print(soul_db[str(member.id)]["soul_coin"])

                    await channel.send(f'<:BD3:915512606423392266> Member: {member}')
                    await channel.send(f'Member id: {member.id}')
                    await channel.send(f'Connect condition: {connect_condition}')
                    await channel.send(f'Leave time: {time.ctime(now + 28800)}')
                    await channel.send(f'Coin now: {soul_db[str(member.id)]["soul_coin"]}')
                    if daily_coin >= 120:
                        await channel.send('Daily coin reach the upper limit.')
                    else:
                        await channel.send(f'Daily coin now: {daily_coin}')
                except KeyError:
                    pass
            db["soul_db"] = soul_db


def setup(bot):
    bot.add_cog(event(bot))
