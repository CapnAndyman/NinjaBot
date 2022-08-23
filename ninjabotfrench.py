import nextcord
import random
import re
import time
import asyncio
import sys, os
from difflib import SequenceMatcher

class Ninjabotfrench:
    async def ninjabotfrench(self,ninjabot,message,gamemode,prefix):
        
        try:

            self.settings = ninjabot.settings

            fscore = prefix + 'fscore'
            fl = prefix + 'french'
            fs = prefix + 'fren'
            gamestop = prefix + 'stop'

            frenchhelpembed=nextcord.Embed(title="NinjaBot French", description="More Information")
            frenchhelpembed.add_field(name="Playing", value='Once you type `{0}french` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}music` if you think the answer is music.'.format(prefix))
            frenchhelpembed.add_field(name="Scoring", value='Type `{}fscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

            def similar(a, b):
                return SequenceMatcher(None, a, b).ratio()

            async def newgame(prefix):

                randomrow = random.randrange(1, 5001)

                frenchdata = ninjabot.ninjabotsql.sql_frenchselect(self.settings.frenchallsql,(randomrow,))

                frenchembed=nextcord.Embed(title="Ninjabot French", description="`What does this word mean?`", color=nextcord.Color.blue())
                frenchembed.add_field(name="French Word", value='`{}`'.format(frenchdata[0][1]), inline=True)
                frenchembed.add_field(name="Type", value=frenchdata[0][2], inline=True)
                frenchembed.add_field(name="Example Sentence", value=frenchdata[0][3], inline=False)
                
                if prefix == 'resume':

                    await message.send(embed=frenchembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.frenchwrite,(frenchdata[0][4],frenchdata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                
                else:

                    await message.channel.send(embed=frenchembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.frenchwrite,(frenchdata[0][4],frenchdata[0][0],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')   
                if not userinput.startswith(prefix):
                    freeanswer = 1    

            elif prefix == 'timesup':
                frenchdata = ninjabot.ninjabotsql.sql_select(self.settings.frenchanswersql,(message.id,))
                revealdata = ninjabot.ninjabotsql.sql_frenchselect(self.settings.frenchreveal,(frenchdata[0][1],))
                
                frenchembed=nextcord.Embed(title="Ninjabot French", description='`Times up!`', color=nextcord.Color.red())
                frenchembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][4]), inline=False)
                frenchembed.add_field(name="French Word", value=revealdata[0][1], inline=True)
                frenchembed.add_field(name="Type", value=revealdata[0][2], inline=True)
                frenchembed.add_field(name="Example Sentence", value=revealdata[0][3], inline=True)
                frenchembed.add_field(name="English Sentence", value=revealdata[0][5], inline=False)            

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.frenchstopsql,(message.id,)) 

                await message.send(embed=frenchembed) 

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'french',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New French starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. French is now stopped.')

            elif prefix == 'resume':
                await newgame(prefix)

            if userinput == fscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.frenchgetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a French score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.french or userinput == self.settings.frenchhelp:
                
                await message.channel.send(embed=frenchhelpembed)

            elif userinput == fl or userinput == fs:
                
                await newgame(prefix)

                if userinput == fl:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(fs,fl))

            elif userinput == gamestop and gamemode:
                frenchdata = ninjabot.ninjabotsql.sql_select(self.settings.frenchanswersql,(userchannel,))
                revealdata = ninjabot.ninjabotsql.sql_frenchselect(self.settings.frenchreveal,(frenchdata[0][1],))
                
                frenchembed=nextcord.Embed(title="Ninjabot French", description='`Ninjabot French is now stopped.`', color=nextcord.Color.red())
                frenchembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][4]), inline=False)
                frenchembed.add_field(name="French Word", value=revealdata[0][1], inline=True)
                frenchembed.add_field(name="Type", value=revealdata[0][2], inline=True)
                frenchembed.add_field(name="Example Sentence", value=revealdata[0][3], inline=True)
                frenchembed.add_field(name="English Sentence", value=revealdata[0][5], inline=False)
                await message.channel.send(embed=frenchembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.frenchstopsql,(userchannel,))            
                    
            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                frenchdata = ninjabot.ninjabotsql.sql_select(self.settings.frenchanswersql,(userchannel,))
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                if frenchdata[0][0]:
                
                    if similar(useranswer,frenchdata[0][0].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in frenchdata[0][0].split('; ')):
                        
                        revealdata = ninjabot.ninjabotsql.sql_frenchselect(self.settings.frenchreveal,(frenchdata[0][1],))
                        
                        frenchembed=nextcord.Embed(title="Ninjabot French", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        frenchembed.add_field(name="Answer", value='`{}`'.format(revealdata[0][4]), inline=False)
                        frenchembed.add_field(name="French Word", value=revealdata[0][1], inline=True)
                        frenchembed.add_field(name="Type", value=revealdata[0][2], inline=True)
                        frenchembed.add_field(name="Example Sentence", value=revealdata[0][3], inline=True)
                        frenchembed.add_field(name="English Sentence", value=revealdata[0][5], inline=False)
                        await message.channel.send(embed=frenchembed)

                        ninjabot.ninjabotsql.sql_insert(self.settings.frenchstopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.frenchsetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'french',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New French starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'french' in useranswer.lower() or 'fren' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop French.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop French.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))