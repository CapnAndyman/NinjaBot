import random
import nextcord
import datetime
import time
import re
import asyncio
import sys, os
from difflib import SequenceMatcher

class Ninjabottrivia:
    async def ninjabottrivia(self,ninjabot,message,gamemode,prefix):

        try:

            self.settings = ninjabot.settings
            
            timeformat = '%Y-%m-%d %H:%M:%S'

            tscore = prefix + 'tscore'
            tl = prefix + 'trivia'
            ts = prefix + 'triv'
            gamestop = prefix + 'stop'

            triviahelpembed=nextcord.Embed(title="Ninjabot Trivia", description="More Information")
            triviahelpembed.add_field(name="Playing", value='Once you type `{0}trivia` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}music` if you think the answer is music.'.format(prefix), inline=False)
            triviahelpembed.add_field(name="Scoring", value='Type `{}tscore` to see your total score. You recieve points for answering correctly within 30 seconds.'.format(prefix), inline=False)

            userchannel = ''
            userid = ''
            userinput = ''
            useranswer = ''
            freeanswer = ''

            def similar(a, b):
                return SequenceMatcher(None, a, b).ratio()

            async def newgame(prefix):

                randomrow = random.randrange(1, 198804)
                chosen_row = ninjabot.ninjabotsql.sql_triviaselect(self.settings.newtriviaquestion,(randomrow,))[0]
                
                questionembed=nextcord.Embed(title="Ninjabot Trivia", description="`Here is your question!`", color=nextcord.Color.blue())
                questionembed.set_author(name="Your Host - Ninja Trebek", icon_url='https://cdn.discordapp.com/emojis/761657815219175465.png')
                questionembed.add_field(name="Category", value=chosen_row[0], inline=False)
                questionembed.add_field(name="Value", value=('$' + str(chosen_row[1])), inline=False)
                questionembed.add_field(name="Question", value='`{}`'.format(chosen_row[2]), inline=False)

                if prefix == 'resume':

                    await message.send(embed=questionembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.triviastartsql,(chosen_row[3],time.strftime('%Y-%m-%d %H:%M:%S'),randomrow,message.id))

                else:

                    await message.channel.send(embed=questionembed)
                    ninjabot.ninjabotsql.sql_insert(self.settings.triviastartsql,(chosen_row[3],time.strftime('%Y-%m-%d %H:%M:%S'),randomrow,userchannel))

            if not prefix == 'timesup' and not prefix == 'resume':
                userchannel = '{0.channel.id}'.format(message)
                userid = '{0.author.id}'.format(message)
                userinput = '{0.content}'.format(message).lower()
                useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')
                if not userinput.startswith(prefix):
                    freeanswer = 1

            elif prefix == 'timesup':
                questiondata = list(ninjabot.ninjabotsql.sql_select(self.settings.triviaanswersql,(message.id,))[0])
                answerdata = ninjabot.ninjabotsql.sql_triviaselect(self.settings.newtriviaquestion,(questiondata[1],))[0]
                questionembed=nextcord.Embed(title="Ninjabot Trivia", description="`Times Up!`", color=nextcord.Color.red())
                questionembed.set_author(name="Your Host - Ninja Trebek", icon_url='https://cdn.discordapp.com/emojis/761657815219175465.png')
                questionembed.add_field(name="Category", value=answerdata[0], inline=False)
                questionembed.add_field(name="Value", value=('$' + str(answerdata[1])), inline=False)
                questionembed.add_field(name="Question", value=answerdata[2], inline=False)
                questionembed.add_field(name="Answer", value='`{}`'.format(answerdata[3]), inline=False)

                checkresume = ninjabot.ninjabotsql.sql_select(self.settings.checkresume,(message.id,))[0]

                ninjabot.ninjabotsql.sql_insert(self.settings.trivianullsql,(message.id,))

                await message.send(embed=questionembed)
                
                if checkresume[0] == 1 and checkresume[1] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'trivia',time.strftime('%Y-%m-%d %H:%M:%S'),message.id))
                    prefix = ninjabot.ninjabotsql.sql_select(self.settings.getprefix,(message.id,))[0][0]
                    await message.send('New Trivia starts in 3 seconds. Type `{}stop` if you would like to stop.'.format(str(prefix)))
                elif checkresume[0] == 0 and checkresume[1] == 1:
                    await message.send('Nobody answered. Trivia is now stopped.')

            elif prefix == 'resume':
                await newgame(prefix)

            if userinput == tscore:
                await message.channel.send('<@{0.author.id}> has a Trivia score of $'.format(message) + str(ninjabot.ninjabotsql.sql_select(self.settings.gettriviascore,(userid,))[0][0]))
        
            elif userinput == self.settings.ninjabottrivia or userinput == self.settings.ninjabottriviahelp:

                await message.channel.send(embed=triviahelpembed)
            
            elif userinput == ts or userinput == tl:

                await newgame(prefix)

                if userinput == tl:
                    await message.channel.send('Reminder: you can also type `{}` to start Trivia.'.format(ts))
                
            elif userinput == gamestop and gamemode:

                questiondata = list(ninjabot.ninjabotsql.sql_select(self.settings.triviaanswersql,(message.channel.id,))[0])
                answerdata = ninjabot.ninjabotsql.sql_triviaselect(self.settings.newtriviaquestion,(questiondata[1],))[0]
                questionembed=nextcord.Embed(title="Ninjabot Trivia", description="`Trivia is now stopped!`", color=nextcord.Color.red())
                questionembed.set_author(name="Your Host - Ninja Trebek", icon_url='https://cdn.discordapp.com/emojis/761657815219175465.png')
                questionembed.add_field(name="Category", value=answerdata[0], inline=False)
                questionembed.add_field(name="Value", value=('$' + str(answerdata[1])), inline=False)
                questionembed.add_field(name="Question", value=answerdata[2], inline=False)
                questionembed.add_field(name="Answer", value='`{}`'.format(answerdata[3]), inline=False)

                await message.channel.send(embed=questionembed)
                ninjabot.ninjabotsql.sql_insert(self.settings.trivianullsql,(userchannel,))

            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                questiondata = list(ninjabot.ninjabotsql.sql_select(self.settings.triviadatasql,(userchannel,))[0])
                answerdata = ninjabot.ninjabotsql.sql_triviaselect(self.settings.newtriviaquestion,(questiondata[2],))[0]
                nonstop = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))[0][0]

                answertime = datetime.datetime.today()
                oldtime = datetime.datetime.strptime(questiondata[1], timeformat)
                answerseconds = answertime - oldtime

                if questiondata[0]:
                
                    if similar(useranswer,questiondata[0].lower()) >= self.settings.difficulty or \
                        any((similar(useranswer,singleitem) >= self.settings.difficulty) for singleitem in re.split('(),',questiondata[0])):

                        if answerseconds.total_seconds() > 30:
                            questionembed=nextcord.Embed(title="Ninjabot Trivia", description='Congrats <@{0.author.id}>! `You are correct!`\r\nAnswer was not within 30 seconds.'.format(message), color=nextcord.Color.green())
                            questionembed.set_author(name="Your Host - Ninja Trebek", icon_url='https://cdn.discordapp.com/emojis/761657815219175465.png')
                            questionembed.add_field(name="Category", value=answerdata[0], inline=False)
                            questionembed.add_field(name="Value", value=('$' + str(answerdata[1])), inline=False)
                            questionembed.add_field(name="Question", value=answerdata[2], inline=False)
                            questionembed.add_field(name="Answer", value='`{}`'.format(answerdata[3]), inline=False)

                            await message.channel.send(embed=questionembed)
                        
                        elif answerseconds.total_seconds() <= 30:
                            questionembed=nextcord.Embed(title="Ninjabot Trivia", description='Congrats <@{0.author.id}>! `You are correct!`\r\nYou answered within 30 seconds!\r\nYour trivia score has been updated!'.format(message), color=nextcord.Color.gold())
                            questionembed.set_author(name="Your Host - Ninja Trebek", icon_url='https://cdn.discordapp.com/emojis/761657815219175465.png')
                            questionembed.add_field(name="Category", value=answerdata[0], inline=False)
                            questionembed.add_field(name="Value", value=('$' + str(answerdata[1])), inline=False)
                            questionembed.add_field(name="Question", value=answerdata[2], inline=False)
                            questionembed.add_field(name="Answer", value='`{}`'.format(answerdata[3]), inline=False)

                            currentscore = ninjabot.ninjabotsql.sql_select(self.settings.gettriviascore,(userid,))[0][0]
                            currentscore = int(currentscore) + int(answerdata[1])
                            ninjabot.ninjabotsql.sql_insert(self.settings.updatetriviascore,(currentscore,userid))

                            await message.channel.send(embed=questionembed)

                        ninjabot.ninjabotsql.sql_insert(self.settings.trivianullsql,(userchannel,))

                        if nonstop == 1:
                            ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(1,'trivia',time.strftime('%Y-%m-%d %H:%M:%S'),userchannel))
                            await message.channel.send('Congrats! New Trivia starts in 3 seconds.')

                        
                    else:
                        if not freeanswer:
                            if 'trivia' in useranswer.lower() or 'triv' in useranswer.lower():
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Trivia.\r\nMake sure you are responding with `{}` followed by your answer.'.format(prefix))
                            else:
                                await message.channel.send('Sorry <@{0.author.id}>, that is incorrect. Type `'.format(message) + prefix + 'stop` if you want to stop Trivia.')
                        ninjabot.ninjabotsql.sql_insert(self.settings.setresume,(userchannel,))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))