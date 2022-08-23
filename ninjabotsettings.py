import nextcord

class Ninjabotsettings:

    def __init__(self):
        
        self.difficulty = 0.7
        
        self.longcommand = 'ninjabot'
        self.shortcommand = '!'
        self.ninjabotannouncements = self.longcommand + ' announcements'
        
        self.ninjabothello = self.longcommand + ' hello'

        self.ninjabotdice = self.longcommand + ' dice'
        self.ninjabotdicehelp = self.longcommand + ' dice help'
        self.ninjabotd20 = 'd20'
        self.ninjabotd6 = 'd6'
        self.ninjabottoohigh = 'https://images.lost.ninja/dicetoohigh.jpg'
        self.ninjabotnegative = 'https://images.lost.ninja/dicenegative.jpg'
        self.dice = self.shortcommand + 'dice'

        self.simple = self.longcommand + ' simple'

        self.ninjabotprefix = self.longcommand + ' prefix'
        
        self.ninjabotdelete = self.longcommand + ' delete'
        self.ninjabotdeleteconfirm = self.longcommand + ' delete confirm'

        self.checkfflookup = '''SELECT search_data FROM ninjabot_fflookups WHERE message_id = ?'''
        self.addfflookup = '''INSERT INTO ninjabot_fflookups(message_id,search_data,date_added) VALUES(?,?,?)'''
        self.removefflookup = '''DELETE FROM ninjabot_left WHERE channel_id = ?'''
        
        self.checkleft = '''SELECT channel_id FROM ninjabot_left WHERE channel_id = ?'''
        self.getleftchannels = '''SELECT channel_id FROM ninjabot_left WHERE guild_id = ?'''
        self.removeleft = '''DELETE FROM ninjabot_left WHERE channel_id = ?'''
        self.addleft = '''INSERT INTO ninjabot_left(channel_id,guild_id,date_added) VALUES(?,?,?)'''
        
        self.removechannel = '''DELETE FROM ninjabot_channels WHERE channel_id = ?'''
        
        self.clearuserdata = '''DELETE FROM ninjabot_users WHERE user_id = ?'''
        self.clearuserschedule = '''DELETE FROM schedule WHERE user_id = ?'''
        
        self.getprefix = '''SELECT channel_prefix,game_mode FROM ninjabot_channels WHERE channel_id = ?'''
        self.setprefix = '''UPDATE ninjabot_channels SET channel_prefix = ? WHERE channel_id = ?'''
        
        self.gamemodesql = '''SELECT game_mode FROM ninjabot_channels WHERE channel_id = ?'''
        self.setsimplestatus = '''UPDATE ninjabot_channels SET simple_status = ? WHERE channel_id = ?'''
        
        self.setgamemodesql = '''UPDATE ninjabot_channels SET game_mode = ? WHERE channel_id = ?'''
        self.nullgamemodesql = '''UPDATE ninjabot_channels SET game_mode = NULL WHERE channel_id = ?'''

        self.addrolesql = '''INSERT INTO ninjabot_roles(message_id,role_id,channel_id,guild_id,date_added,emoji_id) VALUES(?,?,?,?,?,?)'''
        self.getrolesql = '''SELECT role_id FROM ninjabot_roles WHERE role_id = ?'''
        self.getrolemessage = '''SELECT role_id,guild_id FROM ninjabot_roles WHERE message_id = ? AND emoji_id = ?'''
        self.getallrolessql = '''SELECT message_id,role_id,channel_id,guild_id FROM ninjabot_roles'''
        self.removerolesql = '''DELETE FROM ninjabot_roles WHERE role_id = ?'''

        self.addrolepairs = '''INSERT INTO ninjabot_rolepairs(user_id,role_id,date_added) VALUES(?,?,?)'''
        self.removerolepairs = '''DELETE FROM ninjabot_rolepairs WHERE user_id = ? AND role_id = ?'''
        self.removeallrolepairs = '''DELETE FROM ninjabot_rolepairs WHERE role_id = ?'''
        self.getrolepairs = '''SELECT user_id FROM ninjabot_rolepairs WHERE role_id = ?'''

        self.checknonstop = '''SELECT game_nonstop FROM ninjabot_channels WHERE channel_id = ?'''
        self.swapnonstop = '''UPDATE ninjabot_channels SET game_nonstop = ? WHERE channel_id = ?'''  

        self.getactivegames = '''SELECT game_mode,game_time,channel_id,game_timer FROM ninjabot_channels WHERE game_mode != "hangman" AND game_mode != "minesweeper" AND game_mode IS NOT NULL AND game_timer != 0 AND stop_wait = 0'''
        self.getstoppedgames = '''SELECT game_mode,game_time,channel_id,game_timer,stop_wait,game_nonstop FROM ninjabot_channels WHERE game_mode != "hangman" AND game_mode != "minesweeper" AND game_nonstop = 1 AND game_mode IS NOT NULL AND stop_wait = 1'''

        self.setstoppedgame = '''UPDATE ninjabot_channels SET stop_wait = ?, game_mode = ?, game_time = ? WHERE channel_id = ?'''
        self.checkstop = '''SELECT stop_wait,game_mode FROM ninjabot_channels WHERE channel_id = ?'''

        self.checkresume = '''SELECT game_resume,game_nonstop FROM ninjabot_channels WHERE channel_id = ?'''
        self.setresume = '''UPDATE ninjabot_channels SET game_resume = 1 WHERE channel_id = ?'''
        self.cleargamedata = '''UPDATE ninjabot_channels SET stop_wait = 0, game_resume = 0, game_id = NULL, game_answer = NULL WHERE channel_id = ?'''
        
        self.gamestop = self.shortcommand + 'stop'
        
        self.haiku = self.longcommand + ' haiku'

        self.nonstop = self.longcommand + ' nonstop'

        self.timer = self.longcommand + ' timer'

        self.haikuswapsql = '''UPDATE ninjabot_channels SET haiku_status = ? WHERE channel_id = ?'''
        self.haikuchecksql = '''SELECT haiku_status FROM ninjabot_channels WHERE channel_id = ?'''

        self.timerswapsql = '''UPDATE ninjabot_channels SET game_timer = ? WHERE channel_id = ?'''
        self.timerchecksql = '''SELECT game_timer FROM ninjabot_channels WHERE channel_id = ?'''        

        self.ninjabotdicehelpinfo=nextcord.Embed(title="Ninjabot Dice", description="How to play NinjaBot Dice", color=nextcord.Color.green())
        self.ninjabotdicehelpinfo.add_field(name="`ninjabot dice 5d20`", value="Rolls dice with a size of your choosing.\r\nThis example would roll a d20 5 times.\r\nYou are limited to rolling 20 times at once, but the number of sides is not limited. Go crazy!\r\nTry `ninjabot dice 20d100` to see what I mean.", inline=False)   
        
        self.ninjabothelp = self.longcommand + ' help'

        self.ninjabothelpinfo=nextcord.Embed(title="Ninjabot Help", description="Use the following commands to see help information for each function.")
        self.ninjabothelpinfo.add_field(name="Games", value='!hangman\r\n!trivia\r\n!dice\r\n!kanji\r\n!kana\r\n!japanese\r\n!asl\r\n!french', inline=False)
        self.ninjabothelpinfo.add_field(name="Scheduling", value="Ninjabot scheduling feature. Enter 'ninjabot schedule' for more info.", inline=False)
        self.ninjabothelpinfo.add_field(name="Haiku", value="Enter 'ninjabot haiku' to Enable/Disable Ninjabot Haiku for the current channel'.", inline=False)
        self.ninjabothelpinfo.add_field(name="Support", value="Ninjabot support info. Enter 'ninjabot support'.", inline=False)
        self.ninjabothelpinfo.add_field(name="Simple Mode", value="This channel currently is NOT in simple mode. Type 'ninjabot simple' to switch.\r\nSimple mode is an easier way to play NinjaBot games. The only prefix needed is !", inline=False)
        self.ninjabothelpinfo.add_field(name="Change Prefix", value="Enter 'ninjabot prefix' followed by a new prefix. This is per channel.\r\nExample: 'ninjabot prefix ?'.", inline=False)

        self.ninjabothelpinfosimple=nextcord.Embed(title="Ninjabot Help", description="Use the following commands to get started.")
        self.ninjabothelpinfosimple.add_field(name="Games", value='!hangman\r\n!trivia\r\n!dice\r\n!kanji\r\n!kana\r\n!japanese\r\n!asl\r\n!french\r\n\r\nYou can respond to any game with !\r\nYou can stop any game with !stop', inline=False)
        self.ninjabothelpinfosimple.add_field(name="More Help", value='Type "ninjabot" followed by the game. Example: ninjabot hangman', inline=False)        
        self.ninjabothelpinfosimple.add_field(name="Scheduling", value="Ninjabot scheduling feature. Enter 'ninjabot schedule' for more info.", inline=False)
        self.ninjabothelpinfosimple.add_field(name="Haiku", value="Enter 'ninjabot haiku' to Enable/Disable Ninjabot Haiku for the current channel'.", inline=False)
        self.ninjabothelpinfosimple.add_field(name="Change Prefix", value="Enter 'ninjabot prefix' followed by a new prefix. This is per channel.\r\nExample: 'ninjabot prefix ?'.", inline=False)
        #self.ninjabothelpinfosimple.add_field(name="Support", value="Ninjabot support info. Enter 'ninjabot support'.", inline=False)
        #self.ninjabothelpinfosimple.add_field(name="Simple Mode", value="Simple mode is on by default. Games are started with the commands above and can be answered with just a !\r\nIf you want to switch out of this mode, type 'ninjabot simple'\r\nThe only added benefit of leaving this mode is running multiple NinjaBot games at once.", inline=False)

        self.ninjabottrivia = self.longcommand + ' trivia'
        self.ninjabottriviahelp = self.longcommand + ' trivia help'
        self.ninjabottriviastart = self.longcommand + ' trivia start'
        self.ninjabottriviastop = self.longcommand + ' trivia stop'
        self.ninjabottriviaanswer = self.longcommand + ' trivia answer'
        self.ninjabottriviascore = self.longcommand + ' trivia score'
        
        self.lt = self.shortcommand + 'trivia'
        self.lta = self.shortcommand + 'ta'
        self.lts = self.shortcommand + 'ts'
        self.ltscore = self.shortcommand + 'tscore'
        self.ltstop = self.shortcommand + 'tstop'

        self.tlist = [self.lt,self.lta,self.lts,self.ltscore,self.ltstop]
        
        self.refertohelp = 'I am sorry {0.author.name}, I do not recognize that command. Please refer to the help by entering "ninjabot" or "ninjabot help".'

        self.ninjabottriviahelpinfo=nextcord.Embed(title="Ninjabot Trivia", description="How to play NinjaBot Trivia. Commands are in bold.")
        self.ninjabottriviahelpinfo.add_field(name="!ts", value='Trivia start. Generates a new trivia question.', inline=False)
        self.ninjabottriviahelpinfo.add_field(name="!tstop", value='Trivia stop. Gives you the answer if trivia was started and ends the game.', inline=False)
        self.ninjabottriviahelpinfo.add_field(name="!ta", value="Trivia answer. This is for submitting your answer. Follow the command with what you think the answer is. For example, enter '!ta monty python' if you think the answer is 'monty python'.", inline=False)
        self.ninjabottriviahelpinfo.add_field(name="!tscore", value='Trivia score. This is for seeing your score. You recieve points for answering correctly within 30 seconds.', inline=False)
        
        self.ninjabottriviahelpinfosimple=nextcord.Embed(title="Ninjabot Trivia", description="More Information")
        self.ninjabottriviahelpinfosimple.add_field(name="Playing", value='Once you type "!trivia" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!music" if you think the answer is music.', inline=False)
        self.ninjabottriviahelpinfosimple.add_field(name="Scoring", value='Type "!tscore" to see your total score. You recieve points for answering correctly within 30 seconds.', inline=False)

        self.ninjabothangman = self.longcommand + ' hangman'
        self.ninjabothangmanstart = self.longcommand + ' hangman start'
        self.ninjabothangmanstop = self.longcommand + ' hangman stop'
        self.ninjabothangmananswer = self.longcommand + ' hangman answer'
        self.ninjabothangmanhelp = self.longcommand + ' hangman help'
        self.ninjabothangmanscore = self.longcommand + ' hangman score'
        
        self.lh = self.shortcommand + 'hangman'
        self.lha = self.shortcommand + 'ha'
        self.lhs = self.shortcommand + 'hs'
        self.lhscore = self.shortcommand + 'hscore'

        self.hlist = [self.lh,self.lha,self.lhs,self.lhscore]
        
        self.ninjabothangmanhelpinfo=nextcord.Embed(title="Ninjabot Hangman", description="How to play NinjaBot Hangman. Commands are in bold.")
        self.ninjabothangmanhelpinfo.add_field(name="!hs", value='Hangman start. Generates a new word and game.', inline=False)
        self.ninjabothangmanhelpinfo.add_field(name="!ha", value="Hangman answer. This is for submitting your answer. Follow the command with a letter that might be in the word. For example, enter '!ha z' if you think the word contains 'z'.", inline=False)
        self.ninjabothangmanhelpinfo.add_field(name="!hscore", value="Hangman score. This is for seeing your score. You recieve points for answering correctly in winning games.", inline=False)
        self.ninjabothangmanhelpinfo.add_field(name="!hstop", value='Hangman stop. Gives you the answer if hangman was started and ends the game.', inline=False)

        self.ninjabothangmanhelpinfosimple=nextcord.Embed(title="Ninjabot Hangman", description="More Information")
        self.ninjabothangmanhelpinfosimple.add_field(name="Playing", value='Once you type "!hangman" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!a" if you think the answer contains the letter a. You may also attempt to guess whole words.', inline=False)
        self.ninjabothangmanhelpinfosimple.add_field(name="Scoring", value="Type '!hscore' to see your score. You recieve points for answering correctly in winning games.", inline=False)

        self.hangman0 = 'data/images/hangninja0.png'
        self.hangman1 = 'data/images/hangninja1.png'
        self.hangman2 = 'data/images/hangninja2.png'
        self.hangman3 = 'data/images/hangninja3.png'
        self.hangman4 = 'data/images/hangninja4.png'
        self.hangman5 = 'data/images/hangninja5.png'
        self.hangman6 = 'data/images/hangninja6.png'

        self.hangmen = []
        self.hangmen.append(self.hangman0)
        self.hangmen.append(self.hangman1)
        self.hangmen.append(self.hangman2)
        self.hangmen.append(self.hangman3)
        self.hangmen.append(self.hangman4)
        self.hangmen.append(self.hangman5)
        self.hangmen.append(self.hangman6)

        self.channelinfo = self.longcommand + ' channel info'
        self.channelinforesponse = 'Your name is {0.author} with ID {0.author.id}\r\nThis channel is {0.channel} with ID {0.channel.id}\r\nThis server is {0.guild} with ID {0.guild.id}\r\nThe server owner is {0.guild.owner}\r\nThe server channels are {0.guild.channels[1]}'

        self.ninjabotsupport = self.longcommand + ' support'
        self.supportinfo=nextcord.Embed(title="NinjaBot Support Information", description="Use the following information if you need support.")
        self.supportinfo.add_field(name="Support Server", value='Use the following Discord server to get support for NinjaBot or simply to get in touch with the developer.\r\nhttps://discord.gg/gv8anXX', inline=False)
        self.supportinfo.add_field(name="Invite NinjaBot", value='Use the following link to invite NinjaBot to your own server.\r\nhttps://discord.com/oauth2/authorize?client_id=755504243322126426&scope=bot&permissions=0', inline=False)
        self.supportinfo.add_field(name="Donate", value='NinjaBot accepts Stellar Lumens!\r\n`GDGYKCXRJO67IBS3ZW2JMENIZBVXJ7XUZ56JJLGGMVKFO3YGQVWAK67T`', inline=False)

        self.ninjabotschedule = self.longcommand + ' schedule'
        self.ninjabotscheduleadd = self.longcommand + ' schedule add'
        self.ninjabotschedulestatus = self.longcommand + ' schedule status'
        self.ninjabotscheduleremove = self.longcommand + ' schedule remove'
        self.ninjabotscheduleunlock = self.longcommand + ' schedule unlock confirm'
        self.ninjabotschedulesecurity = self.longcommand + ' schedule security'
        self.ninjabotschedulereset = self.longcommand + ' schedule reset confirm'
        self.ninjabotschedulehelp = self.longcommand + ' schedule help'
        
        self.wrongmin = 'I am sorry {0.author.name} but that minute is invalid!'
        self.wronghour = 'I am sorry {0.author.name} but that hour is invalid!'
        self.wrongtime = 'I am sorry {0.author.name} but that time is invalid!'
        self.wrongmon = 'I am sorry {0.author.name} but that month is invalid!'
        self.wrongyear = 'I am sorry {0.author.name} but that year is invalid!'
        self.wrongday = 'I am sorry {0.author.name} but that day is invalid!'
        self.wrongdate = 'I am sorry {0.author.name} but that date is invalid!'
        self.wrongtz = 'I am sorry {0.author.name} but that timezone is invalid!'


        self.nosched = 'I am sorry {0.author.name} but there currently is nothing scheduled!'
        self.wrongchannel = 'I am sorry {0.author.name} but that channel is invalid!'
        self.wrongevent = 'I am sorry {0.author.name} but that event is invalid!'
        self.extravalue = 'I am sorry {0.author.name} but you seem to have submitted something extra!'
        self.noeventdata = 'Warning! An event was scheduled to go off but there was not any data!'
        self.wrongcolor = 'I am sorry {0.author.name} but that color is invalid!'
        self.nodata = 'I am sorry {0.author.name} but you submitted no data!'
        
        self.securityfailure = 'I am sorry {0.author.name} but you are currently not authorized to perform this action!'
        self.verywrong = 'I am sorry {0.author.name} but something went horribly wrong. You should report this to the developer if you have no idea what you did wrong.'


        self.daylist = 'monday','tuesday','wednesday','thursday','friday','saturday','sunday'
        self.monthlist = 'january','february','march','april','may','june','july','august','september','october','november','december'
        tempnumericmonthlist = range(1,13)
        self.numericmonthlist = []
        for num in tempnumericmonthlist:
            self.numericmonthlist.append(str(num).zfill(2))
        self.datelist = range(1,32)
        self.yearlist = range(2020,2200)
        self.eventlist = 'once','weekly','monthly','yearly','dayofmonth'

        self.timelist = []
        for hour in range(00,24):
            for minute in range(00,60):
                self.timelist.append(str(hour).zfill(2) + ':' + str(minute).zfill(2))

        self.hexlist = []

        for hexnum in range(0,256):
            self.hexlist.append(str(hex(hexnum))[2:].zfill(2))


        self.ninjabotschedulehelpinfo=nextcord.Embed(title="Ninjabot Schedule", description='Initially only the server owner can make or edit its events. Security settings coming soon.')
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule create once channel', value='Adds a one-time event to your schedule.\r\nFor example, enter "ninjabot schedule create once general" to create an event that will go off in the #general channel. Proceed to use the "modify" command show below.', inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule create weekly channel', value='Adds a weekly event to your schedule.\r\nFor example, enter "ninjabot schedule create weekly general" to create an event that will go off in the #general channel. Proceed to use the "modify" command show below.', inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule create monthly channel', value='Adds a monthly event to your schedule.\r\nFor example, enter "ninjabot schedule create monthly general" to create an event that will go off in the #general channel. Proceed to use the "modify" command show below.', inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule create yearly channel', value='Adds a yearly event to your schedule.\r\nFor example, enter "ninjabot schedule create yearly general" to create an event that will go off in the #general channel. Proceed to use the "modify" command show below.', inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule create dayofmonth channel', value='Adds a dayofmonth event to your schedule.\r\nFor example, enter "ninjabot schedule create dayofmonth general" to create an event that will go off in the #general channel. Proceed to use the "modify" command show below.', inline=False)        
        self.ninjabotschedulehelpinfo.add_field(name="ninjabot schedule list", value='Shows you all the events on your servers schedule.', inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # title', value="Use this to add or modify the title.\r\nFor example, enter 'ninjabot schedule modify 5 title Today is a good day!' to make your title 'Today is a good day!'", inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # description', value="Use this to add or modify the description.\r\nFor example, enter 'ninjabot schedule modify 5 description Today is a good day!' to make your description 'Today is a good day!'.", inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # date', value="Use this to add or modify the date of the first announcement in the series.\r\nFor example, enter 'ninjabot schedule modify 5 date 2020-09-29 23:32' to make the first event start at 11:32PM on September the 29th.\r\nNinjaBot will know how to handle the rest of the events based on this date and the event type.", inline=False)        
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # color', value="Use this to add or modify the color.\r\nUse the following website to get your 6 character hex color code:\r\nhttps://htmlcolorcodes.com/\r\nFor example, enter 'ninjabot schedule modify 5 color D5F2F1' to make your color a light blue.", inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # image', value="Use this to add or modify the image.\r\nUse a direct URL for the image just like you would post in discord.\r\nFor example, enter 'ninjabot schedule modify 5 image https://media3.giphy.com/media/H4DjXQXamtTiIuCcRU/giphy.gif' to add a cute cat gif to your event.'", inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # timezone', value="Use this to add or modify the timezone.\r\nFor timezone labels, look here:\r\nhttps://en.wikipedia.org/wiki/List_of_tz_database_time_zones\r\nBy default, NinjaBot uses America/Los_Angeles, so change this if you live elsewhere.\r\nFor example, enter 'ninjabot schedule modify 5 timezone America/Chicago' if you are on Central Time.'", inline=False)
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule modify # mention', value="Use this to add or modify who is mentioned for the event.\r\nFor example, enter 'ninjabot schedule modify 5 mention everyone' if you want to mention @everyone.'", inline=False)        
        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule preview #', value="Use this to preview your announcement in the current channel.\r\nFor example, enter 'ninjabot schedule preview 31' if you want to preview event ID 31.'", inline=False)


        self.ninjabotschedulehelpinfo.add_field(name='ninjabot schedule remove', value="Removes an event on your schedule.\r\nFor example, enter 'ninjabot schedule remove 5' to remove that event in your schedule.", inline=False)


        self.hangmanstartsql = '''UPDATE ninjabot_channels SET hangman_word = ?, hangman_letters = ?, hangman_badletters = "NONE", hangman_status = 0, hangman_contributors = "NONE", game_mode = "hangman" WHERE channel_id = ?'''
        self.hangmannullsql = '''UPDATE ninjabot_channels SET hangman_word = NULL, hangman_letters = NULL, hangman_badletters = NULL, hangman_status = 0, hangman_contributors = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.updatehangmanscore = '''UPDATE ninjabot_users SET hangman_score = ? WHERE user_id = ?'''
        self.hangmandatasql = '''SELECT hangman_word,hangman_letters,hangman_badletters,hangman_status,hangman_contributors FROM ninjabot_channels WHERE channel_id = ?'''
        self.gethangmanscore = '''SELECT hangman_score FROM ninjabot_users WHERE user_id = ?'''
        self.updatehangmanbadword = '''UPDATE ninjabot_channels SET hangman_status = ? WHERE channel_id = ?'''
        self.updatehangmangoodletter = '''UPDATE ninjabot_channels SET hangman_letters = ?, hangman_contributors = ? WHERE channel_id = ?'''
        self.updatehangmanbadletter = '''UPDATE ninjabot_channels SET hangman_badletters = ?, hangman_status = ? WHERE channel_id = ?'''

        self.checkusersql = '''SELECT EXISTS (SELECT user_id FROM ninjabot_users WHERE user_id = ?)'''
        self.insertusersql = '''INSERT INTO ninjabot_users(user_id,date_added,hangman_score,trivia_score) VALUES(?,?,?,?)'''
        self.checkchannelsql = '''SELECT EXISTS (SELECT channel_id FROM ninjabot_channels WHERE channel_id = ?)'''
        self.insertchannelsql = '''INSERT INTO ninjabot_channels(channel_id,date_added) VALUES(?,?)'''

        self.gettriviascore = '''SELECT trivia_score FROM ninjabot_users WHERE user_id = ?'''
        self.trivianullsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.triviastartsql = '''UPDATE ninjabot_channels SET game_answer = ?, game_mode = "trivia", game_time = ?, game_id = ?, game_resume = 0 WHERE channel_id = ?'''
        self.triviaanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.triviadatasql = '''SELECT game_answer,game_time,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.updatetriviascore = '''UPDATE ninjabot_users SET trivia_score = ? WHERE user_id = ?'''
        self.newtriviaquestion = '''SELECT category,value,question,answer,round,question_id FROM trivia_questions WHERE question_id = ?'''

        self.geteventsql = '''SELECT channel_id,event_type,event_date,event_title,event_description,event_image,event_color,event_tz,guild_id,event_mention FROM schedule WHERE event_id = ?'''
        self.getalleventssql = '''SELECT channel_id,event_type,event_date,event_title,event_description,event_image,event_color,event_tz,event_mention,event_id FROM schedule'''
        self.insertschedulesql = '''INSERT INTO schedule(guild_id,channel_id,user_id,event_creation,event_type) VALUES(?,?,?,?,?) ;'''
        self.checkeventsql = '''SELECT event_id FROM schedule WHERE event_id = ?'''
        self.checkeventownersql = '''SELECT guild_id FROM schedule WHERE event_id = ?'''
        self.modifyschedulesql = '''INSERT INTO schedule(channel_id,event_type,event_date,event_title,event_description,event_image,event_color) VALUES(?,?,?,?,?,?,?) ;'''
        self.listeventssql = '''SELECT event_id,channel_id,event_type,event_date,event_title,event_tz FROM schedule WHERE guild_id = ?'''
        self.getremoval = '''SELECT guild_id FROM schedule WHERE event_id = ?'''
        self.eventremoval = '''DELETE FROM schedule WHERE event_id = ?;'''

        self.modifychannel = '''UPDATE schedule SET channel_id = ? WHERE event_id = ?'''
        self.modifytype = '''UPDATE schedule SET event_type = ? WHERE event_id = ?'''
        self.modifydate = '''UPDATE schedule SET event_date = ? WHERE event_id = ?'''
        self.modifytitle = '''UPDATE schedule SET event_title = ? WHERE event_id = ?'''
        self.modifydescription = '''UPDATE schedule SET event_description = ? WHERE event_id = ?'''
        self.modifyimage = '''UPDATE schedule SET event_image = ? WHERE event_id = ?'''
        self.modifycolor = '''UPDATE schedule SET event_color = ? WHERE event_id = ?'''
        self.modifytz = '''UPDATE schedule SET event_tz = ? WHERE event_id = ?'''
        self.modifymention = '''UPDATE schedule SET event_mention = ? WHERE event_id = ?'''
        
        self.kanji = self.longcommand + ' kanji'
        self.kanjistart = self.longcommand + ' kanji start'
        self.kanjistop = self.longcommand + ' kanji stop'
        self.kanjianswer = self.longcommand + ' kanji answer'
        self.kanjilevel = self.longcommand + ' kanji level'
        self.kanjiscore = self.longcommand + ' kanji score'
        self.kanjihelp = self.longcommand + ' kanji help'

        self.lk = self.shortcommand + 'kanji'
        self.lks = self.shortcommand + 'ks'
        self.lka = self.shortcommand + 'ka'
        self.lkstop = self.shortcommand + 'kstop'
        self.lkscore = self.shortcommand + 'kscore'

        self.klist = [self.lk,self.lks,self.lka,self.lkstop,self.lkscore]

        self.kanjiallsql = '''SELECT meaning,id,literal FROM kanji WHERE id = ?'''
        self.kanjilevelsql = '''SELECT meaning,id,literal FROM kanji WHERE grade = ?'''
        self.kanjiwrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "kanji", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.kanjistopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.kanjianswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.kanjigetscore = '''SELECT kanji_score FROM ninjabot_users WHERE user_id = ?'''
        self.kanjisetscore = '''UPDATE ninjabot_users SET kanji_score = kanji_score + 1 WHERE user_id = ?'''       
        self.kanjisetlevel = '''UPDATE ninjabot_channels SET kanji_level = ? WHERE channel_id = ?'''
        self.kanjinulllevel = '''UPDATE ninjabot_channels SET kanji_level = NULL WHERE channel_id = ?'''
        self.kanjigetlevel = '''SELECT kanji_level FROM ninjabot_channels WHERE channel_id = ?'''
        self.kanjirandom = '''SELECT meaning,id,literal FROM kanji WHERE grade = ? ORDER BY RANDOM() LIMIT 1'''
        self.kanjireveal = '''SELECT on_reading,kun_reading,romaji,literal FROM kanji WHERE id = ?'''

        self.kanjiinfo=nextcord.Embed(title="NinjaBot Kanji", description="How to play NinjaBot Kanji. Commands are in bold.")
        self.kanjiinfo.add_field(name="!ks", value='Kanji start. Randomly selects a kanji and starts the game.', inline=False)
        self.kanjiinfo.add_field(name="!kstop", value='Kanji stop. Stops NinjaBot Kanji and shows you the answer.', inline=False)
        self.kanjiinfo.add_field(name="!ka", value='Kanji answer. Input your answer after the command.\r\nExample: "!ka grass" if you think the answer is "grass".', inline=False)
        self.kanjiinfo.add_field(name="!kscore", value='Kanji score. Shows your NinjaBot Kanji score.', inline=False)
        self.kanjiinfo.add_field(name="ninjabot kanji level", value='Changes the difficulty of the game.\r\nExample: "ninjabot kanji level 1"\r\nBy default, you will be set to the "1" option.\r\nLevels range from 1 to 9.\r\nIf you have never learned Kanji before, I recommend leaving at level 1', inline=False)

        self.kanjiinfosimple=nextcord.Embed(title="NinjaBot Kanji", description="More Information")
        self.kanjiinfosimple.add_field(name="Playing", value='Once you type "!kanji" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!red" if you think the answer is red.', inline=False)
        self.kanjiinfosimple.add_field(name="Scoring", value='Type "!kscore" to see your total score. You recieve one point per successful game.', inline=False)
        self.kanjiinfosimple.add_field(name="Difficulty Levels", value='You can change the difficulty level. The following changes you to level 1.\r\nExample: "ninjabot kanji level 1"\r\nBy default, you will be set to the "1" option.\r\nLevels range from 1 to 9.\r\nIf you have never learned Kanji before, I recommend leaving it at level 1', inline=False)

        self.asl = self.longcommand + ' asl'
        self.aslstart = self.longcommand + ' asl start'
        self.aslstop = self.longcommand + ' asl stop'
        self.aslanswer = self.longcommand + ' asl answer'
        self.aslscore = self.longcommand + ' asl score'
        self.aslhelp = self.longcommand + ' asl help'

        self.lasl = self.shortcommand + 'asl'
        self.lasls = self.shortcommand + 'asls'
        self.lasla = self.shortcommand + 'asla'
        self.laslstop = self.shortcommand + 'aslstop'
        self.laslscore = self.shortcommand + 'aslscore'

        self.asllist = [self.lasl,self.lasls,self.lasla,self.laslstop,self.laslscore]

        self.aslrandom = '''SELECT Meaning,Base,Link FROM asl ORDER BY RANDOM() LIMIT ?'''
        self.aslwrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "asl", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.aslanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.aslstopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_id = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.aslreveal = '''SELECT Meaning,Base,Link FROM asl WHERE Base = ?'''
        self.aslsetscore = '''UPDATE ninjabot_users SET asl_score = asl_score + 1 WHERE user_id = ?'''
        self.aslgetscore = '''SELECT asl_score FROM ninjabot_users WHERE user_id = ?'''

        self.aslinfo=nextcord.Embed(title="NinjaBot ASL", description="How to play NinjaBot ASL. Commands are in bold.")
        self.aslinfo.add_field(name="!asls", value='ASL start. Randomly selects an ASL word and starts the game.', inline=False)
        self.aslinfo.add_field(name="!aslstop", value='ASL stop. Stops NinjaBot ASL and shows you the answer.', inline=False)
        self.aslinfo.add_field(name="!asla", value='ASL answer. Input your answer after the command.\r\nExample: "!asla tea" if you think the answer is "tea".', inline=False)
        self.aslinfo.add_field(name="!aslscore", value='ASL score. Shows your NinjaBot ASL score.', inline=False)

        self.aslinfosimple=nextcord.Embed(title="NinjaBot ASL", description="More Information")
        self.aslinfosimple.add_field(name="Playing", value='Once you type "!asl" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!walking" if you think the answer is walking.')
        self.aslinfosimple.add_field(name="Scoring", value='Type "!aslscore" to see your score. You recieve one point per successful game.', inline=False)

        self.kana = self.longcommand + ' katakana'
        self.kanastart = self.longcommand + ' kana start'
        self.kanastop = self.longcommand + ' kana stop'
        self.kanaanswer = self.longcommand + ' kana answer'
        self.kanalevel = self.longcommand + ' kana level'
        self.kanascore = self.longcommand + ' kana score'
        self.kanahelp = self.longcommand + ' kana help'

        self.lkn = self.shortcommand + 'kana'
        self.lkns = self.shortcommand + 'kns'
        self.lkna = self.shortcommand + 'kna'
        self.lknstop = self.shortcommand + 'knstop'
        self.lknscore = self.shortcommand + 'knscore'

        self.knlist = [self.lkn,self.lkns,self.lkna,self.lknstop,self.lknscore]

        self.kanaallsql = '''SELECT romaji,id,kana FROM kana WHERE id = ?'''
        self.kanawrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "kana", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.kanastopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.kanaanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.kanagetscore = '''SELECT kana_score FROM ninjabot_users WHERE user_id = ?'''
        self.kanasetscore = '''UPDATE ninjabot_users SET kana_score = kana_score + 1 WHERE user_id = ?'''       
        self.kanareveal = '''SELECT type,kana FROM kana WHERE id = ?'''

        self.kanainfo=nextcord.Embed(title='NinjaBot Katakana', description="How to play NinjaBot Katakana. Commands are in bold.")
        self.kanainfo.add_field(name="!kns", value='Katakana start. Randomly selects a Katakana and starts the game.', inline=False)
        self.kanainfo.add_field(name="!knstop", value='Katakana stop. Stops NinjaBot Katakana and shows you the answer.', inline=False)
        self.kanainfo.add_field(name="!kna", value='Katakana answer. Input your answer after the command.\r\nExample: "!kna ka" if you think the answer is "ka".', inline=False)
        self.kanainfo.add_field(name="!knscore", value='Katakana score. Shows your NinjaBot Katakana score.', inline=False)

        self.kanainfosimple=nextcord.Embed(title='NinjaBot Katakana', description="More Information")
        self.kanainfosimple.add_field(name="Playing", value='Once you type "!kana" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!ka" if you think the answer is ka.', inline=False)
        self.kanainfosimple.add_field(name="Scoring", value='Type "!knscore" to see your score. You recieve one point per successful game.', inline=False)

        self.gana = self.longcommand + ' hiragana'
        self.ganastart = self.longcommand + ' gana start'
        self.ganastop = self.longcommand + ' gana stop'
        self.ganaanswer = self.longcommand + ' gana answer'
        self.ganalevel = self.longcommand + ' gana level'
        self.ganascore = self.longcommand + ' gana score'
        self.ganahelp = self.longcommand + ' gana help'

        self.lgn = self.shortcommand + 'gana'
        self.lgns = self.shortcommand + 'gns'
        self.lgna = self.shortcommand + 'gna'
        self.lgnstop = self.shortcommand + 'gnstop'
        self.lgnscore = self.shortcommand + 'gnscore'

        self.gnlist = [self.lgn,self.lgns,self.lgna,self.lgnstop,self.lgnscore]

        self.ganaallsql = '''SELECT romaji,id,kana FROM kana WHERE id = ?'''
        self.ganawrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "gana", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.ganastopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.ganaanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.ganagetscore = '''SELECT gana_score FROM ninjabot_users WHERE user_id = ?'''
        self.ganasetscore = '''UPDATE ninjabot_users SET gana_score = gana_score + 1 WHERE user_id = ?'''       
        self.ganareveal = '''SELECT type,kana FROM kana WHERE id = ?'''

        self.ganainfo=nextcord.Embed(title='NinjaBot Hiragana', description="How to play NinjaBot Hiragana. Commands are in bold.")
        self.ganainfo.add_field(name="!gns", value='Hiragana start. Randomly selects a Hiragana and starts the game.', inline=False)
        self.ganainfo.add_field(name="!gnstop", value='Hiragana stop. Stops NinjaBot Hiragana and shows you the answer.', inline=False)
        self.ganainfo.add_field(name="!gna", value='Hiragana answer. Input your answer after the command.\r\nExample: "!gna ga" if you think the answer is "ga".', inline=False)
        self.ganainfo.add_field(name="!gnscore", value='Hiragana score. Shows your NinjaBot Hiragana score.', inline=False)

        self.ganainfosimple=nextcord.Embed(title='NinjaBot Hiragana', description="More Information")
        self.ganainfosimple.add_field(name="Playing", value='Once you type "!gana" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!ga" if you think the answer is ga.', inline=False)
        self.ganainfosimple.add_field(name="Scoring", value='Type "!gnscore" to see your score. You recieve one point per successful game.', inline=False)

        self.japanese = self.longcommand + ' japanese'
        self.japanesestart = self.longcommand + ' japanese start'
        self.japanesestop = self.longcommand + ' japanese stop'
        self.japaneseanswer = self.longcommand + ' japanese answer'
        self.japaneselevel = self.longcommand + ' japanese level'
        self.japanesescore = self.longcommand + ' japanese score'
        self.japanesehelp = self.longcommand + ' japanese help'

        self.lj = self.shortcommand + 'japanese'
        self.ljs = self.shortcommand + 'js'
        self.lja = self.shortcommand + 'ja'
        self.ljstop = self.shortcommand + 'jstop'
        self.ljscore = self.shortcommand + 'jscore'

        self.jlist = [self.lj,self.ljs,self.lja,self.ljstop,self.ljscore]

        self.japaneseallsql = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-answers","Vocab-pos","Sentence-expression","Sentence-kana","Sentence-romaji","Vocab-expression" FROM kore WHERE "Core-index" = ?'''
        self.japanesewrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "japanese", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.japanesestopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.japaneseanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.japanesegetscore = '''SELECT japanese_score FROM ninjabot_users WHERE user_id = ?'''
        self.japanesesetscore = '''UPDATE ninjabot_users SET japanese_score = japanese_score + 1 WHERE user_id = ?'''       
        self.japanesereveal = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-meaning","Vocab-pos","Sentence-expression","Sentence-kana","Sentence-romaji","Sentence-meaning","Vocab-expression" FROM kore WHERE "Core-index" = ?'''
        self.japanesegetlevel = '''SELECT japanese_level FROM ninjabot_channels WHERE channel_id = ?'''
        self.japanesesetlevel = '''UPDATE ninjabot_channels SET japanese_level = ? WHERE channel_id = ?'''
        self.japaneserandom = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-answers","Vocab-pos","Sentence-expression","Sentence-kana","Sentence-romaji","Vocab-expression" FROM kore WHERE jlpt = ? ORDER BY RANDOM() LIMIT 1'''
        self.japanesenulllevel = '''UPDATE ninjabot_channels SET japanese_level = NULL WHERE channel_id = ?'''

        self.japaneseinfo=nextcord.Embed(title="NinjaBot japanese", description="How to play NinjaBot Japanese. Commands are in bold.")
        self.japaneseinfo.add_field(name="!js", value='Japanese start. Randomly selects a Japanese word and starts the game.', inline=False)
        self.japaneseinfo.add_field(name="!jstop", value='Japanese stop. Stops NinjaBot Japanese and shows you the answer.', inline=False)
        self.japaneseinfo.add_field(name="!ja", value='Japanese answer. Input your answer after the command.\r\nExample: "!ja music" if you think the answer is "music".', inline=False)
        self.japaneseinfo.add_field(name="!jscore", value='Japanese score. Shows your NinjaBot Japanese score.', inline=False)
        self.japaneseinfo.add_field(name="ninjabot japanese level", value='Set the JLPT level of the vocabulary. Default is 5.\r\nExample: ninjabot japanese level 4', inline=False)

        self.japaneseinfosimple=nextcord.Embed(title="NinjaBot japanese", description="More Information")
        self.japaneseinfosimple.add_field(name="Playing", value='Once you type "!japanese" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!walk" if you think the answer is walk.', inline=False)
        self.japaneseinfosimple.add_field(name="Scoring", value='Type "!jscore" to see your score. You recieve one point per successful game.', inline=False)
        self.japaneseinfosimple.add_field(name="Difficulty Levels", value='You can set the JLPT level of the vocabulary. The default is 5, which is the lowest.\r\nExample: ninjabot japanese level 4', inline=False)

        self.nihongo = self.longcommand + ' nihongo'
        self.nihongostart = self.longcommand + ' nihongo start'
        self.nihongostop = self.longcommand + ' nihongo stop'
        self.nihongoanswer = self.longcommand + ' nihongo answer'
        self.nihongolevel = self.longcommand + ' nihongo level'
        self.nihongoscore = self.longcommand + ' nihongo score'
        self.nihongohelp = self.longcommand + ' nihongo help'

        self.nihongoallsql = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-expression" FROM kore WHERE "Core-index" = ?'''
        self.nihongowrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "nihongo", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.nihongostopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.nihongoanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.nihongogetscore = '''SELECT nihongo_score FROM ninjabot_users WHERE user_id = ?'''
        self.nihongosetscore = '''UPDATE ninjabot_users SET nihongo_score = nihongo_score + 1 WHERE user_id = ?'''       
        self.nihongoreveal = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-meaning","Vocab-expression" FROM kore WHERE "Core-index" = ?'''
        self.nihongogetlevel = '''SELECT japanese_level FROM ninjabot_channels WHERE channel_id = ?'''
        self.nihongosetlevel = '''UPDATE ninjabot_channels SET japanese_level = ? WHERE channel_id = ?'''
        self.nihongorandom = '''SELECT "Core-index","Vocab-kana","Vocab-romaji","Vocab-expression" FROM kore WHERE jlpt = ? ORDER BY RANDOM() LIMIT 1'''

        self.french = self.longcommand + ' french'
        self.frenchstart = self.longcommand + ' french start'
        self.frenchstop = self.longcommand + ' french stop'
        self.frenchanswer = self.longcommand + ' french answer'
        self.frenchlevel = self.longcommand + ' french level'
        self.frenchscore = self.longcommand + ' french score'
        self.frenchhelp = self.longcommand + ' french help'

        self.lf = self.shortcommand + 'french'
        self.lfs = self.shortcommand + 'fs'
        self.lfa = self.shortcommand + 'fa'
        self.lfstop = self.shortcommand + 'fstop'
        self.lfscore = self.shortcommand + 'fscore'

        self.flist = [self.lf,self.lfs,self.lfa,self.lfstop,self.lfscore]

        self.frenchallsql = '''SELECT "rank","word_fr","tag","phrase_fr","answers" FROM french WHERE "rank" = ?'''
        self.frenchwrite = '''UPDATE ninjabot_channels SET game_answer = ?, game_id = ?, game_mode = "french", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.frenchstopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.frenchanswersql = '''SELECT game_answer,game_id FROM ninjabot_channels WHERE channel_id = ?'''
        self.frenchgetscore = '''SELECT french_score FROM ninjabot_users WHERE user_id = ?'''
        self.frenchsetscore = '''UPDATE ninjabot_users SET french_score = french_score + 1 WHERE user_id = ?'''       
        self.frenchreveal = '''SELECT "rank","word_fr","tag","phrase_fr","word_en","phrase_en" FROM french WHERE "rank" = ?'''
        self.frenchrandom = '''SELECT "rank","word_fr","tag","phrase_fr","answers" FROM french WHERE ORDER BY RANDOM() LIMIT 1'''

        self.frenchinfo=nextcord.Embed(title="NinjaBot French", description="How to play NinjaBot French. Commands are in bold.")
        self.frenchinfo.add_field(name="!fs", value='French start. Randomly selects a french word and starts the game.', inline=False)
        self.frenchinfo.add_field(name="!fstop", value='French stop. Stops NinjaBot French and shows you the answer.', inline=False)
        self.frenchinfo.add_field(name="!fa", value='French answer. Input your answer after the command.\r\nExample: "!fa music" if you think the answer is "music".', inline=False)
        self.frenchinfo.add_field(name="!fscore", value='French score. Shows your NinjaBot French score.', inline=False)

        self.frenchinfosimple=nextcord.Embed(title="NinjaBot French", description="More Information")
        self.frenchinfosimple.add_field(name="Playing", value='Once you type "!french" the game will begin. Answer by using an exclamation mark followed by your answer. Example: "!walk" if you think the answer is walk.', inline=False)
        self.frenchinfosimple.add_field(name="Scoring", value='Type "!fscore" to see your score. You recieve one point per successful game.', inline=False)

        self.minesweeper = self.longcommand + ' minesweeper'

        self.minewritesql = '''UPDATE ninjabot_channels SET minesweeper_game = ?, game_mode = "minesweeper" WHERE channel_id = ?'''
        self.minestopsql = '''UPDATE ninjabot_channels SET minesweeper_game = NULL, game_mode = NULL, minesweeper_contributors = NULL WHERE channel_id = ?'''
        self.minegetsql = '''SELECT minesweeper_game FROM ninjabot_channels WHERE channel_id = ?'''
        self.minegetcontsql = '''SELECT minesweeper_contributors FROM ninjabot_channels WHERE channel_id = ?'''
        self.minesetcontsql = '''UPDATE ninjabot_channels SET minesweeper_contributors = ? WHERE channel_id = ?'''


        self.minegetscore = '''SELECT mine_score FROM ninjabot_users WHERE user_id = ?'''
        self.minesetscore = '''UPDATE ninjabot_users SET mine_score = mine_score + 1 WHERE user_id = ?'''   

        self.dictget = '''SELECT word,wordtype,definition FROM entries WHERE word = ?'''

        self.riddle = self.longcommand + ' riddle'

        self.riddlewrite = '''UPDATE ninjabot_channels SET game_id = ?, game_answer = ?, game_mode = "riddle", game_time = ?, game_resume = 0 WHERE channel_id = ?'''
        self.riddlestopsql = '''UPDATE ninjabot_channels SET game_answer = NULL, game_mode = NULL WHERE channel_id = ?'''
        self.riddleanswersql = '''SELECT game_id,game_answer FROM ninjabot_channels WHERE channel_id = ?'''
        self.riddlegetscore = '''SELECT riddle_score FROM ninjabot_users WHERE user_id = ?'''
        self.riddlesetscore = '''UPDATE ninjabot_users SET riddle_score = riddle_score + 1 WHERE user_id = ?'''       
        self.riddlereveal = '''SELECT "game_id","game_answer" FROM ninjabot_channels WHERE "channel" = ?'''
        self.riddlerandom = '''SELECT DISTINCT "question","answer" FROM riddles ORDER BY RANDOM() LIMIT 1'''