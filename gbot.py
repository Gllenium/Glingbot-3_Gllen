#-*- coding: utf-8 -*-

"""Discord bot by Dev.Gllenium"""

import discord, asyncio, os, sqlite3, re, ast, time, psutil
from discord.ext import commands

con = sqlite3.connect('./Premium_list.db')
cur = con.cursor()
cur.execute('SELECT * FROM Premium')
premium_ALL = cur.fetchall()
premium_ID=[]
premium_Grade=[]
con.close()
for i in premium_ALL:
    premium_ID.append(i[0])
    premium_Grade.append(i[1])


print(premium_ID)
print(premium_Grade)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents,command_prefix="*")
token = ""


async def bt(games):
    await bot.wait_until_ready()
    while not bot.is_closed():
        for g in games:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game(g))
            await asyncio.sleep(60)

async def check_em(ctx,embed):
    print(str(ctx.author.id))
    if str(ctx.author.id) in premium_ID:
        embed.color=0xD358F7
        if ctx.author.avatar!=None:
            embed.set_footer(icon_url=ctx.author.avatar, text=f'{ctx.author} ({premium_Grade[premium_ID.index(str(ctx.author.id))]})')
        else:
            embed.set_footer(text=f'{ctx.author} ({premium_Grade[premium_ID.index(str(ctx.author.id))]})')
        return embed
    else:
        if ctx.author.avatar!=None:
            embed.set_footer(icon_url=ctx.author.avatar, text='{}'.format(ctx.author))
        else:
            embed.set_footer(text='{}'.format(ctx.author))
        return embed

async def restart():
    global con,cur,con1,cur1
    con1.close()
    try:
        await bot.close()
    except:
        pass
    time.sleep(5)
    os.system('python3 gbot.py')

async def off():
    con1.close()
    await bot.close()

@bot.event
async def on_ready():
    os.system('echo \033[32mBot Online\033[0m')
    os.system('echo \033[34m{}\033[0m'.format(bot.user.name))
    os.system('echo \033[34m{}\033[0m'.format(bot.user.id))
    os.system('echo \033[35m================\033[0m')
    await bt(['Gbot ver.3.1.8 Gllen', 'Code Remake, Refactoring', "SQL Update", "24h Server"])


@bot.slash_command(description="관리자 전용 기능")
async def command(ctx, prompt: discord.commands.Option(str, "command")):
    if not int(ctx.author.id)==599740489801138197:
        embed = discord.Embed(title="Error: Uncertified", description="인증되지 않은 접근", color=0xFF0000)
        await ctx.respond(embed=embed,ephemeral=True)
        return
    
    if prompt == "reboot" or prompt == "restart":
        embed = discord.Embed(title="Bot: Rebooting...", color=discord.Colour.red())
        await ctx.respond(embed=embed)
        await restart()
        await bot.close()
        return
    
    if prompt == "off":
        embed = discord.Embed(title="Bot: Logout", color=discord.Colour.red())
        await ctx.respond(embed=embed)
        await off()
        return

    if prompt[0:4] == "pre+" or prompt[0:4] =="Pre+":
        sp=prompt.split(' ')
        try:
            grade = sp[2]
        except:
            grade = "Premium"
        print("pre+ command input")
        print(re.sub(r'[^0-9]', '', sp[1]))
        sp=int(re.sub(r'[^0-9]', '', sp[1]))
        target_user=await bot.fetch_user(sp)
        if str(target_user.id) in premium_ID:
            embed = discord.Embed(title="Gllen Premium : ERROR", description="이미 등록된 유저입니다.", color=discord.Colour.red())
            embed.add_field(name=f"User Information", value=f"```ansi\nUser : \033[36m{target_user.name}\033[0m\nID : \033[33m{sp}\033[0m```", inline=False)
            embed.add_field(name=f"Grade",value=f"```fix\nGllen {premium_Grade[premium_ID.index(str(target_user.id))]}```", inline=False)
            await check_em(ctx,embed)
            await ctx.respond(embed=embed)
            return

        con = sqlite3.connect('./Premium_list.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Premium VALUES("{}", "{}")'.format(sp, grade))
        con.commit()
        con.close()

        embed = discord.Embed(title="Gllen Premium : Register", description="<:Gllen:1086672769409888436>Glslen Premium User List에 등록합니다.", color=0xD358F7)
        embed.add_field(name=f"User Information", value=f"```ansi\nUser : \033[36m{target_user.name}\033[0m\nID : \033[33m{sp}\033[0m```", inline=False)
        embed.add_field(name=f"Grade",value=f"```fix\nGllen {grade}```", inline=False)
        if ctx.author.avatar!=None:
            embed.set_footer(icon_url=ctx.author.avatar, text='{} (Bot Developer)'.format(ctx.author))
        else:
            embed.set_footer(text='{} (Bot Developer)'.format(ctx.author))
        await ctx.respond(embed=embed)
        return
    

    if prompt[0:4] == "pre-" or prompt[0:4] == "Pre-":
        sp=prompt.split(' ')
        print("pre- command input")
        print(re.sub(r'[^0-9]', '', sp[1]))
        sp=int(re.sub(r'[^0-9]', '', sp[1]))
        con = sqlite3.connect('./Premium_list.db')
        cur = con.cursor()
        cur.execute(f'DELETE FROM Premium WHERE ID = {sp}')
        con.commit()
        con.close()

        target_user=await bot.fetch_user(sp)
        embed = discord.Embed(title="Gllen Premium : Delete", description="<:Gllen:1086672769409888436>Gllen Premium User List에서 제거합니다..", color=0xD358F7)
        embed.add_field(name=f"User Information", value=f"```ansi\nUser : \033[36m{target_user.name}\033[0m\nID : \033[33m{sp}\033[0m```", inline=False)
        # embed.add_field(name=f"Deleted Grade",value=f"```fix\nGllen {select[1]}```", inline=False)
        if ctx.author.avatar!=None:
            embed.set_footer(icon_url=ctx.author.avatar, text='{} (Bot Developer)'.format(ctx.author))
        else:
            embed.set_footer(text='{} (Bot Developer)'.format(ctx.author))
        await ctx.respond(embed=embed)
        return
    


    code=prompt.replace(";","\n")
    def insert_returns(body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].sbody)
            insert_returns(body[-1].orelse)

        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    print("\n{}\n{}\n".format(code,ctx.author))
    cmd = code.split(" ")

    msg = await ctx.respond(embed = discord.Embed(title='Code Compiling <a:loading:1076164295898959982>').add_field(
        name='📥 Input',
        value=f'```py\n{code}```',
        inline=False
    ))#,ephemeral=True
    await asyncio.sleep(1)

    #banword checking
    banword = ['token', 'file=', 'file =', 'exit()', 'api_key']

    if code in banword:
        embed = discord.Embed(title='Code Compiling')
        embed.add_field(name='📥 Input', value=f'```py\n{code}```', inline=False)
        embed.add_field(name = '📤 Output', value = f'jsk에서 사용 금지된 단어가 포함되어 있습니다.')
        await msg.edit_original_message(embed=embed)
        return None
    else:
        try:
            ccode = code
            cmd = ccode
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'bot': bot,
                'discord': discord,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = await eval(f"{fn_name}()", env)
            embed=discord.Embed(title="Python Code Compiling: Succeed", colour=discord.Colour.green())
            embed.add_field(name="`📥 Input Prompt 📥`", value=f"```py\n{ccode}```", inline=False)
            embed.add_field(name="`📤 Output Prompt 📤`", value=f"```py\n{result}```", inline=False)
            embed.add_field(name="`🔧 Type 🔧`",value=f"```py\n{type(result)}```", inline=False)
            # embed=await check_em(ctx,embed)
            await msg.edit_original_message(embed = embed)
        except Exception as e:
            embed = discord.Embed(title='Python Code Compiling: Exception', colour=discord.Colour.red())
            embed.add_field(name='📥 Input', value=f'```py\n{code}```', inline=False)
            embed.add_field(name = '📤 Output', value = f'{e}')
            await msg.edit_original_message(embed=embed)


