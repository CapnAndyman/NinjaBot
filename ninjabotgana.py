import nextcord
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io
import sys, os

class Ninjabotgana:
    async def ninjabotgana(self,ninjabot,message,gamemode,prefix):

        try:

            self.settings = ninjabot.settings

            gnscore = prefix + 'gnscore'
            gns = prefix + 'hira'
            gnl = prefix + 'hiragana'
            gna = prefix + 'gana'
            gamestop = prefix + 'stop'

            ganahelpembed=nextcord.Embed(title='NinjaBot Hiragana', description="More Information")
            ganahelpembed.add_field(name="Playing", value='Once you type `{0}gana` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}ga` if you think the answer is ga.'.format(prefix), inline=False)
            ganahelpembed.add_field(name="Scoring", value='Type `{}gnscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

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

                randomrow = random.randrange(1, 105)
                
                ganadata = ninjabot.ninjabotsql.sql_ganaselect(self.settings.ganaallsql,(randomrow,))

                gamefile = makeimage(ganadata[0][2])

                ganaembed=nextcord.Embed(title="Ninjabot Hiragana", description="`How do you pronounce this character?`", color=nextcord.Color.blue())
                ganaembed.set_image(url="attachment://image.png")
                
                if prefix == 'resume':

                    await message.send(file=gamefile, embed=ganaembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.ganawrite,(ganadata[0][0],ganadata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                else:

                    await message.channel.send(file=gamefile, embed=ganaembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.ganawrite,(ganadata[0][0],ganadata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                ganadata = ninjabot.ninjabotsql.sql_select(self.settings.ganaanswersql,(message.id,))            
                revealdata = ninjabot.ninjabotsql.sql_ganaselect(self.settings.ganareveal,(ganadata[0][1],))

                gamefile = makeimage(revealdata[0][1])
                
                ganaembed=nextcord.Embed(title="Ninjabot Hiragana", description='`Times Up!`', color=nextcord.Color.red())
                ganaembed.add_field(name="Answer", value='`{}`'.format(ganadata[0][0]), inline=False)
                ganaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                ganaembed.set_image(url="attachment://image.png")

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.ganastopsql,(message.id,))

                await message.send(file=gamefile, embed=ganaembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'gana',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Hiragana starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Hiragana is now stopped.')      

            elif prefix == 'resume':
                await newgame(prefix)      

            if userinput == gnscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.ganagetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a Hiragana score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.gana or userinput == self.settings.ganahelp:

                await message.channel.send(embed=ganahelpembed)

            elif userinput == gns or userinput == gnl or userinput == gna:

                await newgame(prefix)
                
                if userinput == gnl:
                    await message.channel.send('Reminder: you can also type `{}` or `{}` instead of `{}`.'.format(gns,gna,gnl))

            elif userinput == gamestop and gamemode:

                ganadata = ninjabot.ninjabotsql.sql_select(self.settings.ganaanswersql,(userchannel,))            
                revealdata = ninjabot.ninjabotsql.sql_ganaselect(self.settings.ganareveal,(ganadata[0][1],))

                gamefile = makeimage(revealdata[0][1])
                
                ganaembed=nextcord.Embed(title="Ninjabot Hiragana", description='`NinjaBot Hiragana is now stopped.`', color=nextcord.Color.red())
                ganaembed.add_field(name="Answer", value='`{}`'.format(ganadata[0][0]), inline=False)
                ganaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                ganaembed.set_image(url="attachment://image.png")
                await message.channel.send(file=gamefile, embed=ganaembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.ganastopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                ganadata = ninjabot.ninjabotsql.sql_select(self.settings.ganaanswersql,(userchannel,))

                if ganadata[0][0]:

                    if useranswer == ganadata[0][0]:
                        
                        revealdata = ninjabot.ninjabotsql.sql_ganaselect(self.settings.ganareveal,(ganadata[0][1],))
                        nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                        gamefile = makeimage(revealdata[0][1])
                        
                        ganaembed=nextcord.Embed(title="Ninjabot Hiragana", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        ganaembed.add_field(name="Answer", value='`{}`'.format(ganadata[0][0]), inline=False)
                        ganaembed.add_field(name="Kana Type", value=revealdata[0][0], inline=True)
                        ganaembed.set_image(url="attachment://image.png")
                        await message.channel.send(file=gamefile, embed=ganaembed)

                        ninjabot.ninjabotsql.sql_insert(self.settings.ganastopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.ganasetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'gana',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Hiragana starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'hiragana' in useranswer.lower() or 'hira' in useranswer.lower() or 'gana' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Hiragana.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Hiragana.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))