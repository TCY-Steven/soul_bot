import os
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp
import json
import time
#import replNeverSleep
#import keep_alive


#replNeverSleep.awake('https://'+str(os.environ['REPL_SLUG']).lower()+'.'+str(os.environ['REPL_OWNER']).lower()+'.repl.co', True)


intents = discord.Intents.default()
# intents.typing = False
intents.members = True

menu = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌", active_time=30)
bot = commands.Bot(command_prefix='!', intents=intents)

bot.help_command = PrettyHelp(menu=menu, color=discord.Colour.red())


@bot.event
async def on_ready():
    soul_db = db["soul_db"]
    for s in soul_db:
        soul_db[s]["join_time"] = time.time()
        if soul_db[s]["connect_now"] == "join":
            daily_coin = soul_db[s]["daily_coin"]
            if daily_coin < 120:
                add_coin = int((time.time() - db["bot_off"])/180)
                daily_coin += add_coin
                if daily_coin > 120:
                    add_coin = add_coin - (daily_coin - 120)
                soul_db[s]["daily_coin"] = daily_coin
            else:
                add_coin = 0
            soul_db[s]["soul_coin"] += add_coin
    db["soul_db"] = soul_db
    print("Bot is online.")


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'function.{extension}')
    await ctx.send(f'Loaded {extension} success')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'function.{extension}')
    await ctx.send(f'Unloaded {extension} success')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f'function.{extension}')
    await ctx.send(f'Reloaded {extension} success')


'''
@bot.command()
async def ping(ctx):
    await ctx.send(bot.latency)
'''

for filename in os.listdir('./function'):
    if filename.endswith('.py'):
        #print('Loading')
        bot.load_extension(f'function.{filename[:-3]}')


if __name__ == "__main__":
    # keep_alive.keep_alive()
    # bot.run(jset['TOKEN'])
    try:
        bot.run(os.environ['TOKEN'])
    except:
        os.system("kill 1")


'''
[
<Emoji id=997527304920104980 name='ghost' animated=False managed=False>, 
<Emoji id=997527364638625912 name='moon' animated=False managed=False>, 
<Emoji id=586587492803805234 name='BD' animated=False managed=False>, 
<Emoji id=586597752448745494 name='money' animated=False managed=False>, 
<Emoji id=586600718165606412 name='butterfly' animated=False managed=False>, 
<Emoji id=586800280184815627 name='OK' animated=False managed=False>, 
<Emoji id=586800314871447563 name='catcat' animated=False managed=False>, 
<Emoji id=586814420634697728 name='cry' animated=False managed=False>, 
<Emoji id=586814470005719050 name='love' animated=False managed=False>, 
<Emoji id=586814506731175958 name='100' animated=False managed=False>, 
<Emoji id=586814577765777408 name='lol' animated=False managed=False>, 
<Emoji id=586982931403112448 name='cheers' animated=False managed=False>, 
<Emoji id=586982968979881985 name='punch' animated=False managed=False>, 
<Emoji id=586983033173704723 name='robot' animated=False managed=False>, 
<Emoji id=586984077018791936 name='cheer' animated=False managed=False>, 
<Emoji id=586994111303647242 name='angry' animated=False managed=False>, 
<Emoji id=586994177900937216 name='sleep' animated=False managed=False>, 
<Emoji id=586994226491949113 name='gift' animated=False managed=False>, 
<Emoji id=586994248373501967 name='bath' animated=False managed=False>, 
<Emoji id=586994273698840585 name='boxing' animated=False managed=False>, 
<Emoji id=586994295123476491 name='swim' animated=False managed=False>, 
<Emoji id=589094834933989394 name='PKM1' animated=False managed=False>, 
<Emoji id=589095126345842710 name='PKM2' animated=False managed=False>, 
<Emoji id=589098084584259595 name='PKM3' animated=False managed=False>, 
<Emoji id=589104201917792277 name='PKM4' animated=False managed=False>, 
<Emoji id=589104225691238411 name='PKM5' animated=False managed=False>, 
<Emoji id=589110106717814797 name='PKM6' animated=False managed=False>, 
<Emoji id=589110127903244309 name='PKM7' animated=False managed=False>, 
<Emoji id=589110148627300355 name='PKM8' animated=False managed=False>, 
<Emoji id=589117965161725956 name='PKM9' animated=False managed=False>, 
<Emoji id=589117984702857246 name='PKM10' animated=False managed=False>, 
<Emoji id=589118003497402397 name='PKM11' animated=False managed=False>, 
<Emoji id=589136068641816616 name='sleep' animated=False managed=False>, 
<Emoji id=602847726065156116 name='e04' animated=False managed=False>, 
<Emoji id=602854804447821824 name='heart' animated=False managed=False>, 
<Emoji id=701447975469318261 name='mushroom' animated=False managed=False>, 
<Emoji id=701460285541842996 name='kappi' animated=False managed=False>, 
<Emoji id=701464970487136306 name='LALA' animated=False managed=False>, 
<Emoji id=701761408127467530 name='Kappo_cry' animated=False managed=False>, 
<Emoji id=701761433913786471 name='Kappo_love' animated=False managed=False>, 
<Emoji id=701764208563454054 name='pig' animated=False managed=False>, 
<Emoji id=701764235281301624 name='lili' animated=False managed=False>, 
<Emoji id=845679487764529222 name='BD2' animated=False managed=False>, 
<Emoji id=850428097374453763 name='duck' animated=False managed=False>, 
<Emoji id=851330890184917052 name='qua' animated=False managed=False>, 
<Emoji id=852805856494878731 name='rabbit' animated=False managed=False>, 
<Emoji id=853172313268551692 name='someone' animated=False managed=False>, 
<Emoji id=853174745557762048 name='kabo' animated=True managed=False>, 
<Emoji id=853213936147759154 name='monster1' animated=False managed=False>, 
<Emoji id=854954325482143754 name='BD_cry' animated=True managed=False>, 
<Emoji id=855471655483473940 name='BD_cola' animated=True managed=False>, 
<Emoji id=855471676124299295 name='BD_cold' animated=True managed=False>, 
<Emoji id=855471694734557196 name='BD_happy' animated=True managed=False>, 
<Emoji id=855471724665765919 name='BD_lemon' animated=True managed=False>, 
<Emoji id=855471764964638741 name='BD_love' animated=True managed=False>, 
<Emoji id=855471788585385994 name='BD_pull' animated=True managed=False>, 
<Emoji id=855471810887417916 name='BD_punch' animated=True managed=False>, 
<Emoji id=855471831385636884 name='BD_que' animated=True managed=False>, 
<Emoji id=855471849404366858 name='BD_seek' animated=True managed=False>, 
<Emoji id=867067036244770856 name='blackcat_small' animated=True managed=False>, 
<Emoji id=883722212044070933 name='dog' animated=False managed=False>, 
<Emoji id=888263647527325777 name='peng1' animated=False managed=False>, 
<Emoji id=914752223106441256 name='Rich' animated=False managed=False>, 
<Emoji id=915512606423392266 name='BD3' animated=False managed=False>
]

'''


