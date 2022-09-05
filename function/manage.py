import discord
from discord.ext import commands
from classes import Cog_Extension
from replit import db
import time


class manage(Cog_Extension):
    @commands.command()
    @commands.is_owner()
    @commands.cooldown(per=1, rate=10)
    async def ping(self, ctx):
        await ctx.send(self.bot.latency)

    @commands.command()
    @commands.is_owner()
    async def emoji_list(self, ctx):
        with open('emoji.txt', 'w') as f:
            for emo in self.bot.emojis:
                f.write(str(emo))
                f.write('\n')
        await ctx.send('<:100:586814506731175958>finished')

    @commands.command()
    @commands.is_owner()
    async def print_cog(self, ctx):
        for com in ctx.bot.cogs["Main"].get_commands():
            await ctx.send(com.name)

    @commands.command()
    @commands.is_owner()
    async def soul_member(self, ctx, reset=False):
        if ctx.guild.id == 289481126760939520:
            role_baby = ctx.guild.get_role(489467687571947551)
            soulmember = role_baby.members
            if reset:
                member_dict= {}
                for s in soulmember:
                    tmp_dict = {}
                    tmp_dict["name"] = s.name
                    tmp_dict["connection_time"] = 0
                    tmp_dict["soul_coin"] = 0
                    tmp_dict["daily_coin"] = 0
                    tmp_dict["join_time"] = time.time()
                    tmp_dict["leave_time"] = time.time()
                    tmp_dict["msg_num"] = 0
                    tmp_dict["prev_msg"] = 0
                    tmp_dict["connect_now"] = ""
                    member_dict[s.id] = tmp_dict
                db["soul_db"] = member_dict
                await ctx.send("Reset all member data finished.")
            else:
                soul_db = db["soul_db"]
                # print(soul_json.keys())
                for s in soulmember:
                    if str(s.id) not in soul_db.keys():
                        tmp_dict = {}
                        tmp_dict["name"] = s.name
                        tmp_dict["connection_time"] = 0
                        tmp_dict["soul_coin"] = 0
                        tmp_dict["daily_coin"] = 0
                        tmp_dict["join_time"] = time.time()
                        tmp_dict["leave_time"] = time.time()
                        tmp_dict["msg_num"] = 0
                        tmp_dict["prev_msg"] = 0
                        tmp_dict["connect_now"] = ""
                        soul_db[s.id] = tmp_dict
                        print(f'Add new member {tmp_dict}')
                db["soul_db"] = soul_db

    @commands.command()
    @commands.is_owner()
    async def add_param(self, ctx, param):
        if ctx.guild.id == 289481126760939520:
            param = str(param)
            soul_db = db["soul_db"]
            for s in soul_db:
                soul_db[s][param] = 0
            db["soul_db"] = soul_db

    @commands.command()
    @commands.is_owner()
    async def reset_member(self, ctx, member):
        soul_db = db["soul_db"]
        soul_db.pop(str(member), None)
        await ctx.send(f'Member :{member} data reset.')
        try:
            soul_db[str(member)]
        except KeyError:
            await ctx.send(f'Double check member data reset finished')
            db["soul_db"] = soul_db

    @commands.command()
    async def add_member(self, ctx):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id and ctx.guild.id == 289481126760939520:
            role_baby = ctx.guild.get_role(489467687571947551)
            soulmember = role_baby.members
            soul_db = db["soul_db"]
            # print(soul_json.keys())
            for s in soulmember:
                if str(s.id) not in soul_db.keys():
                    tmp_dict = {}
                    tmp_dict["name"] = s.name
                    tmp_dict["connection_time"] = 0
                    tmp_dict["soul_coin"] = 0
                    tmp_dict["daily_coin"] = 0
                    tmp_dict["join_time"] = time.time()
                    tmp_dict["leave_time"] = time.time()
                    tmp_dict["msg_num"] = 0
                    tmp_dict["prev_msg"] = 0
                    tmp_dict["connect_now"] = ""
                    soul_db[s.id] = tmp_dict
                    print(f'Add new member {tmp_dict}')
                    await ctx.send(f'Add new member {s.name} success')
            db["soul_db"] = soul_db
            await ctx.send('Member database update finished.')

    @commands.command()
    async def member_time(self, ctx, Mid):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            soul_db = db["soul_db"]
            await ctx.send(
                f'Join time: {soul_db[str(Mid)]["join_time"]}, leave time: {soul_db[str(Mid)]["leave_time"]}'
            )

    @commands.command()
    async def member_coin(self, ctx, Mid):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            soul_db = db["soul_db"]
            await ctx.send(
                f'Coin: {soul_db[str(Mid)]["soul_coin"]}'
            )

    @commands.command()
    @commands.is_owner()
    async def set_coin(self, ctx, Mid, num):
        db["soul_db"][str(Mid)]["soul_coin"] = int(num)
        await ctx.send(f'User {Mid} coin number set to {num}.')

def setup(bot):
    bot.add_cog(manage(bot))