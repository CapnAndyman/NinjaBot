import nextcord
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import sys, os
from difflib import SequenceMatcher

class Ninjabotkanji:
    async def ninjabotkanji(self,ninjabot,message,gamemode,prefix):
        
        try:
        
            self.settings = ninjabot.settings

            kscore = prefix + 'kscore'
            kl = prefix + 'kanji'
            ks = prefix + 'kanj'
            gamestop = prefix + 'stop'

            kanjihelpembed=nextcord.Embed(title="NinjaBot Kanji", description="More Information")
            kanjihelpembed.add_field(name="Playing", value='Once you type `{0}kanji` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}red` if you think the answer is red.'.format(prefix), inline=False)
            kanjihelpembed.add_field(name="Scoring", value='Type `{}kscore` to see your total score. You recieve one point per successful game.'.format(prefix), inline=False)
            kanjihelpembed.add_field(name="Difficulty Levels", value='You can change the difficulty level. The following changes you to level 1:\r\n`ninjabot kanji level 1`\r\nBy default, you will be set to the "1" option.\r\nLevels range from 1 to 9.\r\nIf you have never learned Kanji before, I recommend leaving it at level 1', inline=False)

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

                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.kanjigetlevel,(message.id,))
                
                else:

                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.kanjigetlevel,(userchannel,))

                if not channellevel[0][0]:
                    randomrow = random.randrange(1, 13039)
                    
                    kanjidata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjiallsql,(randomrow,))

                    while not kanjidata[0][0]:
                        randomrow = random.randrange(1, 13039)
                        kanjidata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjiallsql,(randomrow,))

                    gamefile = makeimage(kanjidata[0][2])

                    kanjiembed=nextcord.Embed(title="Ninjabot Kanji", description="`What does this character mean?`", color=nextcord.Color.blue())
                    kanjiembed.set_image(url="attachment://image.png")
                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=kanjiembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjiwrite,(kanjidata[0][0],kanjidata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                    else:

                        await message.channel.send(file=gamefile, embed=kanjiembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjiwrite,(kanjidata[0][0],kanjidata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

                elif channellevel[0][0]:

                    kanjidata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjirandom,(channellevel[0][0],))

                    while not kanjidata[0][0]:
                        
                        kanjidata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjirandom,(channellevel[0][0],))

                    gamefile = makeimage(kanjidata[0][2])

                    kanjiembed=nextcord.Embed(title="Ninjabot Kanji", description="`What does this character mean?`", color=nextcord.Color.blue())
                    kanjiembed.set_image(url="attachment://image.png")
                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=kanjiembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjiwrite,(kanjidata[0][0],kanjidata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                    else:

                        await message.channel.send(file=gamefile, embed=kanjiembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjiwrite,(kanjidata[0][0],kanjidata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')    
                if not userinput.startswith(prefix):
                    freeanswer = 1    

            elif prefix == 'timesup':

                kanjidata = ninjabot.ninjabotsql.sql_select(self.settings.kanjianswersql,(message.id,))
                
                revealdata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjireveal,(kanjidata[0][1],))
                
                gamefile = makeimage(revealdata[0][3])
                kanjiembed=nextcord.Embed(title="Ninjabot Kanji", description='Times Up!', color=nextcord.Color.red())
                kanjiembed.add_field(name="Possible Answers", value='`{}`'.format(kanjidata[0][0]), inline=False)
                if revealdata[0][0]:
                    kanjiembed.add_field(name="On Reading", value=revealdata[0][0], inline=True)
                if revealdata[0][1]:
                    kanjiembed.add_field(name="Kun Reading", value=revealdata[0][1], inline=True)            
                if revealdata[0][2]:
                    kanjiembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                kanjiembed.set_image(url="attachment://image.png")
                
                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]
                
                ninjabot.ninjabotsql.sql_insert(self.settings.kanjistopsql,(message.id,))

                await message.send(file=gamefile, embed=kanjiembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'kanji',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Kanji starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Kanji is now stopped.')

            elif prefix == 'resume':
                await newgame(prefix)

            if userinput == kscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.kanjigetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a Kanji score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.kanji or userinput == self.settings.kanjihelp:
                await message.channel.send(embed=kanjihelpembed)

            elif userinput.startswith(self.settings.kanjilevel):

                if userinput == self.settings.kanjilevel:
                    channellevel = ninjabot.ninjabotsql.sql_select(self.settings.kanjigetlevel,(userchannel,))[0][0]
                    if not channellevel:
                        channellevel = 'all'
                    await message.channel.send('This channel is currently set at Kanji level `{}`.\r\nTo change this, type `ninjabot kanji level` followed by a new level.\r\nLevels range from 1 to 9. You can also use `all` for maximum difficulty.\r\nExample: `ninjabot kanji level 2`'.format(channellevel))

                else:

                    try:

                        if userinput.split(' ')[-1] == 'all':
                            ninjabot.ninjabotsql.sql_insert(self.settings.kanjinulllevel,(userchannel,))
                            await message.channel.send('Kanji level for channel has been set to `all`.')

                        elif int(userinput.split(' ')[-1]) in range(1,10):
                            ninjabot.ninjabotsql.sql_insert(self.settings.kanjisetlevel,(userinput.split(' ')[-1],userchannel))
                            await message.channel.send('Kanji level for channel has been set to `' + userinput.split(' ')[-1] + '`.')

                        else:
                            await message.channel.send("That is not a valid Kanji level. Only 1-9 and 'all' are allowed.")

                    except:

                        await message.channel.send("That is not a valid Kanji level. Only 1-9 and 'all' are allowed.")

            elif userinput == ks or userinput == kl:
                
                await newgame(prefix)

            elif userinput == gamestop and gamemode:

                kanjidata = ninjabot.ninjabotsql.sql_select(self.settings.kanjianswersql,(userchannel,))
                
                revealdata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjireveal,(kanjidata[0][1],))
                
                gamefile = makeimage(revealdata[0][3])
                kanjiembed=nextcord.Embed(title="Ninjabot Kanji", description='`NinjaBot Kanji is now stopped.`', color=nextcord.Color.red())
                kanjiembed.add_field(name="Possible Answers", value='`{}`'.format(kanjidata[0][0]), inline=False)
                if revealdata[0][0]:
                    kanjiembed.add_field(name="On Reading", value=revealdata[0][0], inline=True)
                if revealdata[0][1]:
                    kanjiembed.add_field(name="Kun Reading", value=revealdata[0][1], inline=True)            
                if revealdata[0][2]:
                    kanjiembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                kanjiembed.set_image(url="attachment://image.png")
                await message.channel.send(file=gamefile, embed=kanjiembed) 
                
                ninjabot.ninjabotsql.sql_insert(self.settings.kanjistopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                kanjidata = ninjabot.ninjabotsql.sql_select(self.settings.kanjianswersql,(userchannel,))
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                if kanjidata[0][0]:
                    if similar(useranswer,kanjidata[0][0].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in kanjidata[0][0].split('; ')):
                        
                        revealdata = ninjabot.ninjabotsql.sql_kanjiselect(self.settings.kanjireveal,(kanjidata[0][1],))
                        
                        gamefile = makeimage(revealdata[0][3])
                        kanjiembed=nextcord.Embed(title="Ninjabot Kanji", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        kanjiembed.add_field(name="Possible Answers", value='`{}`'.format(kanjidata[0][0]), inline=False)
                        if revealdata[0][0]:
                            kanjiembed.add_field(name="On Reading", value=revealdata[0][0], inline=True)
                        if revealdata[0][1]:
                            kanjiembed.add_field(name="Kun Reading", value=revealdata[0][1], inline=True)            
                        if revealdata[0][2]:
                            kanjiembed.add_field(name="Romaji", value=revealdata[0][2], inline=True)
                        kanjiembed.set_image(url="attachment://image.png")
                        await message.channel.send(file=gamefile, embed=kanjiembed)
                        systemRandom = random.SystemRandom()
                        secureNum1 = systemRandom.randint(1, 6)
                        if secureNum1 == 1:
                            await message.channel.send('Reminder: You can change the difficulty with `ninjabot kanji level`.')

                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjistopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanjisetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'kanji',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Kanji starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))

                    else:
                        if not freeanswer:
                            if 'kanji' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Kanji.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Kanji.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))
        
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))