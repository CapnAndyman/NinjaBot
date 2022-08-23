import nextcord
import datetime
import time
import asyncio
from os import walk
from pytz import timezone
import calendar
import sys

class Ninjabotannounce:
    
    async def ninjabotannounce(self,ninjabot,thisisatest):
        #Import Settings
        self.settings = ninjabot.settings
        #Week ranges
        firstweek = range(1,8)
        secondweek = range(8,15)
        thirdweek = range(15,22)
        fourthweek = range(22,29)
        fifthweek = range(29,32)
        
        #DB time format
        timeformat = '%Y-%m-%d %H:%M:%S'
        #Start main while loop
        #Get current seconds in the current minute
        interval = datetime.datetime.now().strftime('%S')
        minute = datetime.datetime.now().strftime('%M')
        #Check if seconds are within the first half of the minute
        if int(interval) in range(0,5) and ninjabot.schedcheck == 0:

            #Notify on guilds
            
            
            try:
                if (int(minute) == 45 or int(minute) == 15) and thisisatest == 0:
                    newguilds = ninjabot.guilds
                    if len(ninjabot.currentguilds) > len(newguilds):
                        
                        for oneserver in ninjabot.currentguilds:
                            if oneserver not in newguilds:
                                await ninjabot.startupchannel.send(oneserver.name + ' kicked NinjaBot @here')
                                ninjabot.currentguilds = newguilds
                        await ninjabot.theposter.post()
                    
                    elif len(ninjabot.currentguilds) < len(newguilds):
                        
                        for oneserver in newguilds:
                            if oneserver not in ninjabot.currentguilds:
                                await ninjabot.startupchannel.send(oneserver.name + ' added NinjaBot @here')
                                ninjabot.currentguilds = newguilds
                        await ninjabot.theposter.post()

            except:
                await ninjabot.startupchannel.send("Can't update servers @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))

            #Notify channel change

            if ninjabot.statusid == 1:

                try:
                    #Update Status
                    await ninjabot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{len(ninjabot.currentguilds)} servers!"))
                except:
                    await ninjabot.startupchannel.send("Can't update status (servers) @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))

            else:
                
                try:
                    #Update Status
                    await ninjabot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="ninjabot help"))        
                except:
                    await ninjabot.startupchannel.send("Can't update status (help) @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))    

            ninjabot.statusid = ninjabot.statusid * -1

            #Pull all events from db
            schedule = list(ninjabot.ninjabotsql.sql_novalues(self.settings.getalleventssql))

            for singleevent in schedule:

                event = list(singleevent)

                if event[2]:

                    try:
                        if not event[7]:
                            event[7] = 'America/Los_Angeles'

                        now_time = datetime.datetime.now(timezone(event[7]))
                        date_time = datetime.datetime.strptime(event[2], timeformat)

                        now_time = now_time.replace(tzinfo=None)

                        if not event[3]:
                            event[3] = 'NONE'
                        if not event[4]:
                            event[4] = 'NONE'
                    
                        if event[1] == 'once':
                            if now_time.strftime('%Y-%m-%d %H:%M') == event[2][:-3]:

                                channel = ninjabot.get_channel(int(event[0]))
                                
                                eventmessage=nextcord.Embed(title=event[3], description=event[4])

                                if event[6]:
                                    hex_str = '0x' + event[6]
                                    hex_int = int(hex_str, 16)                                    
                                    
                                    eventmessage=nextcord.Embed(title=event[3], description=event[4], color=hex_int)
                                
                                if event[5]:
                                    eventmessage.set_image(url=event[5])    

                                if event[8]:
                                    role = channel.guild.get_role(int(event[8]))
                                    if role != None:
                                        if role.name == '@everyone':
                                            await channel.send('@everyone',embed=eventmessage)
                                        else:
                                            await channel.send('{}'.format(role.mention),embed=eventmessage)
                                    else:
                                        await channel.send(embed=eventmessage)
                                elif not event[8]:
                                    await channel.send(embed=eventmessage)


                        elif event[1] == 'weekly':
                            if date_time <= now_time:
                                if now_time.strftime('%A %H:%M') == date_time.strftime('%A %H:%M'):

                                    channel = ninjabot.get_channel(int(event[0]))

                                    eventmessage=nextcord.Embed(title=event[3], description=event[4])

                                    if event[6]:
                                        hex_str = '0x' + event[6]
                                        hex_int = int(hex_str, 16)                                    
                                        
                                        eventmessage=nextcord.Embed(title=event[3], description=event[4], color=hex_int)
                                    
                                    if event[5]:
                                        eventmessage.set_image(url=event[5])

                                    if event[8]:
                                        role = channel.guild.get_role(int(event[8]))
                                        if role != None:
                                            if role.name == '@everyone':
                                                await channel.send('@everyone',embed=eventmessage)
                                            else:
                                                await channel.send('{}'.format(role.mention),embed=eventmessage)
                                        else:
                                            await channel.send(embed=eventmessage)
                                    elif not event[8]:
                                        await channel.send(embed=eventmessage)


                        elif event[1] == 'monthly':
                            if date_time <= now_time:
                                if now_time.strftime('%d %H:%M') == date_time.strftime('%d %H:%M'):

                                    channel = ninjabot.get_channel(int(event[0]))

                                    eventmessage=nextcord.Embed(title=event[3], description=event[4])

                                    if event[6]:
                                        hex_str = '0x' + event[6]
                                        hex_int = int(hex_str, 16)                                    
                                        
                                        eventmessage=nextcord.Embed(title=event[3], description=event[4], color=hex_int)
                                    
                                    if event[5]:
                                        eventmessage.set_image(url=event[5])

                                    if event[8]:
                                        role = channel.guild.get_role(int(event[8]))
                                        if role != None:
                                            if role.name == '@everyone':
                                                await channel.send('@everyone',embed=eventmessage)
                                            else:
                                                await channel.send('{}'.format(role.mention),embed=eventmessage)
                                        else:
                                            await channel.send(embed=eventmessage)
                                    elif not event[8]:
                                        await channel.send(embed=eventmessage)

                        elif event[1] == 'yearly':
                            if date_time <= now_time:
                                if now_time.strftime('%m-%d %H:%M') == date_time.strftime('%m-%d %H:%M'):

                                    channel = ninjabot.get_channel(int(event[0]))

                                    eventmessage=nextcord.Embed(title=event[3], description=event[4])

                                    if event[6]:
                                        hex_str = '0x' + event[6]
                                        hex_int = int(hex_str, 16)                                    
                                        
                                        eventmessage=nextcord.Embed(title=event[3], description=event[4], color=hex_int)
                                    
                                    if event[5]:
                                        eventmessage.set_image(url=event[5])

                                    if event[8]:
                                        role = channel.guild.get_role(int(event[8]))
                                        if role != None:
                                            if role.name == '@everyone':
                                                await channel.send('@everyone',embed=eventmessage)
                                            else:
                                                await channel.send('{}'.format(role.mention),embed=eventmessage)
                                        else:
                                            await channel.send(embed=eventmessage)
                                    elif not event[8]:
                                        await channel.send(embed=eventmessage)

                        elif event[1] == 'dayofmonth':
                            if date_time <= now_time:
                                if now_time.strftime('%A %H:%M') == date_time.strftime('%A %H:%M'):

                                    channel = ninjabot.get_channel(int(event[0]))
                                    eventmessage=nextcord.Embed(title=event[3], description=event[4])

                                    if event[6]:
                                        hex_str = '0x' + event[6]
                                        hex_int = int(hex_str, 16)                                    
                                        
                                        eventmessage=nextcord.Embed(title=event[3], description=event[4], color=hex_int)
                                    
                                    if event[5]:
                                        eventmessage.set_image(url=event[5])


                                    if int((now_time.strftime('%d')).lstrip('0')) in firstweek and int((date_time.strftime('%d')).lstrip('0')) in firstweek:

                                        if event[8]:
                                            role = channel.guild.get_role(int(event[8]))
                                            if role != None:
                                                if role.name == '@everyone':
                                                    await channel.send('@everyone',embed=eventmessage)
                                                else:
                                                    await channel.send('{}'.format(role.mention),embed=eventmessage)
                                            else:
                                                await channel.send(embed=eventmessage)
                                        elif not event[8]:
                                            await channel.send(embed=eventmessage)
                                    
                                    elif int((now_time.strftime('%d')).lstrip('0')) in secondweek and int((date_time.strftime('%d')).lstrip('0')) in secondweek:

                                        if event[8]:
                                            role = channel.guild.get_role(int(event[8]))
                                            if role != None:
                                                if role.name == '@everyone':
                                                    await channel.send('@everyone',embed=eventmessage)
                                                else:
                                                    await channel.send('{}'.format(role.mention),embed=eventmessage)
                                            else:
                                                await channel.send(embed=eventmessage)
                                        elif not event[8]:
                                            await channel.send(embed=eventmessage)

                                    elif int((now_time.strftime('%d')).lstrip('0')) in thirdweek and int((date_time.strftime('%d')).lstrip('0')) in thirdweek:

                                        if event[8]:
                                            role = channel.guild.get_role(int(event[8]))
                                            if role != None:
                                                if role.name == '@everyone':
                                                    await channel.send('@everyone',embed=eventmessage)
                                                else:
                                                    await channel.send('{}'.format(role.mention),embed=eventmessage)
                                            else:
                                                await channel.send(embed=eventmessage)
                                        elif not event[8]:
                                            await channel.send(embed=eventmessage)

                                    elif int((now_time.strftime('%d')).lstrip('0')) in fourthweek and int((date_time.strftime('%d')).lstrip('0')) in fourthweek:

                                        if event[8]:
                                            role = channel.guild.get_role(int(event[8]))
                                            if role != None:
                                                if role.name == '@everyone':
                                                    await channel.send('@everyone',embed=eventmessage)
                                                else:
                                                    await channel.send('{}'.format(role.mention),embed=eventmessage)
                                            else:
                                                await channel.send(embed=eventmessage)
                                        elif not event[8]:
                                            await channel.send(embed=eventmessage)

                                    elif int((now_time.strftime('%d')).lstrip('0')) in fifthweek and int((date_time.strftime('%d')).lstrip('0')) in fifthweek:

                                        if event[8]:
                                            role = channel.guild.get_role(int(event[8]))
                                            if role != None:
                                                if role.name == '@everyone':
                                                    await channel.send('@everyone',embed=eventmessage)
                                                else:
                                                    await channel.send('{}'.format(role.mention),embed=eventmessage)
                                            else:
                                                await channel.send(embed=eventmessage)
                                        elif not event[8]:
                                            await channel.send(embed=eventmessage)
                    except:
                        await ninjabot.startupchannel.send("Schedule ID {} failed and then removed @here\r\n{}\r\n{}\r\n{}".format(str(event[9]),str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
                        ninjabot.ninjabotsql.sql_insert(self.settings.eventremoval,(event[9],))

            ninjabot.schedcheck = 1

        stoppedgames = ninjabot.ninjabotsql.sql_novalues(self.settings.getstoppedgames)

        if stoppedgames:

            for stoppedgame in stoppedgames:
                answertime = datetime.datetime.today()
                oldtime = datetime.datetime.strptime(stoppedgame[1], timeformat)
                answerseconds = answertime - oldtime

                if answerseconds.total_seconds() >= 3:
                    channel = ''
                    try:
                        channel = ninjabot.get_channel(int(stoppedgame[2]))
                        channeltest = channel.id
                    except:
                        await ninjabot.startupchannel.send("Failed to pull channel for game timer. Clearing game for channel. @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
                        ninjabot.ninjabotsql.sql_insert(self.settings.nullgamemodesql,(int(stoppedgame[2]),))
                    
                    else:
                        ninjabot.ninjabotsql.sql_insert(self.settings.setstoppedgame,(0,None,None,stoppedgame[2]))
                        await ninjabot.ninjabotresponse.ninjabotresponse(ninjabot,channel,0,stoppedgame[0],'resume',thisisatest)
                        
        
        if int(interval) in range(10,60):
            
            ninjabot.schedcheck = 0
        
        activegames = ninjabot.ninjabotsql.sql_novalues(self.settings.getactivegames)

        if activegames:

            for activegame in activegames:
                answertime = datetime.datetime.today()
                oldtime = datetime.datetime.strptime(activegame[1], timeformat)
                answerseconds = answertime - oldtime
                
                if answerseconds.total_seconds() >= 30:
                    channel = ''
                    try:
                        channel = ninjabot.get_channel(int(activegame[2]))
                        channeltest = channel.id
                    except:
                        await ninjabot.startupchannel.send("Failed to pull channel for game timer. Clearing game for channel. @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
                        ninjabot.ninjabotsql.sql_insert(self.settings.nullgamemodesql,(int(activegame[2]),))
                    else:
                        await ninjabot.ninjabotresponse.ninjabotresponse(ninjabot,channel,0,activegame[0],'timesup',thisisatest)


        
        await asyncio.sleep(1)


            