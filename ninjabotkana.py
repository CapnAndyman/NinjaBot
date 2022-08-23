import nextcord
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import sys, os

class Ninjabotkana:
    async def ninjabotkana(self,ninjabot,message,gamemode,prefix):
        
        try:
        
            self.settings = ninjabot.settings
            
            knscore = prefix + 'knscore'
            knl = prefix + 'katakana'
            kns = prefix + 'kata'
            kna = prefix + 'kana'
            gamestop = prefix + 'stop'

            kanahelpembed=nextcord.Embed(title='NinjaBot Katakana', description="More Information")
            kanahelpembed.add_field(name="Playing", value='Once you type `{0}kana` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}ka` if you think the answer is ka.'.format(prefix), inline=False)
            kanahelpembed.add_field(name="Scoring", value='Type `{}knscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

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

                randomrow = random.randrange(105, 214)
                
                kanadata = ninjabot.ninjabotsql.sql_kanaselect(self.settings.kanaallsql,(randomrow,))

                gamefile = makeimage(kanadata[0][2])

                kanaembed=nextcord.Embed(title="Ninjabot Katakana", description="`How do you pronounce this character?`", color=nextcord.Color.blue())
                kanaembed.set_image(url="attachment://image.png")
                
                if prefix == 'resume':

                    await message.send(file=gamefile, embed=kanaembed) 
                    ninjabot.ninjabotsql.sql_insert(self.settings.kanawrite,(kanadata[0][0],kanadata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                
                else:

                    await message.channel.send(file=gamefile, embed=kanaembed)   
                    ninjabot.ninjabotsql.sql_insert(self.settings.kanawrite,(kanadata[0][0],kanadata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))     
            
            
            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                kanadata = ninjabot.ninjabotsql.sql_select(self.settings.kanaanswersql,(message.id,))            
                revealdata = ninjabot.ninjabotsql.sql_kanaselect(self.settings.kanareveal,(kanadata[0][1],))

                gamefile = makeimage(revealdata[0][1])
                
                kanaembed=nextcord.Embed(title="Ninjabot Katakana", description='`Times Up!`', color=nextcord.Color.red())
                kanaembed.add_field(name="Answer", value='`{}`'.format(kanadata[0][0]), inline=False)
                kanaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                kanaembed.set_image(url="attachment://image.png")

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.kanastopsql,(message.id,))

                await message.send(file=gamefile, embed=kanaembed) 

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'kana',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Katakana starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Katakana is now stopped.')    

            elif prefix == 'resume':
                await newgame(prefix)                 

            if userinput == knscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.kanagetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a Katakana score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.kana or userinput == self.settings.kanahelp:
                await message.channel.send(embed=kanahelpembed)

            elif userinput == kns or userinput == knl or userinput == kna:

                await newgame(prefix)

                if userinput == knl:
                    await message.channel.send('Reminder: you can also type `{}` or `{}` instead of `{}`.'.format(kns,kna,knl))

            elif userinput == gamestop and gamemode:

                kanadata = ninjabot.ninjabotsql.sql_select(self.settings.kanaanswersql,(userchannel,))            
                revealdata = ninjabot.ninjabotsql.sql_kanaselect(self.settings.kanareveal,(kanadata[0][1],))

                gamefile = makeimage(revealdata[0][1])
                
                kanaembed=nextcord.Embed(title="Ninjabot Katakana", description='`NinjaBot Katakana is now stopped.`', color=nextcord.Color.red())
                kanaembed.add_field(name="Answer", value='`{}`'.format(kanadata[0][0]), inline=False)
                kanaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                kanaembed.set_image(url="attachment://image.png")
                await message.channel.send(file=gamefile, embed=kanaembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.kanastopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                kanadata = ninjabot.ninjabotsql.sql_select(self.settings.kanaanswersql,(userchannel,))

                if kanadata[0][0]:
                
                    if useranswer == kanadata[0][0]:
                        
                        revealdata = ninjabot.ninjabotsql.sql_kanaselect(self.settings.kanareveal,(kanadata[0][1],))
                        nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                        gamefile = makeimage(revealdata[0][1])
                        
                        kanaembed=nextcord.Embed(title="Ninjabot Katakana", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        kanaembed.add_field(name="Answer", value='`{}`'.format(kanadata[0][0]), inline=False)
                        kanaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                        kanaembed.set_image(url="attachment://image.png")
                        await message.channel.send(file=gamefile, embed=kanaembed)

                        ninjabot.ninjabotsql.sql_insert(self.settings.kanastopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.kanasetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'kana',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Katakana starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'katakana' in useranswer.lower() or 'kata' in useranswer.lower() or 'kana' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Katakana.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Katakana.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))