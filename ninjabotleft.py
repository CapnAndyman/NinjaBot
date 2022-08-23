import nextcord
import sys
import time
import sys, os

class Ninjabotleft:
    async def ninjabotleft(self,ninjabot,message):
        
        try:

            self.settings = ninjabot.settings

            userchannel = '{0.channel.id}'.format(message)
            userid = message.author.id
            userinput = '{0.content}'.format(message).lower()
            guildowner = message.guild.owner_id
            userguild = message.guild.id

            if userinput == 'ninjabot left':
                if userid == guildowner:
                    channelcheck = ninjabot.ninjabotsql.sql_select(self.settings.checkleft,(userchannel,))
                    
                    if channelcheck:
                        ninjabot.ninjabotsql.sql_insert(self.settings.removeleft,(userchannel,))
                        await message.channel.send('Removed leave message from channel.')
                    else:
                        ninjabot.ninjabotsql.sql_insert(self.settings.addleft,(userchannel,userguild,time.strftime('%Y-%m-%d %H:%M:%S')))
                        await message.channel.send('Leave messages will now show here.')                        
                    
                else:
                    await message.channel.send('Sorry <@{0.author.id}>, only the server owner may use that command.'.format(message))


        except:
            await message.channel.send('Something went wrong with that command. Ask Andy.')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))