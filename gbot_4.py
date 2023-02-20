from pydoc import describe
import discord,re,ast,asyncio,os,calendar,datetime

bot = discord.Bot(command_prefix='>')
token = open("token.txt",'r+').readline()
premium_=[]
premium=[]

f = open("premium.txt", 'r+')
pr = f.readline()
premium_=pr.split(',')

del premium_[-1]
for i in premium_:
    premium.append(int(i))



import openai

openai.api_key = open("openaitoken.txt",'r').readline()


@bot.event
async def on_ready():
    os.system('echo \033[32mGllen Online\033[0m')
    os.system('echo \033[34m{}\033[0m'.format(bot.user.name))
    os.system('echo \033[34m{}\033[0m'.format(bot.user.id))
    os.system('echo \033[35m================\033[0m')
    await bot.change_presence(status=discord.Status.dnd)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Gllen 3.1.0 : SSH 24h server"))



@bot.slash_command(description="글렌의 핑을 출력")
async def 핑(ctx):
    global premium
    pong=str(round(bot.latency*1000))
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="Ping", description=pong + ' ms', color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
    else:
        embed = discord.Embed(title="Ping", description=pong + ' ms', color=0x00FF80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
    await ctx.respond(embed=embed)


@bot.slash_command(description="캘린더 출력")
async def 캘린더(ctx):
    global premium
    dt=datetime.datetime.now()
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="calendar", description="```py\n{}```".format(calendar.month(dt.year,dt.month)), color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
    else:
        embed = discord.Embed(title="calendar", description="```py\n{}```".format(calendar.month(dt.year,dt.month)), color=0x00FF80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
    await ctx.respond(embed=embed)


@bot.slash_command(description="자신의 프사 출력")
async def 내프사(ctx):
    global premium
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="프로필 사진", description='{}님의 프로필 사진입니다.'.format(ctx.author), color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
        embed.set_image(url=ctx.author.avatar)
    else:
        embed = discord.Embed(title="프로필 사진", description='{}님의 프로필 사진입니다.'.format(ctx.author), color=0x00FF80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author)
        embed.set_image(url=ctx.author.avatar)
    await ctx.respond(embed=embed)


@bot.slash_command(description="지정한 사람의 프사 출력")
async def 프사(ctx, id_또는_mention: discord.commands.Option(str, "id or @mention")):
    global premium
    try:
        sp=int(re.sub(r'[^0-9]', '', id_또는_mention))
        f_user=await bot.fetch_user(sp)
    except:
        await ctx.respond("존재하지 않는 id입니다.",ephemeral=True)
        return
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="프로필 사진", description='{}님의 프로필 사진입니다.'.format(f_user), color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
        embed.set_image(url=f_user.avatar)
    else:
        embed = discord.Embed(title="프로필 사진", description='{}님의 프로필 사진입니다.'.format(f_user), color=0x00FF80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author)
        embed.set_image(url=f_user.avatar)
    await ctx.respond(embed=embed)


@bot.slash_command(description="유저의 정보를 출력")
async def 정보(ctx, id_또는_mention: discord.commands.Option(str, "id or @mention")):
    global premium
    try:
        sp=int(re.sub(r'[^0-9]', '', id_또는_mention))
        f_user=await bot.fetch_user(sp)
    except:
        await ctx.respond("존재하지 않는 id입니다.",ephemeral=True)
        return
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="유저 정보", description="`{}`님의 정보입니다.".format(f_user.name), color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
    else:
        embed = discord.Embed(title="유저 정보", description="`{}`님의 정보입니다.".format(f_user.name), color=0x00ff80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
    embed.set_thumbnail(url=f_user.avatar)
    embed.add_field(name="이름(+태그)", value=f_user, inline=True)
    embed.add_field(name="계정 생성 시간", value=str(f_user.created_at), inline=True)
    if sp in premium:
        embed.add_field(name="GlingBot Premium", value="```fix\nPremium 사용중\n```", inline=False)
    else:
        embed.add_field(name="GlingBot Premium", value="```\nPremium 사용중이지 않음```\n", inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(description="메세지 삭제")
async def 삭제(ctx, 수 : discord.commands.Option(int, "삭제할 메세지 수")):
    global premium
    if not (ctx.author.guild_permissions.manage_messages) and not ctx.author==await bot.fetch_user(599740489801138197):
        await ctx.respond("메세지 관리 권한이 없습니다.",ephemeral=True)
        return
    sp=수
    embee = discord.Embed(title="메세지를 삭제하는 중입니다.", description="삭제하는 메세지 : {}개".format(sp), color=0xD358F7)
    await ctx.respond(embed=embee,ephemeral=True)
    await ctx.channel.purge(limit=sp,bulk=True)
    if int(ctx.author.id) in premium:
        embed = discord.Embed(title="메세지 삭제를 성공적으로 마쳤습니다.", description="삭제된 메세지 : {}개".format(sp), color=0xD358F7)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (premium)'.format(ctx.author))
    else:
        embed = discord.Embed(title="메세지 삭제를 성공적으로 마쳤습니다.", description="삭제된 메세지 : {}개".format(sp), color=0x00ff80)
        embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
    await ctx.respond(embed=embed)


@bot.slash_command(description="임베드 생성")
async def 임베드(ctx,title:discord.commands.Option(str, "타이틀(제목)"),description:discord.commands.Option(str, "소제목"),fieldname:discord.commands.Option(str, "내용 제목"),fieldvalue:discord.commands.Option(str, "내용")):
    global premium
    embed = discord.Embed(title=title, description=description, color=0xD358F7)
    embed.set_footer(icon_url=ctx.author.avatar, text=ctx.author.name)
    embed.add_field(name=fieldname, value=fieldvalue, inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(description="프리미엄+개발자 전용 기능, 파이썬 코드 컴파일링")
async def jsk(ctx, code: discord.commands.Option(str, "code 입력")):
    global premium
    code=code.replace(";","\n")
    if code.startswith("pre+"):
        if not int(ctx.author.id)==599740489801138197:
            embed = discord.Embed(title="소유자가 아닙니다.", description="이 기능은 소유자만 가능해요", color=0xFF0000)
            await ctx.respond(embed=embed,ephemeral=True)
            return
        sp=code.split(' ')
        print(re.sub(r'[^0-9]', '', sp[1]))
        sp=int(re.sub(r'[^0-9]', '', sp[1]))
        f = open("premium.txt", 'a')
        f.write('{},'.format(sp))
        f.close()
        premium.append(sp)
        h=await bot.fetch_user(sp)
        embed = discord.Embed(title="성공", description="`{}`님을 프리미엄 멤버 리스트에 추가합니다.".format(h,sp), color=0xD358F7)
        embed.add_field(name=f"Gllen의 {len(premium)}번째 프리미엄 소유자입니다.", value=f"ID : {sp}", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar, text='{} (봇 소유자)'.format(ctx.author))
        await ctx.respond(embed=embed)
        return
    if int(ctx.author.id) in premium:
        def insert_returns(body):
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])

            if isinstance(body[-1], ast.If):
                insert_returns(body[-1].body)
                insert_returns(body[-1].orelse)

            if isinstance(body[-1], ast.With):
                insert_returns(body[-1].body)
        print(code,ctx.author)
        cmd = code.split(" ")
        _cmd = cmd
        msg = await ctx.respond(embed = discord.Embed(title='Code Compiling').add_field(
            name='📥 Input',
            value=f'```py\n{cmd}```',
            inline=False
        ))#,ephemeral=True
        await asyncio.sleep(1)

        #banword checking
        banword = ['token', 'file=', 'file =']

        if cmd in banword:
            embed = discord.Embed(title='Code Compiling')
            embed.add_field(name='📥 Input', value=f'```py\n{_cmd}```', inline=False)
            embed.add_field(name = '📤 Output', value = f'`{cmd}`에는 eval에서 사용 금지된 단어가 포함되어 있습니다.')
            await msg.edit_original_message(embed=embed)
            await ctx.respond(f'{code}는 사용 금지된 단어가 포함되어 있습니다.',ephemeral=True)
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
                result = (await eval(f"{fn_name}()", env))
                embed=discord.Embed(title="실행 성공", colour=discord.Colour.green())
                embed.add_field(name="`📥 Input (들어가는 내용) 📥`", value=f"```py\n{ccode}```", inline=False)
                embed.add_field(name="`📤 Output (나오는 내용) 📤`", value=f"```py\n{result}```", inline=False)
                embed.add_field(name="`🔧 Type (타입) 🔧`",value=f"```py\n{type(result)}```", inline=False)
                embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)
                await msg.edit_original_message(embed = embed)
            except Exception as e:
                await ctx.respond(f"실행 중 오류가 발생하였습니다.\n\n```py\n{e}```",ephemeral=True)
    else:
        await ctx.respond("프리미엄이 아닙니다.",ephemeral=True)

@bot.slash_command(description="테스트 기능")
async def ai(ctx, message: discord.commands.Option(str, "AI에게 적을 메세지")):
    eng="text-davinci-003" #text-davinci-003(powerful) #text-curie-001 #text-babbage-001(lower) #text-ada-001(lowest)
    embed=discord.Embed(title="<a:loading:1076164295898959982>ChatGPT AI<a:loading:1076164295898959982>", description="AI가 생각하는 중입니다...\n시간 초과로 응답이 나오지 않을 수 있습니다.", colour=discord.Colour.green())
    embed.add_field(name="<a:blob_1:1076168747720650762> `Input` <a:blob_1:1076168747720650762>", value=f"```fix\n{message}```", inline=False)
    embed.add_field(name="<a:blob_2:1076168750576963655> `Engine` <a:blob_2:1076168750576963655>", value="{} (ChatGPT)".format(eng), inline=False)
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)
    msg=await ctx.respond(embed=embed)
    try:
        response = await openai.Completion.acreate(
            engine=eng,
            prompt=message,
            max_tokens=2048,
            top_p=0.1,
            stop=None,
            temperature=0.1,
        )
        resp=response.get("choices")[0].text
        '''embed=discord.Embed(title="ChatGPT AI", description="engine : {}".format(eng), colour=discord.Colour.green())
        embed.add_field(name="`📥 Input (들어가는 내용) 📥`", value=f"```py\n'{message}'```", inline=False)
        embed.add_field(name="`📤 Output (나오는 내용) 📤`", value=f"```\n{resp}```", inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)'''
        await msg.edit_original_message(embed=None,content="```\n>>> {}\n{}```".format(message,resp))
    except Exception as e:
        embed=discord.Embed(title="<a:error:1076170456740143135> ChatGPT AI : Error <a:error:1076170456740143135>", description="시간 초과 또는 다른 오류입니다. 다시 질문해주세요!", colour=discord.Colour.red())
        embed.add_field(name="Debug Message", value=f"```py\n{e}````", inline=False)
        await msg.edit_original_message(embed=embed)

bot.run(token) # Bot Running Code