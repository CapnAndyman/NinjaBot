import nextcord
import re
import time
import asyncio
import sys, os
from difflib import SequenceMatcher

class Ninjabotriddle:
    async def ninjabotriddle(self,ninjabot,message,gamemode,prefix):
        
        try:
        
            self.settings = ninjabot.settings

            rscore = prefix + 'rscore'
            rl = prefix + 'riddle'
            rs = prefix + 'ridd'
            gamestop = prefix + 'stop'

            riddlehelpembed=nextcord.Embed(title="NinjaBot Riddle", description="More Information")
            riddlehelpembed.add_field(name="Playing", value='Once you type `{0}riddle` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}music` if you think the answer is music.'.format(prefix))
            riddlehelpembed.add_field(name="Scoring", value='Type `{}rscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

            def similar(a, b):
                return SequenceMatcher(None, a, b).ratio()

            async def newgame(prefix):

                riddledata = ninjabot.ninjabotsql.sql_riddleselect(self.settings.riddlerandom)

                riddleembed=nextcord.Embed(title="Ninjabot Riddle", description="Here is your riddle.", color=nextcord.Color.blue())
                riddleembed.add_field(name="Riddle", value='`{}`'.format(riddledata[0][0]), inline=True)
                
                if prefix == 'resume':

                    await message.send(embed=riddleembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.riddlewrite,(riddledata[0][0],riddledata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                
                else:

                    await message.channel.send(embed=riddleembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.riddlewrite,(riddledata[0][0],riddledata[0][1],time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))


            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')      
                if not userinput.startswith(prefix):
                    freeanswer = 1 

            elif prefix == 'timesup':
                riddledata = ninjabot.ninjabotsql.sql_select(self.settings.riddleanswersql,(message.id,))
                
                riddleembed=nextcord.Embed(title="Ninjabot Riddle", description='`Times up!`', color=nextcord.Color.red())
                riddleembed.add_field(name="Riddle", value='{}'.format(riddledata[0][0]), inline=False)
                riddleembed.add_field(name="Answer", value='`{}`'.format(riddledata[0][1]), inline=False)            

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.riddlestopsql,(message.id,))  

                await message.send(embed=riddleembed)

                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'riddle',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Riddle starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Riddle is now stopped.')  

            elif prefix == 'resume':
                await newgame(prefix)          

            if userinput == rscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.riddlegetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a Riddle score of '.format(message) + str(userscore[0][0]))

            elif userinput == self.settings.riddle:
                
                await message.channel.send(embed=riddlehelpembed)

            elif userinput == rl or userinput == rs:

                await newgame(prefix)

                if userinput == rl:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(rs,rl))

            elif userinput == gamestop and gamemode:
                riddledata = ninjabot.ninjabotsql.sql_select(self.settings.riddleanswersql,(userchannel,))
                
                riddleembed=nextcord.Embed(title="Ninjabot Riddle", description='`Ninjabot Riddle is now stopped.`', color=nextcord.Color.red())
                riddleembed.add_field(name="Riddle", value='{}'.format(riddledata[0][0]), inline=False)
                riddleembed.add_field(name="Answer", value='`{}`'.format(riddledata[0][1]), inline=False)
                await message.channel.send(embed=riddleembed)
                
                ninjabot.ninjabotsql.sql_insert(self.settings.riddlestopsql,(userchannel,))            
                    
            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                riddledata = ninjabot.ninjabotsql.sql_select(self.settings.riddleanswersql,(userchannel,))
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                if riddledata[0][1]:
                
                    if similar(useranswer,riddledata[0][1].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in re.split('(),"',riddledata[0][1])):
                                    
                        riddleembed=nextcord.Embed(title="Ninjabot Riddle", description='`That is correct` <@{0.author.id}>! You win one point!'.format(message), color=nextcord.Color.green())
                        riddleembed.add_field(name="Riddle", value='{}'.format(riddledata[0][0]), inline=False)
                        riddleembed.add_field(name="Answer", value='`{}`'.format(riddledata[0][1]), inline=False)
                        await message.channel.send(embed=riddleembed)

                        ninjabot.ninjabotsql.sql_insert(self.settings.riddlestopsql,(userchannel,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.riddlesetscore,(userid,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'riddle',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Riddle starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(prefix))

                    else:
                        if not freeanswer:
                            if 'riddle' in useranswer.lower() or 'ridd' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Riddle.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Riddle.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))