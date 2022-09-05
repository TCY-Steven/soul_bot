import discord
from discord.ext import commands
from classes import Cog_Extension
from datetime import datetime, timedelta, timezone
import random
import json
import asyncio
import time
import gc
from replit import db


class cmds(Cog_Extension):
    @commands.command()
    async def formula(self, ctx):
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
        embed = discord.Embed(
            title="配方大全",
            url=
            "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vS7Oy5AJBhqm5unk1YvQT9zw-7QF0VOXc-g1grRulydSGB9IIuJlfL1ufkeir-8YXvde8Cqhp9Gcjs0/pubhtml#",
            description="料理煉金配方大全！",
            timestamp=dt2)
        embed.set_thumbnail(
            url=
            "https://s1.pearlcdn.com/TR/Upload/WIKI/7ae6e23773820171103151522913.jpg"
        )
        embed.add_field(name="料理", value="材料總整理", inline=True)
        embed.add_field(name="煉金", value="材料總整理", inline=True)
        embed.set_footer()
        await ctx.send(embed=embed)

    # 正式開始
    @commands.command()
    async def 世界王(self, ctx):
        with open('boss.json', 'r', encoding='utf8') as f:
            boss = json.load(f)
        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        now_time = dt.astimezone(timezone(timedelta(hours=8)))
        week_day = now_time.weekday()
        HM = now_time.strftime('%H%M')
        tmp = []
        for n in boss[str(week_day)].keys():
            tmp.append(int(n))
        try:
            near_time = min([x for x in tmp if x >= int(HM)])
        except ValueError:
            near_time = '0155'
            week_day += 1
        near_time = str(near_time).zfill(4)
        boss_now = boss[str(week_day)][near_time]
        await ctx.send(f'下一波世界王是：{boss_now}')

    @commands.command()
    async def 骰子(self, ctx):
        # print(self.bot.emojis)  # show all emojis name and id
        emoji = await ctx.guild.fetch_emoji(851330890184917052)
        await ctx.send(
            f'{emoji} {ctx.author.mention} 你抽到的數字是 {random.choice(range(1, 29))}'
        )

    @commands.command()
    async def 數字(self, ctx):
        # print(self.bot.emojis)  # show all emojis name and id
        emoji = await ctx.guild.fetch_emoji(851330890184917052)
        await ctx.send(
            f'{emoji} {ctx.author.mention} 你抽到的數字是 {random.choice(range(1, 29))}'
        )

    @commands.command()
    async def 分流(self, ctx):
        server_list = [
            '卡爾佩恩-1', '卡爾佩恩-2', '卡爾佩恩-3', '巴雷諾斯-1', '巴雷諾斯-2', '巴雷諾斯-3',
            '卡瑪希爾比亞-1', '卡瑪希爾比亞-2', '卡瑪希爾比亞-3', '梅迪亞-1', '梅迪亞-2', '梅迪亞-3',
            '瓦倫西亞-1', '瓦倫西亞-2', '瓦倫西亞-3', '賽林迪亞-1', '賽林迪亞-2', '賽林迪亞-3',
            '艾裴莉雅-1', '艾裴莉雅-2', '艾裴莉雅-3', '璐璐飛-1', '璐璐飛-2', '阿勒沙'
        ]
        emoji = await ctx.guild.fetch_emoji(586597752448745494)
        await ctx.send(
            f'{emoji} {ctx.author.mention} 你抽到的分流是 {random.choice(server_list)}'
        )

    @commands.command()
    async def 鎮魂幣說明(self, ctx):
        await ctx.send('鎮魂幣 - 是在鎮魂交響歌 Discord 伺服器可取得的一種幣，其單位為”果“ ')
        await ctx.send('用途：可透過幣來獲得各種好康～(正在規劃中...)')
        await ctx.send('如何獲得：')
        await ctx.send('1. 透過進入鎮魂DC語音頻道聊天可獲得，每3分鐘可獲得1果，離開語音頻道或每個整點會進行結算更新，每日取得上限為120果，等同於在線6小時')
        await ctx.send('2. 透過加入文字頻道聊天可以獲得，每個聊天訊息可獲得2果，每日取得上限為200果，每則訊息間隔超過一定時間方有效')

    @commands.command()
    async def 鎮魂幣(self, ctx):
        coins = db["soul_db"][str(ctx.author.id)]["soul_coin"]
        await ctx.send('{} 你在鎮魂交響歌 Discord 取得的鎮魂幣有：{:,}果'.format(ctx.author.mention, coins))

    @commands.command()
    async def 鎮魂幣查詢(self, ctx, member):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            coins = db["soul_db"][str(ctx.message.mentions[0].id)]["soul_coin"]
            await ctx.send('{} 在鎮魂交響歌 Discord 取得的鎮魂幣有：{:,}果'.format(member, coins))
        else:
            await ctx.send('查詢功能目前僅開放管理員使用，非常抱歉～')

    @commands.command()
    async def 鎮魂幣TOP(self, ctx):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            await ctx.send('現在公佈擁有最多鎮魂幣前五名的會員：')
            member_coin = []
            # start = time.time()
            soul_db = db["soul_db"]
            for s in soul_db.keys():
                gc.disable()
                member_coin.append([soul_db[s]["name"], soul_db[s]["soul_coin"]])
                gc.enable()
            # print(f'spend time {time.time() - start}')
            # print(member_coin)
            member_coin = sorted(member_coin, key=lambda s: s[1], reverse=True)
            top = 5
            for t in range(top):
                await asyncio.sleep(1)
                await ctx.send(f'第 {t + 1} 名的是 {member_coin[t][0]} 擁有 {member_coin[t][1]} 果')
        else:
            await ctx.send('此功能目前僅開放管理員使用，非常抱歉～')

    @commands.command()
    async def 消費(self, ctx, member, cost: int):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            if db["soul_db"][str(ctx.message.mentions[0].id)]["soul_coin"] < abs(cost):
                await ctx.send(f'{member} 鎮魂幣餘額不足...')
            else:
                db["soul_db"][str(ctx.message.mentions[0].id)]["soul_coin"] -= abs(cost)
                await ctx.send('{} 本次消費：{:,}果'.format(member, abs(cost)))
        else:
            await ctx.send('消費功能目前僅開放管理員使用，非常抱歉～')

    @commands.command()
    async def 賽馬說明(self, ctx):
        await ctx.send("此賽馬依彩池制進行，馬兒身心狀況會影響賠率以及勝率～")

    @commands.command()
    async def 賽馬開始(self, ctx):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            horse_race = db["horse_race"]
            if horse_race["mode"] == 1:
                await ctx.send("有賽馬正在進行中...")
            else:
                with open("horse.json", "r", encoding="utf8") as f:
                    horse = json.load(f)
                health = [horse["good_health"], horse["normal_health"], horse["bad_health"]]
                health_mag = [0.8, 1, 1.2]
                horse_pick = random.sample(horse["horse_list"], 10)
                horse_dict = {}
                await ctx.send("此賽馬依彩池制進行，馬兒身心狀況會影響賠率以及勝率～")
                for i in range(len(horse_pick)):
                    health_status = random.choice(range(len(health)))
                    health_adj = random.choice(health[health_status])
                    tmp_dict = {}
                    tmp_dict["name"] = horse_pick[i]
                    tmp_dict["health_adj"] = health_adj
                    tmp_dict["health_mag"] = health_mag[health_status]
                    # tmp_dict["init_odds"] = random.randrange(25, 31)/20 * health_mag[health_status]
                    tmp_dict["odds"] = 0
                    tmp_dict["bet"] = 0
                    tmp_dict["betby"] = {}

                    horse_dict[i] = tmp_dict
                    await ctx.send(
                        f'背號第 {i + 1} 號為 {health_adj} {horse_pick[i]} 初始賠率為{health_mag[health_status] * 1.25}')
                await ctx.send('初始賠率僅供參考，確切賠率將依投注情況浮動變化')
                db["horse"] = horse_dict
                horse_race = {}
                horse_race["start_time"] = time.time()
                horse_race["mode"] = 1
                horse_race["total_bet"] = 0
                db["horse_race"] = horse_race

    @commands.command()
    async def 賽馬查詢(self, ctx):
        mode = db["horse_race"]["mode"]
        if mode:
            horse_dict = db["horse"]
            for i in range(len(horse_dict)):
                await ctx.send(
                    f'背號第 {i + 1} 號為 {horse_dict[str(i)]["health_adj"]} {horse_dict[str(i)]["name"]} 賠率為{horse_dict[str(i)]["odds"]:.2f}')
        else:
            await ctx.send("沒有賽馬活動正在進行中唷...")

    @commands.command()
    async def 投注查詢(self, ctx):
        mode = db["horse_race"]["mode"]
        if mode:
            horse_dict = db["horse"]
            await ctx.send(f"{ctx.author.mention} 你目前投注情況：")
            for i in range(len(horse_dict)):
                bet_coin = horse_dict[str(i)]["betby"].get(str(ctx.author.id), False)
                if bet_coin:
                    await ctx.send(f"背號第 {i + 1} 號 {horse_dict[str(i)]['name']} 共投注 {bet_coin} 果")
        else:
            await ctx.send("沒有賽馬活動正在進行中唷...")

    @commands.command()
    async def 賽馬下注(self, ctx, which: int, pics: int):
        pic_price = 100
        coins = db["soul_db"][str(ctx.author.id)]["soul_coin"]
        which -= 1
        horse_race = db["horse_race"]
        if horse_race["mode"] == 1:
            if coins < pic_price * pics:
                await ctx.send(f"{ctx.author.mention} 很抱歉您的鎮魂幣不足...")
            else:
                horse_dict = db["horse"]

                horse_dict[str(which)]["bet"] += pic_price * pics
                horse_race["total_bet"] += pic_price * pics
                coins -= pic_price * pics
                if ctx.author in horse_dict[str(which)]["betby"].keys():
                    horse_dict[str(which)]["betby"][ctx.author.id] += pic_price * pics
                else:
                    horse_dict[str(which)]["betby"][ctx.author.id] = pic_price * pics
                for h in horse_dict:
                    if horse_dict[h]["bet"] != 0:
                        odds = (horse_race["total_bet"] - horse_dict[h]["bet"]) / horse_dict[h]["bet"] * horse_dict[h][
                            "health_mag"] + 1
                    else:
                        odds = 0
                    horse_dict[h]["odds"] = odds
                db["horse"] = horse_dict
                db["horse_race"] = horse_race
                db["soul_db"][str(ctx.author.id)]["soul_coin"] = coins
                await ctx.send(
                    f"{ctx.author.mention} 您已完成投注，投注對象為：{horse_dict[str(which)]['name']}, 共購買 {pics} 張, 花費 {pic_price * pics} 果")
        else:
            await ctx.send("沒有賽馬活動正在進行中唷...")

    @commands.command()
    async def 賽馬結束(self, ctx):
        manage_member = ctx.guild.get_role(489404444551806976).members
        manage_id = []
        for id in manage_member:
            manage_id.append(id.id)
        if ctx.author.id in manage_id:
            mode = db["horse_race"]["mode"]
            if mode:
                horse_dict = db["horse"]
                total_bet = db["horse_race"]["total_bet"]
                win_list = []
                for i in range(len(horse_dict)):
                    try:
                        win_rate = int(total_bet / horse_dict[str(i)]["bet"] / horse_dict[str(i)]["health_mag"])
                    except ZeroDivisionError:
                        win_rate = 0
                    # print(win_rate)
                    tmp_win = [i] * win_rate
                    win_list.extend(tmp_win)
                win_no = random.choice(win_list)
                final_odds = (total_bet - horse_dict[str(win_no)]["bet"]) / horse_dict[str(win_no)]["bet"] * \
                             horse_dict[str(win_no)]["health_mag"] + 1
                await ctx.send(f'本次賽馬獲勝的是 {horse_dict[str(win_no)]["health_adj"]} {horse_dict[str(win_no)]["name"]}')
                await ctx.send(f"最終賠率為 {final_odds:.2f}")
                soul_db = db["soul_db"]
                for who in horse_dict[str(win_no)]["betby"]:
                    win_coin = int(horse_dict[str(win_no)]["betby"][str(who)] * final_odds)
                    soul_db[str(who)]["soul_coin"] += win_coin
                    member = ctx.guild.get_member(int(who))
                    await ctx.send(f"恭喜 {member.mention} 獲得 {win_coin} 果")
                db["soul_db"] = soul_db
                db["horse_race"]["mode"] = 0
                db["horse_race"]["total_bet"] = 0
            else:
                await ctx.send(f"沒有賽馬活動正在進行中唷...")

    @commands.command()
    async def 職業(self, ctx, init=False):
        if init and ctx.author.id == 289823362837118976:
            quiz_dict = {}
            quiz_dict["mode"] = 0
            quiz_dict["question"] = 1
            quiz_dict["member"] = 0
            quiz_dict["time"] = 0
            quiz_dict["ans"] = ''
            db["quiz"] = quiz_dict
            with open("class.json", "r", encoding="utf8") as f:
                question_dict = json.load(f)
            db["class_ques"] = question_dict
        else:
            if db["quiz"]["mode"] == 0:
                db["quiz"]["mode"] = 1
                db["quiz"]["member"] = ctx.author.id
                db["quiz"]["time"] = time.time()
                await ctx.send('鎮魂交響歌 - 職業測驗開始啦～')
                await ctx.send('測驗即將開始，倒數5秒鐘！')
                await ctx.send('54321')
                await asyncio.sleep(1)
                await ctx.send('START!!!')
                await asyncio.sleep(1)
                await ctx.send(db["class_ques"][str(db["quiz"]["question"])]["question"])
                await asyncio.sleep(1)
                for an in db["class_ques"][str(db["quiz"]["question"])]["ans"]:
                    await ctx.send(an)

            elif db["quiz"]["mode"] == 1:
                await ctx.send('還有人在進行測驗中，稍等不要插隊唷～')

    @commands.command()
    async def 艾針(self, ctx, init=False):
        if ctx.guild.id == 289481126760939520:
            if init:
                with open('numbers.txt', 'r') as f:
                    num = f.read()
                db["needle_num"] = int(num)
            else:
                num = db["needle_num"]
                if num <= 1000:
                    await ctx.send(f'你問的是敏敏打不到的那個艾針嗎？你已經問了{num}次...')
                else:
                    await ctx.send(f'你已經問了{num}次, 敏敏也該打到了...')
                num += 1
                db["needle_num"] = num

    @commands.command()
    async def 風貓大小(self, ctx):
        if ctx.guild.id == 289481126760939520:
            await ctx.send('蹲到桌下去你就會知道了<:catcat:586800314871447563>')

    @commands.command()
    async def 據點(self, ctx):
        await ctx.send(
            'https://docs.google.com/spreadsheets/d/1HqGHROLdnm9pR872NKnuOg5qO79Ch-79DYPvQM83TSk/edit#gid=701677756'
        )

    @commands.command()
    async def 小秘訣(self, ctx, inp):
        if '牛' in inp or '圖魯' in inp or '屯克塔' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/880420345184682034/17032d8714f9beb110187f0a62196935.png'
            )
            await ctx.send(
                'https://forum.gamer.com.tw/C.php?bsn=19017&snA=57032&tnum=1')
        elif '黑洞' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/873613427145343006/unknown.png'
            )
        elif '豬' in inp or '半獸' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/882903932664418324/ae96cc5756afd51c9b9d81b999964236.png'
            )
        elif '針' in inp:
            await ctx.send('廢墟-波杜肯/艾爾敦/杜卡路巴特恩, 寺廟-亞克曼菁英守護者')
            await ctx.send(
                'https://lh3.googleusercontent.com/B5Jema0ZP37ILV2WMv4O5pTT9pl4UOrxY71Q7-9liLwNdEh7USWOiY5vT7g4Ev3pO4cm_XgvqmJQabhLcoe3e5LZbFLG3_PSK0CwvLEx3-Ciq79qpOTulmWCs1GTw6kez0wR85B5Cg_NjXXHErxEvg=w403-h154'
            )
        elif '地圖' in inp:
            await ctx.send('火山-熔岩族精英掠食者/熔岩族掠食者, 監獄-鐵拳典獄長/卑劣流放者')
            await ctx.send(
                'https://lh5.googleusercontent.com/ORZkp1sCpvpQHEWV6fHwbdYmP7OhmwsfRkIf4Oel4fhJhsk9MHWlQ-ws1bpxs-SqDAwCwCxqr_jQX4GZ8uX0XYeT5XcUdszHMe6hBJFi38rFGIanNRiUP4ShUNr5GdOcREeNh9pAiQTjuzCJyuHEcA=w403-h171'
            )
        elif '配方' in inp or '料理' in inp or '煉金' in inp:
            dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
            dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
            embed = discord.Embed(
                title="配方大全",
                url=
                "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vS7Oy5AJBhqm5unk1YvQT9zw-7QF0VOXc-g1grRulydSGB9IIuJlfL1ufkeir-8YXvde8Cqhp9Gcjs0/pubhtml#",
                description="料理煉金配方大全！",
                timestamp=dt2)
            embed.set_thumbnail(
                url=
                "https://s1.pearlcdn.com/TR/Upload/WIKI/7ae6e23773820171103151522913.jpg"
            )
            embed.add_field(name="料理", value="材料總整理", inline=True)
            embed.add_field(name="煉金", value="材料總整理", inline=True)
            embed.set_footer()
            await ctx.send(embed=embed)
        elif '紅水' in inp or '洪水' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/1003669208342736946/1a715bbf61020210914121506790.jpg'
            )
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/1003669265154592810/6f103ba5f5d20210914151109058.jpg'
            )
        elif '藍水' in inp or '蘭水' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/1003669243943981197/6d27ec2ffaf20210914121454416.jpg'
            )
        elif '永久水' in inp:
            await ctx.send('請在小秘訣後輸入你要查詢的是紅水或藍水～')
        elif '東飾品' in inp or '東勢' in inp or '飾品' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/884475370542334043/V20210804.png'
            )
            await ctx.send(
                'https://forum.gamer.com.tw/C.php?bsn=19017&snA=55926')
        elif '東王裝' in inp or '王裝' in inp or '東裝' in inp or '東王' in inp or '東王莊' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564537608699904/895904333093302272/unknown.png'
            )
            await ctx.send(
                'https://forum.gamer.com.tw/C.php?bsn=19017&snA=57207&tnum=29')
        elif '光明' in inp:
            await ctx.send(
                'https://www.tw.playblackdesert.com/Wiki?wikiNo=656#光明石組合條件與效果'
            )
        elif '王' in inp:
            await ctx.send(
                'https://cdn.discordapp.com/attachments/586564281840041995/731509124692574258/bef65ac63e33d5a68d5c42b0300be687.png'
            )
        else:
            await ctx.send('小秘訣沒有這個內容唷，需要增加內容請聯絡風貓～')


def setup(bot):
    bot.add_cog(cmds(bot))
