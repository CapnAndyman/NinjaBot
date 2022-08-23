import nextcord
import random
import re
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import sys, os
from difflib import SequenceMatcher

class Ninjabotjapanese:
    async def ninjabotjapanese(self,ninjabot,message,gamemode,prefix):

        try:

            self.settings = ninjabot.settings

            jscore = prefix + 'jscore'
            jl = prefix + 'japanese'
            js = prefix + 'japa'
            gamestop = prefix + 'stop'

            japanesehelpembed=nextcord.Embed(title="NinjaBot japanese", description="More Information")
            japanesehelpembed.add_field(name="Playing", value='Once you type `{0}japanese` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}walk` if you think the answer is walk.'.format(prefix), inline=False)
            japanesehelpembed.add_field(name="Scoring", value='Type `{}jscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)
            japanesehelpembed.add_field(name="Difficulty Levels", value='You can set the JLPT level between 5 and 1. The default is 5, which is the lowest.\r\nExample: `ninjabot japanese level 4`', inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

            def similar(a, b):
                return SequenceMatcher(None, a, b).ratio()

            def makeimage(character):

                width = 100*len(character)
                img = Image.new('RGB', (width, 100), color = (0, 0, 0))
                fnt = ImageFont.truetype('fonts/DroidSansFallback.ttf', 100)
                d = ImageDraw.Draw(img)
                d.text((00,-20), character, font=fnt, fill=(255,255,255))

                arr = io.BytesIO()
                img.save(arr, format='PNG')
                arr.seek(0)
                gamefile = nextcord.File(arr, 'image.png')
                return gamefile

            async def newgame(prefix):

                channellevel = ''
                
                if prefix == 'resume':

                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.japanesegetlevel,(message.id,))
                
                else:
                
                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.japanesegetlevel,(userchannel,))
                
                if not channellevel[0][0]:
                
                    randomrow = random.randrange(1, 6001)

                    japanesedata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.japaneseallsql,(randomrow,))

                    gamefile = makeimage(japanesedata[0][8])
                    japaneseembed=nextcord.Embed(title="Ninjabot Japanese", description="`What does this mean?`", color=nextcord.Color.blue())
                    japaneseembed.add_field(name="Type", value=japanesedata[0][4], inline=True)
                    japaneseembed.add_field(name="Kana", value=japanesedata[0][1], inline=True)
                    japaneseembed.add_field(name="Romaji", value=japanesedata[0][2], inline=True)
                    japaneseembed.add_field(name="Sentence", value=japanesedata[0][5], inline=False)
                    japaneseembed.add_field(name="Kana Sentence", value=japanesedata[0][6], inline=True)
                    japaneseembed.add_field(name="Romaji Sentence", value=japanesedata[0][7], inline=False)
                    japaneseembed.set_image(url="attachment://image.png")
                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=japaneseembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesewrite,(japanesedata[0][3],japanesedata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                    else:

                        await message.channel.send(file=gamefile, embed=japaneseembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesewrite,(japanesedata[0][3],japanesedata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

                elif channellevel[0][0]:
                    namedlevel = 'JLPT' + str(channellevel[0][0] - 1)
                    japanesedata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.japaneserandom,(namedlevel,))

                    gamefile = makeimage(japanesedata[0][8])
                    japaneseembed=nextcord.Embed(title="Ninjabot Japanese", description="`What does this mean?`", color=nextcord.Color.blue())
                    japaneseembed.add_field(name="Type", value=japanesedata[0][4], inline=True)
                    japaneseembed.add_field(name="Kana", value=japanesedata[0][1], inline=True)
                    japaneseembed.add_field(name="Romaji", value=japanesedata[0][2], inline=True)
                    japaneseembed.add_field(name="Sentence", value=japanesedata[0][5], inline=False)
                    japaneseembed.add_field(name="Kana Sentence", value=japanesedata[0][6], inline=True)
                    japaneseembed.add_field(name="Romaji Sentence", value=japanesedata[0][7], inline=False)
                    japaneseembed.set_image(url="attachment://image.png")
                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=japaneseembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesewrite,(japanesedata[0][3],japanesedata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                    else:

                        await message.channel.send(file=gamefile, embed=japaneseembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesewrite,(japanesedata[0][3],japanesedata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                japanesedata = ninjabot.ninjabotsql.sql_select(self.settings.japaneseanswersql,(message.id,))
                revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.japanesereveal,(japanesedata[0][1],))
                
                gamefile = makeimage(revealdata[0][9])
                japaneseembed=nextcord.Embed(title="Ninjabot Japanese", description='`Times Up!`', color=nextcord.Color.red())
                japaneseembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][3]), inline=True)
                japaneseembed.add_field(name="Type", value=revealdata[0][4], inline=True)
                japaneseembed.add_field(name="Kana", value=revealdata[0][1], inline=True)
                japaneseembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                japaneseembed.add_field(name="Sentence", value=revealdata[0][5], inline=False)
                japaneseembed.add_field(name="Kana Sentence", value=revealdata[0][6], inline=True)
                japaneseembed.add_field(name="Romaji Sentence", value=revealdata[0][7], inline=False)
                japaneseembed.add_field(name="English Sentence", value=revealdata[0][8], inline=False)
                japaneseembed.set_image(url="attachment://image.png")

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.japanesestopsql,(message.id,))

                await message.send(file=gamefile, embed=japaneseembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'japanese',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Japanese starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Japanase is now stopped.')         

            elif prefix == 'resume':
                await newgame(prefix)   

            if userinput == jscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.japanesegetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a japanese score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.japanese or userinput == self.settings.japanesehelp:
                
                await message.channel.send(embed=japanesehelpembed)

            elif userinput.startswith(self.settings.japaneselevel):

                if userinput == self.settings.japaneselevel:

                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.japanesegetlevel,(userchannel,))[0][0]

                    if not channellevel:
                        channellevel = 'all'

                    await message.channel.send('This channel is currently set at Japanese level `{}`.\r\nTo change this, type `ninjabot japanese level` followed by a new level.\r\nDifficulty levels are based on JLPT and range from 1-5 with 5 as the lowest.\r\nYou can also use `all` for maximum difficulty.\r\nExample: `ninjabot japanese level 4`'.format(channellevel))

                else:

                    try:
                        
                        if userinput.split(' ')[-1] == 'all':
                            ninjabot.ninjabotsql.sql_insert(self.settings.japanesenulllevel,(userchannel,))
                            await message.channel.send('Japanese level for channel has been set to `all`.')

                        elif int(userinput.split(' ')[-1]) in range(1,6):
                            ninjabot.ninjabotsql.sql_insert(self.settings.japanesesetlevel,(userinput.split(' ')[-1],userchannel))
                            await message.channel.send('Japanese level for channel has been set to `' + userinput.split(' ')[-1] + '`.')

                        else:
                            await message.channel.send("That is not a valid Japanese level. Only 1-5 and 'all' are allowed.")

                    except:

                        await message.channel.send("That is not a valid Japanese level. Only 1-5 and 'all' are allowed.")

            elif userinput == js or userinput == jl:

                await newgame(prefix)

                if userinput == jl:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(js,jl))

            elif userinput == gamestop and gamemode:
                japanesedata = ninjabot.ninjabotsql.sql_select(self.settings.japaneseanswersql,(userchannel,))
                revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.japanesereveal,(japanesedata[0][1],))
                
                gamefile = makeimage(revealdata[0][9])
                japaneseembed=nextcord.Embed(title="Ninjabot Japanese", description='`Ninjabot Japanese is now stopped.`', color=nextcord.Color.red())
                japaneseembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][3]), inline=True)
                japaneseembed.add_field(name="Type", value=revealdata[0][4], inline=True)
                japaneseembed.add_field(name="Kana", value=revealdata[0][1], inline=True)
                japaneseembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                japaneseembed.add_field(name="Sentence", value=revealdata[0][5], inline=False)
                japaneseembed.add_field(name="Kana Sentence", value=revealdata[0][6], inline=True)
                japaneseembed.add_field(name="Romaji Sentence", value=revealdata[0][7], inline=False)
                japaneseembed.add_field(name="English Sentence", value=revealdata[0][8], inline=False)
                japaneseembed.set_image(url="attachment://image.png")
                await message.channel.send(file=gamefile, embed=japaneseembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.japanesestopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                japanesedata = ninjabot.ninjabotsql.sql_select(self.settings.japaneseanswersql,(userchannel,))
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                if japanesedata[0][0]:
                
                    if similar(useranswer,japanesedata[0][0].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in re.split('();',japanesedata[0][0])):
                        
                        revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.japanesereveal,(japanesedata[0][1],))
                        
                        gamefile = makeimage(revealdata[0][9])
                        japaneseembed=nextcord.Embed(title="Ninjabot Japanese", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        japaneseembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][3]), inline=True)
                        japaneseembed.add_field(name="Type", value=revealdata[0][4], inline=True)
                        japaneseembed.add_field(name="Kana", value=revealdata[0][1], inline=True)
                        japaneseembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                        japaneseembed.add_field(name="Sentence", value=revealdata[0][5], inline=False)
                        japaneseembed.add_field(name="Kana Sentence", value=revealdata[0][6], inline=True)
                        japaneseembed.add_field(name="Romaji Sentence", value=revealdata[0][7], inline=False)
                        japaneseembed.add_field(name="English Sentence", value=revealdata[0][8], inline=False)
                        japaneseembed.set_image(url="attachment://image.png")
                        await message.channel.send(file=gamefile, embed=japaneseembed)
                        systemRandom = random.SystemRandom()
                        secureNum1 = systemRandom.randint(1, 6)
                        if secureNum1 == 1:
                            await message.channel.send('Reminder: You can change the difficulty with `ninjabot japanese level`.')

                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesestopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.japanesesetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'japanese',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Japanese starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'japanese' in useranswer.lower() or 'japa' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Japanese.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Japanese.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))