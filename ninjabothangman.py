import json
import random
import urllib.request
import nextcord
from pathlib import Path
import os.path
from os import path
import string
import sys, os

class Ninjabothangman:
    async def ninjabothangman(self,ninjabot,message,gamemode,prefix):

        try:

            self.settings = ninjabot.settings
            userchannel = '{0.channel.id}'.format(message)
            hangmandata = list(ninjabot.ninjabotsql.sql_select(self.settings.hangmandatasql,(userchannel,))[0])
            userid = '{0.author.id}'.format(message)
            userscore = ninjabot.ninjabotsql.sql_select(self.settings.gethangmanscore, (userid,))[0][0]
            url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
            words = json.loads(url.read())
            userinput = '{0.content}'.format(message).lower()
            
            useranswer = ''
            
            hscore = prefix + 'hscore'
            hl = prefix + 'hangman'
            hs = prefix + 'hang'
            gamestop = prefix + 'stop'

            hangmanhelpembed=nextcord.Embed(title="Ninjabot Hangman", description="More Information")
            hangmanhelpembed.add_field(name="Playing", value='Once you type `{0}hangman` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}a` if you think the answer contains the letter a. You may also attempt to guess whole words.'.format(prefix), inline=False)
            hangmanhelpembed.add_field(name="Scoring", value="Type `{}hscore` to see your score. You recieve points for answering correctly in winning games.".format(prefix), inline=False)

            if gamemode:

                useranswer = userinput.replace(prefix,'').replace(' ','')

            if userinput == hscore:
                await message.channel.send('<@{0.author.id}> has a Hangman score of '.format(message) + str(userscore))

            
            elif userinput == self.settings.ninjabothangman or userinput == self.settings.ninjabothangmanhelp:
                await message.channel.send(embed=hangmanhelpembed)

            elif userinput == hs or userinput == hl:

                blankstring = ''
                newword = random.choice(words).replace('-','')
                newwordcount = len(newword)
                while newwordcount != 0:
                    blankstring = blankstring + '-'
                    newwordcount = newwordcount - 1


                ninjabot.ninjabotsql.sql_insert(self.settings.hangmanstartsql,(newword, blankstring, userchannel))

                attachfile = nextcord.File("data/images/hangninja0.png", filename="image.png")

                hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="`Here is your word!`", color=nextcord.Color.blue())
                hangmaninfo.add_field(name="Word", value='`{}`'.format(blankstring), inline=False)
                hangmaninfo.add_field(name="Word Length", value=str(len(newword.replace('"',''))), inline=False)            
                hangmaninfo.set_image(url="attachment://image.png")


                await message.channel.send(file=attachfile, embed=hangmaninfo)

                if userinput == hl:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(hs,hl))

            elif userinput == gamestop and gamemode:

                await message.channel.send('The word was `{}`'.format(hangmandata[0]))
                ninjabot.ninjabotsql.sql_insert(self.settings.hangmannullsql,(userchannel,))

            elif gamemode:

                if len(useranswer) > 1 and userinput.startswith(prefix):
                    if useranswer.lower() == hangmandata[0].lower():
                        if hangmandata[4] == 'NONE':
                            hangmandata[4] = userid
                        elif hangmandata[4] != 'NONE' and userid not in hangmandata[4]:
                            hangmandata[4] = hangmandata[4] + '~' + userid
                        await message.channel.send(
                            ('Congrats <@{0.author.id}>, you are correct.\r\nThe answer was `'.format(message)
                                + hangmandata[0] 
                                + "`\r\nAll successful players have recieved one point!\r\nHope to see you again!"))
                        if '~' in hangmandata[4]:
                            for player in hangmandata[4].split('~'):

                                currentscore = ninjabot.ninjabotsql.sql_select(self.settings.gethangmanscore, (player,))[0][0]
                                currentscore = int(currentscore) + 1
                                
                                values = (currentscore,player)
                                ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanscore,values)

                        elif '~' not in hangmandata[4]:
                            
                            player = hangmandata[4]
                            currentscore = int(userscore) + 1
                            values = (currentscore,player)
                            ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanscore,values)

                        ninjabot.ninjabotsql.sql_insert(self.settings.hangmannullsql,(userchannel,))

                    elif useranswer.lower() != hangmandata[0].lower():
                        hangmandata[3] = str(int(hangmandata[3]) + 1)
                        if int(hangmandata[3]) >= 6:

                            attachfile = nextcord.File(self.settings.hangmen[6], filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="`YOU LOSE!`", color=nextcord.Color.red())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[0]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)                        
                            ninjabot.ninjabotsql.sql_insert(self.settings.hangmannullsql,(userchannel,))

                        elif int(hangmandata[3]) < 6:

                            attachfile = nextcord.File(self.settings.hangmen[int(hangmandata[3])], filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="<@{0.author.id}> `Incorrect!`".format(message), color=nextcord.Color.purple())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[1]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)
                            if 'hangman' in useranswer or 'hang' in useranswer:
                                await message.channel.send("Make sure you are responding with {0} followed by your answer. Example: `{0}e`".format(prefix))
                            ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanbadword,(hangmandata[3],userchannel))

                        
                    
                elif len(useranswer) == 1:
                    if useranswer in hangmandata[1] or useranswer in hangmandata[2]:
                        await message.channel.send(
                            ('Sorry <@{0.author.id}>, that letter has already been guessed!').format(message))

                    elif useranswer in hangmandata[0]:
                        if hangmandata[4] == 'NONE':
                            hangmandata[4] = userid
                        elif hangmandata[4] != 'NONE' and userid not in hangmandata[4]:
                            hangmandata[4] = hangmandata[4] + '~' + userid
                        
                        whichletter = 0
                        letterlist = list(hangmandata[1])
                        for letter in hangmandata[0]:
                            if useranswer == letter:
                                letterlist[whichletter] = useranswer
                            whichletter = whichletter + 1
                        hangmandata[1] = ''.join(letterlist)
                        ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmangoodletter,(hangmandata[1],hangmandata[4],userchannel))


                        if '-' in hangmandata[1]:

                            attachfile = nextcord.File(self.settings.hangmen[int(hangmandata[3])], filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="<@{0.author.id}> `That letter is right!`".format(message), color=nextcord.Color.green())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[1]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)  
                        
                        elif '-' not in hangmandata[1]:

                            attachfile = nextcord.File(self.settings.hangmen[int(hangmandata[3])], filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description='`YOU WON!`\r\nAll successful players have recieved one point!', color=nextcord.Color.gold())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[1]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)
                            if '~' in hangmandata[4]:
                                for player in hangmandata[4].split('~'):
                                    
                                    currentscore = ninjabot.ninjabotsql.sql_select(self.settings.gethangmanscore, (player,))[0][0]
                                    currentscore = int(currentscore) + 1
                                    
                                    values = (currentscore,player)
                                    ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanscore,values)

                            elif '~' not in hangmandata[4]:
                            
                                player = hangmandata[4]
                                currentscore = int(userscore) + 1
                                values = (currentscore,player)
                                ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanscore,values)
                            
                            ninjabot.ninjabotsql.sql_insert(self.settings.hangmannullsql,(userchannel,))
                    
                    elif useranswer not in list(string.ascii_lowercase)[0:26]:
                        await message.channel.send("Sorry {}, that is not a valid letter.".format(message.author.mention))
                    
                    elif useranswer not in hangmandata[0]:
                        hangmandata[3] = str(int(hangmandata[3]) + 1)
                        if int(hangmandata[3]) >= 6:
                            if hangmandata[2] == 'NONE':
                                hangmandata[2] = useranswer
                            else:
                                hangmandata[2] = hangmandata[2] + useranswer

                            attachfile = nextcord.File("data/images/hangninja6.png", filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="`YOU LOSE!`", color=nextcord.Color.red())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[0]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)                        
                            ninjabot.ninjabotsql.sql_insert(self.settings.hangmannullsql,(userchannel,))

                        elif int(hangmandata[3]) < 6:
                            if hangmandata[2] == 'NONE':
                                hangmandata[2] = useranswer
                            else:
                                hangmandata[2] = hangmandata[2] + useranswer

                            attachfile = nextcord.File(self.settings.hangmen[int(hangmandata[3])], filename="image.png")
                            hangmaninfo=nextcord.Embed(title="Ninjabot Hangman", description="<@{0.author.id}> `Incorrect!`".format(message), color=nextcord.Color.purple())
                            
                            hangmaninfo.add_field(name="Word", value='`{}`'.format(hangmandata[1]), inline=False)
                            hangmaninfo.add_field(name="Bad Letters", value=hangmandata[2], inline=False)
                            hangmaninfo.set_image(url="attachment://image.png")
                            await message.channel.send(file=attachfile, embed=hangmaninfo)
                            if 'hangman' in useranswer or 'hang' in useranswer:
                                await message.channel.send("Make sure you are responding with {0} followed by your answer. Example: `{0}e`".format(prefix))

                            ninjabot.ninjabotsql.sql_insert(self.settings.updatehangmanbadletter,(hangmandata[2],hangmandata[3],userchannel))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))