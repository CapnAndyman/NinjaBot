import nextcord
import sys
import time
import sys, os
import emoji
import re

class Ninjabotroles:
    async def ninjabotroles(self,ninjabot,message):
        
        try:

            self.settings = ninjabot.settings

            userchannel = '{0.channel.id}'.format(message)
            userid = '{0.author.id}'.format(message)
            userinput = '{0.content}'.format(message).lower()
            usermessage = '{0.id}'.format(message)

            userinput = userinput.replace('<',' <').replace('>','> ')

            while '  ' in userinput:
                userinput = userinput.replace('  ',' ')

            userinput = userinput.rstrip().lstrip()

            filleremoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', \
                '6️⃣', '7️⃣', '8️⃣', '9️⃣', '0️⃣', '🇦', '🇧', '🇨', '🇩', '🇪']

            if userinput == 'ninjabot roles':
                await message.channel.send('Placeholder response.')
            
            # elif userinput.startswith('ninjabot roles') and len(userinput.split(' ')) == 3:
            elif userinput.startswith('ninjabot roles '):

                rolelist = userinput.replace('ninjabot roles ','').split(' ')

                if message.author.guild_permissions.manage_roles:

                    if message.guild.get_member(ninjabot.user.id).guild_permissions.manage_roles:
                        currentemoji = ''
                        currentrole = ''
                        rolestring = {}
                        for item in rolelist:
                            if item.startswith('<@&'):
                                if currentrole:
                                    currentemoji = filleremoji.pop(0)
                                    rolestring[currentemoji] = currentrole
                                    currentemoji = ''
                                    currentrole = ''  

                                if item == rolelist[-1]:
                                    currentemoji = filleremoji.pop(0)

                                currentrole = item
                            elif emoji.emoji_list(item) != [] and len(item) == 1:
                                currentemoji = emoji.emoji_list(item)[0]['emoji']
                                if currentemoji in rolestring:
                                    currentemoji = filleremoji.pop(0)

                            elif item.startswith('<:'):

                                pattern = r":\w*:"

                                def clean(string):
                                    result = re.search(pattern, string)
                                    return(result.group())

                                currentemoji = clean(item)
                            
                            if item.startswith('<a:'):
                                currentemoji = filleremoji.pop(0)

                            if currentemoji and currentrole:
                                rolestring[currentemoji] = currentrole
                                if currentemoji in filleremoji:
                                    filleremoji.remove(currentemoji)
                                currentemoji = ''
                                currentrole = ''

                        messagedata = ''

                        for key, value in rolestring.items():
                            stringemoji = key
                            if key.startswith(':'):
                                stringemoji = str(nextcord.utils.get(message.guild.emojis, name=key.replace(':','')))
                            messagedata = messagedata + ' '.join([stringemoji,value]) + '\r\n'
                            
                        
                        listembed=nextcord.Embed(title='Ninjabot Roles', description='React using the following emotes to be assigned a role.')
                        listembed.add_field(name="Roles", value=messagedata)
                        thismessage = await message.channel.send(embed=listembed)

                        for key, value in rolestring.items():
                            sqlrole = value.replace('<@&','').replace('>','')
                            ninjabot.ninjabotsql.sql_insert(self.settings.addrolesql,(thismessage.id,sqlrole,userchannel,message.guild.id,time.strftime('%Y-%m-%d %H:%M:%S'),key.replace(':','')))
                            if key.startswith(':'):
                                key = nextcord.utils.get(message.guild.emojis, name=key.replace(':',''))
                            await thismessage.add_reaction(key)
                        

                        # role = ''
                        
                        # if userinput.split(' ')[-1].startswith('<@&'):
                            
                        #     role = message.guild.get_role(int(userinput.split(' ')[-1].replace('<@&','').replace('>','')))


                        # else:
                            
                        #     role = nextcord.utils.get(message.guild.roles, name=userinput.split(' ')[-1])

                        # try:
                        #     me = message.guild.get_member(ninjabot.user.id)
                        #     await me.add_roles(role)
                        # except:
                        #     await message.channel.send('Sorry <@{0.author.id}>, I cannot seem to manage that role. Try remaking it or dropping it down the role list.'.format(message))
                        # else:
                        #     if role != '' or role != None:

                        #         me = message.guild.get_member(ninjabot.user.id)
                        #         await me.remove_roles(role)
                        #         ninjabot.ninjabotsql.sql_insert(self.settings.addrolesql,(message.id,role.id,userchannel,message.guild.id,time.strftime('%Y-%m-%d %H:%M:%S')))
                        #         await message.channel.send('That message checks out. Start reacting to it to be added to the <@&{}> role.\r\nYou may also edit the message to look cleaner!\r\nFeel free to delete this message as well.'.format(role.id))
                                

                        #     else:
                                


                        #         await message.channel.send('Sorry <@{0.author.id}>, this message will not work for joining roles. Please try again.'.format(message))

                    else:
                        await message.channel.send('Sorry <@{0.author.id}>, I do not have permissions to manage roles. I will need this to give members roles.'.format(message))

                else:
                    await message.channel.send('Sorry <@{0.author.id}>, you do not have permissions to manage roles.'.format(message))


        except:
            await message.channel.send('This message will not work for joining roles. Please try again.')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))
            