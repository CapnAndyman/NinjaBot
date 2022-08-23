import nextcord
import random
from pathlib import Path
import os.path
from os import path
from datetime import datetime
import pytz
import string
import re
import time

class Ninjabotschedule:
    async def ninjabotschedule(self,ninjabot,message):
        # Opening variables
        self.settings = ninjabot.settings
        userguild = message.guild.id
        userid = message.author.id
        guildowner = message.guild.owner_id

        firstweek = range(1,8)
        secondweek = range(8,15)
        thirdweek = range(15,22)
        fourthweek = range(22,29)
        fifthweek = range(29,32)
        
        #Place message into a variable
        command = '{0.content}'.format(message)
        #Split message into a list
        commandlist = command.split(' ')
        #Remove 'ninjabot schedule' from commandlist
        del commandlist[0]
        del commandlist[0]
        #All channels in the source server
        channellist = message.guild.channels


        #Help Command
        if commandlist == [] or commandlist[0].lower() == 'help':
            await message.channel.send(
                embed=self.settings.ninjabotschedulehelpinfo
                )
        #List Command
        elif commandlist[0].lower() == 'list':
            eventlist = ninjabot.ninjabotsql.sql_select(self.settings.listeventssql,(userguild,))

            if eventlist:
                
                formattedlist = ''

                for event in eventlist:
                    
                    event = list(event)

                    date_time = ''

                    thisday = ''
                    
                    if event[3]:
                        
                        date_time = datetime.strptime(event[3], '%Y-%m-%d %H:%M:%S')

                        if int(date_time.strftime('%d')) in firstweek:
                            thisday = 'First'
                        elif int(date_time.strftime('%d')) in secondweek:
                            thisday = 'Second'
                        elif int(date_time.strftime('%d')) in thirdweek:
                            thisday = 'Third'
                        elif int(date_time.strftime('%d')) in fourthweek:
                            thisday = 'Fourth'
                        elif int(date_time.strftime('%d')) in fifthweek:
                            thisday = 'Fifth'

                    eventchannel = ninjabot.get_channel(event[1]).name


                    if not event[5]:

                        event[5] = 'America/Los_Angeles'
                    
                    if not event[4]:

                        event[4] = 'None'

                    if not event[3]:
                        
                        formattedlist = formattedlist + 'Event ID ' + str(event[0]) + ' - ' + event[4] + ' - Unscheduled in ' + eventchannel + '\r\n'

                    elif event[2] == 'once':
                        formattedlist = formattedlist + str(event[0]) + ' - ' + event[4] + ' - ' + 'Once in ' + date_time.strftime('%Y') + ' on ' + date_time.strftime('%B %d') + ' at ' + date_time.strftime('%H:%M') + ' in ' + eventchannel + '\r\n'
                    elif event[2] == 'weekly':
                        formattedlist = formattedlist + str(event[0]) + ' - ' + event[4] + ' - ' + 'Weekly on ' + date_time.strftime('%A') + ' at ' + date_time.strftime('%H:%M') + ' in ' + eventchannel + '\r\n'
                    elif event[2] == 'monthly':
                        formattedlist = formattedlist + str(event[0]) + ' - ' + event[4] + ' - ' + 'Monthly on day ' + date_time.strftime('%d') + ' at ' + date_time.strftime('%H:%M') + ' in ' + eventchannel + '\r\n'
                    elif event[2] == 'yearly':
                        formattedlist = formattedlist + str(event[0]) + ' - ' + event[4] + ' - ' + 'Yearly on ' + date_time.strftime('%B %d') + ' at ' + date_time.strftime('%H:%M') + ' in ' + eventchannel + '\r\n'
                    elif event[2] == 'dayofmonth':
                        formattedlist = formattedlist + str(event[0]) + ' - ' + event[4] + ' - ' + 'On the ' + thisday + ' ' + date_time.strftime('%A') + ' at ' + date_time.strftime('%H:%M') + ' in ' + eventchannel + '\r\n'

                
                await message.channel.send(formattedlist)

            else:

                await message.channel.send(self.settings.nosched.format(message))

        #Check if server owner for the rest of the commands
        elif userid == guildowner:
            #Create Command    
            if commandlist[0].lower() == 'create':
                if len(commandlist) == 3:
                    #Check if channel is valid in server
                    if commandlist[2].lower() in (name.name for name in channellist):
                        #Validate the command only contains 3 words
                        if len(commandlist) == 3:
                            #Validate the event type
                            if commandlist[1].lower() in self.settings.eventlist:
                                #Pull the ID for the channel in the command
                                channel = nextcord.utils.get(ninjabot.get_guild(int(userguild)).text_channels, name=commandlist[2].lower())
                                #Create the database row for the event and return the ID of the event.
                                eventid = ninjabot.ninjabotsql.sql_insert(self.settings.insertschedulesql,(userguild,channel.id,userid,time.strftime('%Y-%m-%d %H:%M:%S'),commandlist[1].lower()))
                                #Send a message back verifying event creation with the ID.
                                await message.channel.send('Event successfully created with an ID of ' + str(eventid) + '. Please use "ninjabot schedule modify ' + str(eventid) + '" commands to set additional parameters.'.format(message))
                        #Tell the user they need to provide more info
                        elif len(commandlist) == 2:
                            message.channel.send(self.settings.nodata.format(message))
            #Modify Command        
            elif commandlist[0].lower() == 'modify':
                
                eventguild = ninjabot.ninjabotsql.sql_select(self.settings.checkeventownersql,(commandlist[1],))
                
                if eventguild:
                    eventguildowner = ninjabot.get_guild(int(eventguild[0][0])).owner_id

                    allowedusers = []
                    allowedusers.append(eventguildowner)
                    
                    if userid in allowedusers:
                        #Make sure the command is 4 words or longer
                        if len(commandlist) >= 4:
                            #Make sure the event has been created
                            if ninjabot.ninjabotsql.sql_select(self.settings.checkeventsql,(commandlist[1],))[0][0]:
                                #Change the event channel
                                if commandlist[2].lower() == 'channel':
                                    #Validate the new channel
                                    if commandlist[3].lower() in (name.name for name in channellist):
                                        #Get the new channels ID
                                        updated = nextcord.utils.get(ninjabot.get_guild(int(userguild)).text_channels, name=commandlist[3].lower())
                                        #Update the event in the database with the new channel
                                        ninjabot.ninjabotsql.sql_insert(self.settings.modifychannel,(updated,commandlist[1]))
                                        #Tell the user the event has been updated
                                        await message.channel.send('Event successfully modified.'.format(message))
                                #Change the event type
                                elif commandlist[2].lower() == 'type':
                                    #Validate the event type
                                    if commandlist[3].lower() in self.settings.eventlist:
                                        #Update the event in the database with the new type
                                        ninjabot.ninjabotsql.sql_insert(self.settings.modifytype,(commandlist[3].lower(),commandlist[1]))
                                        await message.channel.send('Event successfully modified.'.format(message))
                                #Change/Set the date for the first instance of the event
                                elif commandlist[2].lower() == 'date':
                                    datecheck = commandlist[3].split('-')
                                    #Validate the year
                                    if int(datecheck[0]) in self.settings.yearlist:
                                        #Validate the month
                                        if datecheck[1] in self.settings.numericmonthlist:
                                            #Validate the date on the calendar
                                            if int(datecheck[2]) in self.settings.datelist:
                                                #Validate the time
                                                if commandlist[4] in self.settings.timelist:
                                                    #Append seconds for storing
                                                    commandlist[4] = commandlist[4] + ':00'
                                                    #Validate the words in the command is 5
                                                    if len(commandlist) == 5:
                                                        #Format the time so it can be stored
                                                        timevalue = commandlist[3] + ' ' + commandlist[4]
                                                        #Update/Set the time in the DB
                                                        ninjabot.ninjabotsql.sql_insert(self.settings.modifydate,(timevalue,commandlist[1]))

                                                        #Send confirmation of event modification
                                                        await message.channel.send('Event successfully modified.'.format(message))
                                                    #Tell user that command is too long
                                                    else:
                                                        await message.channel.send(self.settings.extravalue.format(message))
                                                #Tell user that the time is in the wrong format
                                                else:
                                                    await message.channel.send(self.settings.wrongtime.format(message))
                                            #Tell the user that the date is invalid
                                            else:
                                                await message.channel.send(self.settings.wrongdate.format(message))
                                        #Tell the user that the month is invalid
                                        else:
                                            await message.channel.send(self.settings.wrongmon.format(message))
                                    #Tell the user the year is invalid
                                    else:
                                        await message.channel.send(self.settings.wrongyear.format(message))                            
                                #Title modification
                                elif commandlist[2].lower() == 'title':
                                    #Put together the title information into a string
                                    titlevalue = ' '.join(commandlist[3:])
                                    #Push title to database
                                    ninjabot.ninjabotsql.sql_insert(self.settings.modifytitle,(titlevalue,commandlist[1]))
                                    await message.channel.send('Event successfully modified.'.format(message))
                                #Description modification
                                elif commandlist[2].lower() == 'description':
                                    #Put together the description information into a string
                                    descriptionvalue = ' '.join(commandlist[3:])
                                    ninjabot.ninjabotsql.sql_insert(self.settings.modifydescription,(descriptionvalue,commandlist[1]))    
                                    await message.channel.send('Event successfully modified.'.format(message))                        
                                #Image modification
                                elif commandlist[2].lower() == 'image':
                                    #Push image to db
                                    ninjabot.ninjabotsql.sql_insert(self.settings.modifyimage,(commandlist[3],commandlist[1]))   
                                    await message.channel.send('Event successfully modified.'.format(message))                          
                                #Color modification
                                elif commandlist[2].lower() == 'color':
                                    #Validate hex falues
                                    commandlist[3] = commandlist[3].lower().replace('#','')
                                    if len(commandlist[3]) == 6:
                                        if commandlist[3].lower()[0:2] in self.settings.hexlist and commandlist[3].lower()[2:4] in self.settings.hexlist and commandlist[3].lower()[4:6] in self.settings.hexlist:
                                            #Store color in database
                                            ninjabot.ninjabotsql.sql_insert(self.settings.modifycolor,(commandlist[3].lower(),commandlist[1]))
                                            await message.channel.send('Event successfully modified.'.format(message))
                                #Timezone modification
                                elif commandlist[2].lower() == 'timezone':
                                    #Validate Timezone
                                    if commandlist[3].lower() in (name.lower() for name in pytz.all_timezones):
                                        for tzo in pytz.all_timezones:
                                            if re.match(commandlist[3].lower(), tzo, re.IGNORECASE):
                                                #Replace timezone with properly formatted one
                                                commandlist[3] = tzo
                                                #Push Timezone to db
                                                ninjabot.ninjabotsql.sql_insert(self.settings.modifytz,(commandlist[3],commandlist[1]))
                                                await message.channel.send('Event successfully modified.'.format(message))
                                #Mentioned user or group
                                elif commandlist[2].lower() == 'mention':
                                    #Clean mention
                                    mentionvalue = ' '.join(commandlist[3:])
                                    if mentionvalue.startswith('<@&'):
                                        role = message.guild.get_role(int(mentionvalue.replace('<@&','').replace('>','')))
                                        if role != None:
                                            ninjabot.ninjabotsql.sql_insert(self.settings.modifymention,(role.id,commandlist[1]))
                                            await message.channel.send('Event successfully modified.')
                                        else:
                                            await message.channel.send('Invalid role. Check case and spelling.')
                                    elif not mentionvalue.startswith('<@&'):
                                        if mentionvalue == 'everyone':
                                            mentionvalue = '@everyone'
                                        role = nextcord.utils.get(message.guild.roles, name=mentionvalue)
                                        if role != None:
                                            ninjabot.ninjabotsql.sql_insert(self.settings.modifymention,(role.id,commandlist[1]))
                                            await message.channel.send('Event successfully modified.')
                                        else:
                                            await message.channel.send('Invalid role. Check case and spelling.')

                    else:
                        await message.channel.send(self.settings.securityfailure.format(message))

                else:
                    await message.channel.send(self.settings.wrongevent.format(message))

            elif commandlist[0].lower() == 'preview':

                eventinfo = ninjabot.ninjabotsql.sql_select(self.settings.geteventsql,(commandlist[1],))

                if eventinfo:
                    
                    eventinfo = list(eventinfo[0])

                    if not eventinfo[3]:
                        eventinfo[3] = 'NONE'

                    if not eventinfo[4]:
                        eventinfo[4] = 'NONE'
                    
                    eventguildowner = ninjabot.get_guild(int(eventinfo[8])).owner_id
                    previeweventchannel = str(ninjabot.get_channel(int(eventinfo[0])).name)
                    
                    allowedusers = []
                    allowedusers.append(eventguildowner)

                    if userid in allowedusers:

                        eventmessage=nextcord.Embed(title=eventinfo[3], description=eventinfo[4])

                        if eventinfo[6]:
                            hex_str = '0x' + eventinfo[6]
                            hex_int = int(hex_str, 16)                                    
                            
                            eventmessage=nextcord.Embed(title=eventinfo[3], description=eventinfo[4], color=hex_int)
                        
                        if eventinfo[5]:
                            eventmessage.set_image(url=eventinfo[5])    

                        if eventinfo[9]:
                            role = message.guild.get_role(int(eventinfo[9]))
                            if role != None:    
                                await message.channel.send('This event will go off in #{} and notify {}'.format(previeweventchannel,role.name),embed=eventmessage)
                            else:
                                await message.channel.send('This event will go off in #{}'.format(previeweventchannel),embed=eventmessage)
                        
                        elif not eventinfo[9]:

                            await message.channel.send('This event will go off in #{}'.format(previeweventchannel),embed=eventmessage)
                        
                    else:
                        await message.channel.send(self.settings.securityfailure.format(message))

                else:
                    await message.channel.send(self.settings.wrongevent.format(message))
            
            elif commandlist[0].lower() == 'remove':

                eventguild = ninjabot.ninjabotsql.sql_select(self.settings.checkeventownersql,(commandlist[1],))

                if eventguild:

                    eventguildowner = ninjabot.get_guild(int(eventguild[0][0])).owner_id

                    allowedusers = []
                    allowedusers.append(eventguildowner)
                    
                    if userid in allowedusers:

                        ninjabot.ninjabotsql.sql_insert(self.settings.eventremoval,(commandlist[1],))
                        await message.channel.send('Event removed.'.format(message))


                else:
                    await message.channel.send(self.settings.wrongevent.format(message))

        else:
            await message.channel.send(self.settings.securityfailure.format(message))        
            # elif commandlist[0] == 'security':