@bot.slash_command(description="메세지 삭제")
async def 삭제(ctx, 수 : discord.commands.Option(int, "삭제할 메세지 수")):
    if not (ctx.author.guild_permissions.manage_messages) and not ctx.author==await bot.fetch_user(599740489801138197):
        await ctx.respond("메세지 관리 권한이 없습니다.",ephemeral=True)
        return
    num=수
    embee = discord.Embed(title="Message Deleting: Deleting...", description="Deleting message : {}개".format(num))
    embee=await check_em(ctx,embee)
    await ctx.respond(embed=embee,ephemeral=True)
    await ctx.channel.purge(limit=num,bulk=True)
    embed = discord.Embed(title="Message Deleting: Deleted", description="Deleted message : {}개".format(num))
    embed=await check_em(ctx,embed)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Gllen Status")
async def status(ctx):
    pong=str(round(bot.latency*1000))
    embed = discord.Embed(title="Gllen Status")
    embed.add_field(
        name=f"Bot Information",
        value=f"```ansi\nClient : \033[36m{bot.user.name}#{bot.user.discriminator}\033[0m\nPing : \033[33m{pong + 'ms'}\033[0m\nCPU Usage : \033[36m{psutil.cpu_percent()}%\033[0m\nMemory Usage : \033[33m{psutil.virtual_memory().percent}%\033[0m```",
        inline=False
        )
    embed=await check_em(ctx,embed)
    await ctx.respond(embed=embed)

@bot.slash_command(name="시즌", description="잠깐만 사용할 이터널리턴 시즌 조회")
async def season(ctx):
    headers = {'x-api-key': 'AGTDWidtsB53qnAYDTV9p4BCGMTBYzPh8YunGuxt'}
    url = (f"https://open-api.bser.io/v2/data/Season")
    response = requests.get(url, headers= headers)
    jj=eval(response.content.decode("utf-8"))
    embed = discord.Embed(title="Season List", description="이터널 리턴 시즌 리스트\n일반적인 공개보다 1주정도 먼저 업데이트됨")
    for i in range(len(jj['data'])):
        if int(jj['data'][i]['seasonID'])>=18:
            embed.add_field(name=f"ID: {jj['data'][i]['seasonID']} ㅣ (정규){jj['data'][i]['seasonName'][:-2]} {int(jj['data'][i]['seasonName'][-2:])-9}",value=f"{jj['data'][i]['seasonStart']} ~ {jj['data'][i]['seasonEnd']}",inline=False)
        else:
            embed.add_field(name=f"ID: {jj['data'][i]['seasonID']} ㅣ {jj['data'][i]['seasonName']}",value=f"{jj['data'][i]['seasonStart']} ~ {jj['data'][i]['seasonEnd']}")
    await ctx.respond(embed=embed)

bot.run(token)

