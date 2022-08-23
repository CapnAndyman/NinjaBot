import nextcord
import random
import re
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import sys, os

class Ninjabotnihongo:
    async def ninjabotnihongo(self,ninjabot,message,gamemode,prefix):
        
        try:

            self.settings = ninjabot.settings

            nscore = prefix + 'nscore'
            nl = prefix + 'nihongo'
            ns = prefix + 'niho'
            gamestop = prefix + 'stop'

            nihongohelpembed=nextcord.Embed(title="NinjaBot Nihongo", description="More Information")
            nihongohelpembed.add_field(name="Playing", value='Once you type `{0}nihongo` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}oniisan` if you think the answer is oniisan.'.format(prefix), inline=False)
            nihongohelpembed.add_field(name="Scoring", value='Type `{}nscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)
            nihongohelpembed.add_field(name="Difficulty Levels", value='You can set the JLPT level (1-5) of the vocabulary. The default is 5, which is the lowest.\r\nExample: `ninjabot japanese level 4`', inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

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
                    
                    nihongodata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.nihongoallsql,(randomrow,))

                    answer = '; '.join((nihongodata[0][1],nihongodata[0][2]))

                    gamefile = makeimage(nihongodata[0][3])
                    nihongoembed=nextcord.Embed(title="Ninjabot Nihongo", description="`How do you pronounce this?`", color=nextcord.Color.blue())
                    nihongoembed.set_image(url="attachment://image.png")
                    
                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=nihongoembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongowrite,(answer,nihongodata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    
                    else:

                        await message.channel.send(file=gamefile, embed=nihongoembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongowrite,(answer,nihongodata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

                elif channellevel[0][0]:
                    namedlevel = 'JLPT' + str(channellevel[0][0] - 1)
                    nihongodata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.nihongorandom,(namedlevel,))

                    answer = '; '.join((nihongodata[0][1],nihongodata[0][2]))

                    gamefile = makeimage(nihongodata[0][3])
                    nihongoembed=nextcord.Embed(title="Ninjabot Nihongo", description="`How do you pronounce this?`", color=nextcord.Color.blue())
                    nihongoembed.set_image(url="attachment://image.png")

                    if prefix == 'resume':

                        await message.send(file=gamefile, embed=nihongoembed)
                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongowrite,(answer,nihongodata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    
                    else:

                        await message.channel.send(file=gamefile, embed=nihongoembed)   
                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongowrite,(answer,nihongodata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))       

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                nihongodata = ninjabot.ninjabotsql.sql_select(self.settings.nihongoanswersql,(message.id,))
                revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.nihongoreveal,(nihongodata[0][1],))
                
                gamefile = makeimage(revealdata[0][4])
                nihongoembed=nextcord.Embed(title="Ninjabot Nihongo", description='`Times Up!`', color=nextcord.Color.red())
                nihongoembed.add_field(name="Kana", value='`{}`'.format(revealdata[0][1]), inline=True)
                nihongoembed.add_field(name="Romaji", value='`{}`'.format(revealdata[0][2]), inline=True)
                nihongoembed.add_field(name="English", value=revealdata[0][3], inline=True)
                nihongoembed.set_image(url="attachment://image.png")

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.nihongostopsql,(message.id,))

                await message.send(file=gamefile, embed=nihongoembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'nihongo',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Nihongo starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Nihongo is now stopped.')

            elif prefix == 'resume':
                await newgame(prefix)  

            if userinput == nscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.nihongogetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a nihongo score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.nihongo or userinput == self.settings.nihongohelp:
                
                await message.channel.send(embed=nihongohelpembed)

            elif userinput == ns or userinput == nl:

                await newgame(prefix)

                if userinput == nl:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(ns,nl))

            elif userinput == gamestop and gamemode:
                nihongodata = ninjabot.ninjabotsql.sql_select(self.settings.nihongoanswersql,(userchannel,))
                revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.nihongoreveal,(nihongodata[0][1],))
                
                gamefile = makeimage(revealdata[0][4])
                nihongoembed=nextcord.Embed(title="Ninjabot Nihongo", description='`Ninjabot Nihongo is now stopped.`', color=nextcord.Color.red())
                nihongoembed.add_field(name="Kana", value='`{}`'.format(revealdata[0][1]), inline=True)
                nihongoembed.add_field(name="Romaji", value='`{}`'.format(revealdata[0][2]), inline=True)
                nihongoembed.add_field(name="English", value=revealdata[0][3], inline=True)
                nihongoembed.set_image(url="attachment://image.png")
                await message.channel.send(file=gamefile, embed=nihongoembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.nihongostopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                nihongodata = ninjabot.ninjabotsql.sql_select(self.settings.nihongoanswersql,(userchannel,))

                if nihongodata[0][0]:
                
                    if useranswer in nihongodata[0][0].split('; '):
                        
                        revealdata = ninjabot.ninjabotsql.sql_japaneseselect(self.settings.nihongoreveal,(nihongodata[0][1],))
                        nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]
                        
                        gamefile = makeimage(revealdata[0][4])
                        nihongoembed=nextcord.Embed(title="Ninjabot Nihongo", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        nihongoembed.add_field(name="Kana", value='`{}`'.format(revealdata[0][1]), inline=True)
                        nihongoembed.add_field(name="Romaji", value='`{}`'.format(revealdata[0][2]), inline=True)
                        nihongoembed.add_field(name="English", value=revealdata[0][3], inline=True)
                        nihongoembed.set_image(url="attachment://image.png")
                        await message.channel.send(file=gamefile, embed=nihongoembed)
                        await message.channel.send('Reminder: You can change the difficulty with `ninjabot japanese level`.')

                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongostopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.nihongosetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'nihongo',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Nihongo starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'nihongo' in useranswer.lower() or 'niho' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Nihongo.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Nihongo.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))