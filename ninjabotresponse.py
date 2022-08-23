import nextcord
import time
import sys, os


class Ninjabotresponse:

    async def ninjabotresponse(self,ninjabot,message,syllcount,gamemode,prefix,thisisatest):

        self.settings = ninjabot.settings
    
        usermessage = ''
        userchannel = ''

        if not prefix == 'timesup' and not prefix == 'resume':
            usermessage = '{0.content}'.format(message).lower()
            userchannel = '{0.channel.id}'.format(message)
            try:
                await ninjabot.startupchannel.send('Channel {} `{}`'.format(userchannel,usermessage))
            except:
                print('failed to send message to startup')

        prefixstop = prefix + 'stop'
        define = prefix + 'define'
        prefixninja = prefix + 'ninjabot'
        prefixninjahelp = prefix + 'ninjabot help'
        dice = prefix + 'dice'
        lt = prefix + 'trivia'
        ltscore = prefix + 'tscore'
        lts = prefix + 'triv'
        tlist = [lt,ltscore,lts]
        lh = prefix + 'hangman'
        lhscore = prefix + 'hscore'
        lhs = prefix + 'hang'
        hlist = [lh,lhscore,lhs]
        lk = prefix + 'kanji'
        lkscore = prefix + 'kscore'
        lks = prefix + 'kanj'
        klist = [lk,lkscore,lks]
        lasl = prefix + 'asl'
        laslscore = prefix + 'aslscore'
        asllist = [lasl,laslscore]
        lkn = prefix + 'katakana'
        lknscore = prefix + 'knscore'
        lkns = prefix + 'kana'
        lkna = prefix + 'kata'
        knlist = [lkn,lknscore,lkns,lkna]
        lj = prefix + 'japanese'
        ljscore = prefix + 'jscore'
        ljs = prefix + 'japa'
        jlist = [lj,ljscore,ljs]
        lf = prefix + 'french'
        lfscore = prefix + 'fscore'
        lfs = prefix + 'fren'
        flist = [lf,lfscore,lfs]
        lgn = prefix + 'hiragana'
        lgnscore = prefix + 'gnscore'
        lgns = prefix + 'gana'
        lgna = prefix + 'hira'
        gnlist = [lgn,lgnscore,lgns,lgna]
        ln = prefix + 'nihongo'
        lnscore = prefix + 'nscore'
        lns = prefix + 'niho'
        nlist = [ln,lnscore,lns]
        lm = prefix + 'minesweeper'
        lmscore = prefix + 'mscore'
        lms = prefix + 'mine'
        mlist = [lm,lmscore,lms]
        lr = prefix + 'riddle'
        lrscore = prefix + 'rscore'
        lrs = prefix + 'ridd'
        rlist = [lr,lrscore,lrs]
        lffs = prefix + 'ffl'
        lff = prefix + 'fflookup'
        fflist = [lff,lffs]

        try:
            # if prefix != 'timesup' and prefix != 'resume' and thisisatest == 1:
            #     await ninjabot.startupchannel.send('{0.author.id} {0.author.name} sent message with content {0.content}'.format(message))
                    
            # if prefix == 'timesup' and thisisatest == 1:
            #     await ninjabot.startupchannel.send('{} ended in channel ID {}'.format(gamemode,message.id))            
            if usermessage == self.settings.ninjabothello:
                await message.channel.send('Hello {0.author.name}'.format(message))
            
            if usermessage == prefixstop:
                stopvalue = ninjabot.ninjabotsql.sql_select(self.settings.checkstop,(userchannel,))[0]
                if stopvalue[0] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(0,None,None,userchannel))
                    await message.channel.send('Game is now stopped.')
                    gamemode = None

            if usermessage.startswith(self.settings.ninjabotprefix):
                if len(usermessage.split(' ')) == 3 and len(usermessage.split(' ')[-1]) <= 4:
                    ninjabot.ninjabotsql.sql_insert(self.settings.setprefix,(usermessage.split(' ')[-1],userchannel))
                    await message.channel.send('Prefix for this channel is now ' + usermessage.split(' ')[-1])
                elif usermessage == 'ninjabot prefix':
                    await message.channel.send('Please provide a new prefix after that command like `ninjabot prefix ?`')
                else:
                    await message.channel.send('Sorry, I cannot use that prefix!')
            
            elif usermessage.startswith(self.settings.ninjabotschedule):
                await ninjabot.ninjabotschedule.ninjabotschedule(ninjabot,message)
            
            elif usermessage.startswith('ninjabot roles'):
                await ninjabot.ninjabotroles.ninjabotroles(ninjabot,message)

            elif usermessage == 'ninjabot left':
                await ninjabot.ninjabotleft.ninjabotleft(ninjabot,message)

            elif usermessage.split(' ')[0] in fflist:
                await ninjabot.ninjabotffxiv.ninjabotffxiv(ninjabot,message,prefix)

            elif usermessage == self.settings.ninjabothelp or \
                usermessage == self.settings.longcommand or \
                usermessage == prefixninja or \
                usermessage == prefixninjahelp:
                
                ninjabothelpinfosimple=nextcord.Embed(title="Ninjabot Help", description='The current set prefix for this channel is `{0}`\r\nYou can respond to any game with `{0}` followed by your answer.\r\nMost games have 4-character shortcuts like `{0}hang` for Hangman.'.format(prefix), color=nextcord.Color.green())
                ninjabothelpinfosimple.add_field(name="Fun Games", value='`{0}hangman`\r\n`{0}trivia`\r\n`{0}dice`\r\n`{0}minesweeper`\r\n`{0}riddle`'.format(prefix), inline=True)
                ninjabothelpinfosimple.add_field(name="Japanese Games", value='`{0}hiragana`\r\n`{0}katakana`\r\n`{0}kanji`\r\n`{0}japanese`\r\n`{0}nihongo`'.format(prefix), inline=True)
                ninjabothelpinfosimple.add_field(name="Other", value='`{0}asl`\r\n`{0}french`\r\n`{0}define`'.format(prefix), inline=True)
                ninjabothelpinfosimple.add_field(name="Game Timer", value="Enter `ninjabot timer` to Enable/Disable the game timer for the current channel.\r\nDisable this if you do not want games to expire on their own.", inline=True)
                ninjabothelpinfosimple.add_field(name="Nonstop", value="Enter `ninjabot nonstop` to Enable/Disable nonstop gameplay for the current channel.\r\nDisable this if you do not want to start a new game when you win.", inline=True)                
                ninjabothelpinfosimple.add_field(name="Haiku", value="Enter `ninjabot haiku` to Enable/Disable Ninjabot Haiku for the current channel.", inline=True)
                ninjabothelpinfosimple.add_field(name="More Help", value='Type `ninjabot` followed by the game. Example: `ninjabot hangman`', inline=False)
                ninjabothelpinfosimple.add_field(name="Change Prefix", value="Enter `ninjabot prefix` followed by a new prefix. This is per channel.\r\nExample: `ninjabot prefix ?` if you want to use a question mark instead.", inline=False)
                ninjabothelpinfosimple.add_field(name="Scheduling", value="Ninjabot scheduling feature. Enter `ninjabot schedule` for more info.", inline=True)
                ninjabothelpinfosimple.add_field(name="Delete User Data", value="Enter `ninjabot delete` to delete your saved user data.", inline=True)
                ninjabothelpinfosimple.add_field(name="Ninjabot Privacy Policy", value="Enter `ninjabot policy` to see how we handle your data.", inline=False)
               
                await message.channel.send(embed=ninjabothelpinfosimple)
            
            elif usermessage == 'ninjabot policy' or usermessage == 'ninjabot privacy policy':

                ninjabotpolicy=nextcord.Embed(title="Ninjabot Privacy Policy", description='Ninjabot and its creators value privacy and want to be very clear how we handle your information. We do not record anything beyond what is necessary for Ninjabot to function.', color=nextcord.Color.green())
                ninjabotpolicy.add_field(name="Personal Information", value='Ninjabot and its creators will never share or sell your personal information unless required by law. Please see the next section to see what exactly is saved.', inline=False)
                ninjabotpolicy.add_field(name="Recorded Data", value='Ninjabot saves your Discord user ID, Ninjabot game scores, and any scheduled announcements you have created with Ninjabots scheduling feature.', inline=False)
                ninjabotpolicy.add_field(name="Limitations", value='The data that Ninjabot receives comes directly from Discord and is allowed to view such data. Ninjabot and its creators will never ask for information such as real name, address, password, or anything of a sensitive nature.', inline=False)
                ninjabotpolicy.add_field(name="Opting Out", value="If you would like to opt out and have Ninjabot remove your saved user ID, scores, and any scheduled announcements you have created using Ninjabots scheduling feature, please enter `ninjabot delete`.", inline=False)
                ninjabotpolicy.add_field(name="Changes", value='This policy is subject to change at any time. If you have any questions or suggestions, please visit our support server located here: https://discord.gg/gv8anXX', inline=False)

                await message.channel.send(embed=ninjabotpolicy)
            
            elif usermessage == self.settings.ninjabotsupport:
                await message.channel.send(embed=self.settings.supportinfo)
            
            elif usermessage == self.settings.haiku:
                await ninjabot.ninjabothaiku.ninjabothaiku(ninjabot,message)

            elif usermessage == self.settings.timer:
                timerstatus = ninjabot.ninjabotsql.sql_select(self.settings.timerchecksql,(userchannel,))
                if timerstatus[0][0] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.timerswapsql,('0',userchannel))
                    await message.channel.send('Game Timer is now off for this channel.')
                elif timerstatus[0][0] == 0:
                    ninjabot.ninjabotsql.sql_insert(self.settings.timerswapsql,('1',userchannel))
                    await message.channel.send('Game Timer is now on for this channel.')

            elif usermessage == self.settings.nonstop:
                nonstopstatus = ninjabot.ninjabotsql.sql_select(self.settings.checknonstop,(userchannel,))
                if nonstopstatus[0][0] == 1:
                    ninjabot.ninjabotsql.sql_insert(self.settings.swapnonstop,('0',userchannel))
                    await message.channel.send('Nonstop gameplay is now off for this channel.')
                elif nonstopstatus[0][0] == 0:
                    ninjabot.ninjabotsql.sql_insert(self.settings.swapnonstop,('1',userchannel))
                    await message.channel.send('Nonstop gameplay is now on for this channel.')                


            elif usermessage == self.settings.channelinfo:
                    await message.channel.send(self.settings.channelinforesponse.format(message))

            elif syllcount == 17:
                await ninjabot.ninjabothaiku.ninjabothaiku(ninjabot,message)
            
            elif gamemode or prefix == 'timesup' or prefix == 'resume':

                if gamemode == 'trivia':
                    await ninjabot.ninjabottrivia.ninjabottrivia(ninjabot,message,gamemode,prefix)

                elif gamemode == 'french':
                    await ninjabot.ninjabotfrench.ninjabotfrench(ninjabot,message,gamemode,prefix)

                elif gamemode == 'hangman':
                    await ninjabot.ninjabothangman.ninjabothangman(ninjabot,message,gamemode,prefix)

                elif gamemode == 'kana':
                    await ninjabot.ninjabotkana.ninjabotkana(ninjabot,message,gamemode,prefix)

                elif gamemode == 'gana':
                    await ninjabot.ninjabotgana.ninjabotgana(ninjabot,message,gamemode,prefix)

                elif gamemode == 'kanji':
                    await ninjabot.ninjabotkanji.ninjabotkanji(ninjabot,message,gamemode,prefix)

                elif gamemode == 'asl':
                    await ninjabot.ninjabotasl.ninjabotasl(ninjabot,message,gamemode,prefix)

                elif gamemode == 'japanese':
                    await ninjabot.ninjabotjapanese.ninjabotjapanese(ninjabot,message,gamemode,prefix)

                elif gamemode == 'nihongo':
                    await ninjabot.ninjabotnihongo.ninjabotnihongo(ninjabot,message,gamemode,prefix)

                elif gamemode == 'minesweeper':
                    await ninjabot.ninjabotminesweeper.ninjabotminesweeper(ninjabot,message,gamemode,prefix)

                elif gamemode == 'riddle':
                    await ninjabot.ninjabotriddle.ninjabotriddle(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.ninjabotdice) or \
                usermessage.startswith(dice):
                await ninjabot.ninjabotdice.ninjabotdice(ninjabot,message,prefix,thisisatest)

            elif usermessage.startswith(self.settings.ninjabottrivia) or \
                usermessage.split(' ')[0] in tlist:
                await ninjabot.ninjabottrivia.ninjabottrivia(ninjabot,message,gamemode,prefix)
            
            elif usermessage.startswith(self.settings.french) or \
                usermessage.split(' ')[0] in flist:
                await ninjabot.ninjabotfrench.ninjabotfrench(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.ninjabothangman) or \
                usermessage.split(' ')[0] in hlist:
                await ninjabot.ninjabothangman.ninjabothangman(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.kana) or \
                usermessage.split(' ')[0] in knlist:
                await ninjabot.ninjabotkana.ninjabotkana(ninjabot,message,gamemode,prefix)    

            elif usermessage.startswith(self.settings.gana) or \
                usermessage.split(' ')[0] in gnlist:
                await ninjabot.ninjabotgana.ninjabotgana(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.kanji) or \
                usermessage.split(' ')[0] in klist:
                await ninjabot.ninjabotkanji.ninjabotkanji(ninjabot,message,gamemode,prefix)
                    
            elif usermessage.startswith(self.settings.asl) or \
                usermessage.split(' ')[0] in asllist:
                await ninjabot.ninjabotasl.ninjabotasl(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.japanese) or \
                usermessage.split(' ')[0] in jlist:
                await ninjabot.ninjabotjapanese.ninjabotjapanese(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.nihongo) or \
                usermessage.split(' ')[0] in nlist:
                await ninjabot.ninjabotnihongo.ninjabotnihongo(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.minesweeper) or \
                usermessage.split(' ')[0] in mlist:
                await ninjabot.ninjabotminesweeper.ninjabotminesweeper(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(self.settings.riddle) or \
                usermessage.split(' ')[0] in rlist:
                await ninjabot.ninjabotriddle.ninjabotriddle(ninjabot,message,gamemode,prefix)

            elif usermessage.startswith(define):
                await ninjabot.ninjabotdictionary.ninjabotdictionary(ninjabot,message,prefix)
            
            elif usermessage.startswith(self.settings.ninjabotdelete):
                if usermessage == self.settings.ninjabotdelete:
                    await message.channel.send('WARNING!!!\r\nThis command is used for COMPLETELY clearing your saved user information which includes game scores and scheduled events you have made.\r\nTo finalize this task, please type:\r\n`ninjabot delete confirm`')
                if usermessage == self.settings.ninjabotdeleteconfirm:
                    try:
                        ninjabot.ninjabotsql.sql_insert(self.settings.clearuserdata,(message.author.id,))
                        ninjabot.ninjabotsql.sql_insert(self.settings.clearuserschedule,(message.author.id,))
                        await message.channel.send('Scores and schedule have been cleared for <@{0.author.id}>.'.format(message))

                    except:
                        await message.channel.send('Something went wrong with deleting user data for {}, please run the command one more time!'.format(message.author.name))
                        await ninjabot.startupchannel.send('Ninjabot failed to delete user data for {}. @here\r\n{}\r\n{}\r\n{}'.format(str(message.author.id),str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
            
            elif usermessage.startswith(self.settings.longcommand):
                await message.channel.send(self.settings.refertohelp.format(message))
        
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}\r\nChannel {}'.format(exc_tb.tb_lineno,userchannel))))