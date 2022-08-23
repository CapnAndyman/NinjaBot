import nextcord
import random
import time
import asyncio
import sys, os
from difflib import SequenceMatcher

class Ninjabotasl:
    async def ninjabotasl(self,ninjabot,message,gamemode,prefix):
        
        try:

            self.settings = ninjabot.settings
                    
            aslscore = prefix + 'aslscore'
            asl = prefix + 'asl'
            gamestop = prefix + 'stop'

            aslhelpembed=nextcord.Embed(title="NinjaBot ASL", description="More Information")
            aslhelpembed.add_field(name="Playing", value='Once you type `{0}asl` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}walking` if you think the answer is walking.'.format(prefix))
            aslhelpembed.add_field(name="Scoring", value='Type `{}aslscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

            def similar(a, b):
                return SequenceMatcher(None, a, b).ratio()

            async def newgame(prefix):

                asldata = ninjabot.ninjabotsql.sql_aslselect(self.settings.aslrandom,('1',))

                embedimg = asldata[0][2]

                aslembed=nextcord.Embed(title="Ninjabot ASL", description="What does this mean?", color=nextcord.Color.blue())
                aslembed.set_image(url=embedimg)
                
                if prefix == 'resume':

                    await message.send(embed=aslembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.aslwrite,(asldata[0][0],asldata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))

                else:

                    await message.channel.send(embed=aslembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.aslwrite,(asldata[0][0],asldata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                asldata = ninjabot.ninjabotsql.sql_select(self.settings.aslanswersql,(message.id,))
                revealdata = ninjabot.ninjabotsql.sql_aslselect(self.settings.aslreveal,(asldata[0][1],))
                
                embedimg = revealdata[0][2]
                aslembed=nextcord.Embed(title="Ninjabot ASL", description='Times Up!', color=nextcord.Color.red())
                aslembed.add_field(name="Possible Answers", value='`{}`'.format(revealdata[0][0]), inline=False)
                aslembed.set_image(url=embedimg)                 

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.aslstopsql,(message.id,))

                await message.send(embed=aslembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'asl',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New ASL starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. ASL is now stopped.')  

            elif prefix == 'resume':
                await newgame(prefix)

            if userinput == aslscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.aslgetscore,(userid,))
                await message.channel.send('{0.author} has an ASL score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.asl or userinput == self.settings.aslhelp:

                await message.channel.send(embed=aslhelpembed)

            elif userinput == asl:
                
                await newgame(prefix)

            elif userinput == gamestop and gamemode:
                asldata = ninjabot.ninjabotsql.sql_select(self.settings.aslanswersql,(userchannel,))
                revealdata = ninjabot.ninjabotsql.sql_aslselect(self.settings.aslreveal,(asldata[0][1],))
                
                embedimg = revealdata[0][2]
                aslembed=nextcord.Embed(title="Ninjabot ASL", description='NinjaBot ASL has stopped!', color=nextcord.Color.red())
                aslembed.add_field(name="Possible Answers", value='`{}`'.format(revealdata[0][0]), inline=False)
                aslembed.set_image(url=embedimg)
                await message.channel.send(embed=aslembed)                 

                ninjabot.ninjabotsql.sql_insert(self.settings.aslstopsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                asldata = ninjabot.ninjabotsql.sql_select(self.settings.aslanswersql,(userchannel,))
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                if asldata[0][0]:

                    if similar(useranswer,asldata[0][0].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in asldata[0][0].split('; ')):
                        
                        revealdata = ninjabot.ninjabotsql.sql_aslselect(self.settings.aslreveal,(asldata[0][1],))
                        
                        embedimg = revealdata[0][2]
                        aslembed=nextcord.Embed(title="Ninjabot ASL", description='That is correct {0.author}! You win one point!'.format(message), color=nextcord.Color.green())
                        aslembed.add_field(name="Possible Answers", value='`{}`'.format(revealdata[0][0]), inline=False)
                        aslembed.set_image(url=embedimg)
                        await message.channel.send(embed=aslembed) 

                        ninjabot.ninjabotsql.sql_insert(self.settings.aslsetscore,(userid,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.aslstopsql,(userchannel,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'asl',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New ASL starts in 3 seconds.')
                    
                    else:
                        if not freeanswer:
                            if 'asl' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop ASL.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop ASL.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))