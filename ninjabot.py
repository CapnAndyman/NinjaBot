#Before Ninjabot will run, you will need to fill out credentials.py
from credentials import Credentials

import nextcord
import requests
from bs4 import BeautifulSoup
from pysyllables import get_syllable_count
from ninjabotsettings import Ninjabotsettings
from ninjabotresponse import Ninjabotresponse
from ninjabotdice import Ninjabotdice
from ninjabothangman import Ninjabothangman
from ninjabottrivia import Ninjabottrivia
from ninjabotschedule import Ninjabotschedule
from ninjabotannounce import Ninjabotannounce
from ninjabotsql import Ninjabotsql
from ninjabotkanji import Ninjabotkanji
from ninjabotasl import Ninjabotasl
from ninjabotkana import Ninjabotkana
from ninjabotgana import Ninjabotgana
from ninjabotjapanese import Ninjabotjapanese
from ninjabotnihongo import Ninjabotnihongo
from ninjabotfrench import Ninjabotfrench
from ninjabothaiku import Ninjabothaiku
from ninjabotminesweeper import Ninjabotminesweeper
from ninjabotriddle import Ninjabotriddle
from ninjabotdictionary import Ninjabotdictionary
from ninjabotroles import Ninjabotroles
from ninjabotleft import Ninjabotleft
from ninjabotffxiv import Ninjabotffxiv
import dbots
import time
import sys

#Set this to 0 if you want to run the prod version. Set this to 1 to run the test version.
thisisatest = 0

#Don't touch this. This is how Ninjabot knows it has already started. This prevents the announce loop from starting more than once.
thisstarted = 0

class MyClient(nextcord.Client):
    
    async def on_ready(self):

        global thisstarted
        if thisstarted == 0:

            print('Logged on as {0}!'.format(self.user))
            self.settings = Ninjabotsettings()
            self.ninjabotresponse = Ninjabotresponse()
            self.ninjabotdice = Ninjabotdice()
            self.ninjabothangman = Ninjabothangman()
            self.ninjabottrivia = Ninjabottrivia()
            self.ninjabotschedule = Ninjabotschedule()
            self.ninjabotannounce = Ninjabotannounce()
            self.ninjabotsql = Ninjabotsql()
            self.ninjabotkanji = Ninjabotkanji()
            self.ninjabotasl = Ninjabotasl()
            self.ninjabotkana = Ninjabotkana()
            self.ninjabotgana = Ninjabotgana()
            self.ninjabotjapanese = Ninjabotjapanese()
            self.ninjabotnihongo = Ninjabotnihongo()
            self.ninjabotfrench = Ninjabotfrench()
            self.ninjabothaiku = Ninjabothaiku()
            self.ninjabotminesweeper = Ninjabotminesweeper()
            self.ninjabotriddle = Ninjabotriddle()
            self.ninjabotdictionary = Ninjabotdictionary()
            self.ninjabotroles = Ninjabotroles()
            self.ninjabotleft = Ninjabotleft()
            self.ninjabotffxiv = Ninjabotffxiv()
            
            self.statusid = 1
            self.schedcheck = 1
            if thisisatest == 0:
                self.startupchannel = self.get_channel(Credentials.prodchannel)
                self.devchannel = self.get_channel(Credentials.prodchanneltest)
            elif thisisatest == 1:
                self.startupchannel = self.get_channel(Credentials.devchannel)
                self.devchannel = self.get_channel(Credentials.devchanneltest)
            if thisisatest == 0:
                await self.startupchannel.send('Starting up NinjaBot @here')
                self.theposter = poster
            elif thisisatest == 1:
                await self.startupchannel.send('Starting up NinjaBot Test @here')
            self.currentguilds = self.guilds
            thisstarted = 1
            while True:
                try:
                    await self.ninjabotannounce.ninjabotannounce(self,thisisatest)
                except:
                    await self.startupchannel.send("Announce loop failed @here\r\n{}\r\n{}\r\n{}".format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
                    if thisisatest == 1:
                        raise
            exit()

    # async def on_disconnect(self):
    #     exit()

    async def on_member_remove(self, member):
        try:
            leftcheck = self.ninjabotsql.sql_select(self.settings.getleftchannels,(member.guild.id,))
            for singlechannel in leftcheck:
                try:
                    thischannel = self.get_channel(singlechannel[0])
                    await thischannel.send('{0} has left the server.'.format(member.name))
                except:
                    self.ninjabotsql.sql_insert(self.settings.removeleft,(singlechannel[0]))
        except:
            await self.startupchannel.send('On Leave Error.\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
            
        
    
    async def on_raw_reaction_add(self, payload):
        rolecheck = self.ninjabotsql.sql_select(self.settings.getrolemessage,(payload.message_id,payload.emoji.name))
        ffcheck = self.ninjabotsql.sql_ffselect(self.settings.checkfflookup,(payload.message_id,))

        if rolecheck and not payload.member.bot:
            try:
                thisguild = self.get_guild(int(rolecheck[0][1]))
                thisrole = thisguild.get_role(int(rolecheck[0][0]))
                await payload.member.add_roles(thisrole)
            except:
                await self.startupchannel.send('Unable to add role\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))

        elif ffcheck and not payload.member.bot:
            try:
                num2words = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, \
                    '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9, '0️⃣': 0}
                
                def charactersheet(charlink):
                    baseurl = 'https://na.finalfantasyxiv.com'
                    wholeurl = baseurl + charlink
                    page = requests.get(wholeurl)
                    soup = BeautifulSoup(page.content, "html.parser")
                    refined = soup.find(class_="ldst__window")
                    smallpic = refined.find("img", class_="character-block__face")['src']
                    bigpic = refined.find("a", class_="js__image_popup")['href']
                    charworld = refined.find("p", class_="frame__chara__world").text
                    charname = refined.find("p", class_="frame__chara__name").text
                    jobrefined = soup.find(class_="character__profile__detail").find(class_="js__character_toggle")
                    jobnames = jobrefined.find_all("img", class_="js__tooltip")
                    joblevels = jobrefined.find_all("li")
                    jobdata = '\r\n'.join([' Level '.join(job) for job in [[jobnames[i]['data-tooltip'], joblevels[i].text] for i in range(len(joblevels)) if not '-' in joblevels[i].text]])                
                    sheetembed=nextcord.Embed(title='Character Stats', description=charworld)
                    sheetembed.add_field(name="Jobs", value=jobdata)
                    sheetembed.set_author(name=charname, icon_url=smallpic)
                    sheetembed.set_image(url=bigpic)
                    return sheetembed

                thisemoji = payload.emoji.name
                thischar = ffcheck[0][0].split(';')[num2words[thisemoji]]
                thisguild = self.get_guild(payload.guild_id)
                thischannel = thisguild.get_channel(payload.channel_id)
                thismessage = thischannel.get_partial_message(payload.message_id)
                await thismessage.edit(embed=charactersheet(thischar))

            except:
                await self.startupchannel.send('Unable to update ff embed\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))            

    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        rolecheck = self.ninjabotsql.sql_select(self.settings.getrolemessage,(payload.message_id,emoji))
        ffcheck = self.ninjabotsql.sql_ffselect(self.settings.checkfflookup,(payload.message_id,))

        if rolecheck:
            try:
                thisguild = self.get_guild(int(rolecheck[0][1]))
                thisrole = thisguild.get_role(int(rolecheck[0][0]))
                thismember = thisguild.get_member(payload.user_id)
                try:
                    await thismember.remove_roles(thisrole)
                except:
                    await self.startupchannel.send('Unable to remove role\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))
            except:
                await self.startupchannel.send('Unable to remove role\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))

        elif ffcheck:
            try:
                num2words = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, \
                    '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9, '0️⃣': 0}
                
                def charactersheet(charlink):
                    baseurl = 'https://na.finalfantasyxiv.com'
                    wholeurl = baseurl + charlink
                    page = requests.get(wholeurl)
                    soup = BeautifulSoup(page.content, "html.parser")
                    refined = soup.find(class_="ldst__window")
                    smallpic = refined.find("img", class_="character-block__face")['src']
                    bigpic = refined.find("a", class_="js__image_popup")['href']
                    charworld = refined.find("p", class_="frame__chara__world").text
                    charname = refined.find("p", class_="frame__chara__name").text
                    jobrefined = soup.find(class_="character__profile__detail").find(class_="js__character_toggle")
                    jobnames = jobrefined.find_all("img", class_="js__tooltip")
                    joblevels = jobrefined.find_all("li")
                    jobdata = '\r\n'.join([' Level '.join(job) for job in [[jobnames[i]['data-tooltip'], joblevels[i].text] for i in range(len(joblevels)) if not '-' in joblevels[i].text]])                
                    sheetembed=nextcord.Embed(title='Character Stats', description=charworld)
                    sheetembed.add_field(name="Jobs", value=jobdata)
                    sheetembed.set_author(name=charname, icon_url=smallpic)
                    sheetembed.set_image(url=bigpic)
                    return sheetembed

                thisemoji = payload.emoji.name
                thischar = ffcheck[0][0].split(';')[num2words[thisemoji]]
                thisguild = self.get_guild(payload.guild_id)
                thischannel = thisguild.get_channel(payload.channel_id)
                thismessage = thischannel.get_partial_message(payload.message_id)
                await thismessage.edit(embed=charactersheet(thischar))

            except:
                await self.startupchannel.send('Unable to update ff embed\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))   

    async def on_message(self, message):
        if not message.author.bot:
            if thisisatest == 1:
                print(message.content)
            userchannel = '{0.channel.id}'.format(message)
            
            syllcount = 0
            if not self.ninjabotsql.sql_select(self.settings.checkchannelsql,(message.channel.id,))[0][0]:
                self.ninjabotsql.sql_insert(self.settings.insertchannelsql,(message.channel.id,time.strftime('%Y-%m-%d %H:%M:%S'),))
            userchannel = '{0.channel.id}'.format(message)
            prefix = self.ninjabotsql.sql_select(self.settings.getprefix,(userchannel,))[0]
            try:
                characters_to_remove = '!?,."-'

                new_string = '{0.content}'.format(message).lower().replace('  ',' ').replace('\r\n',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
                
                for character in characters_to_remove:
                    new_string = new_string.replace(character, "")
                
                for eachword in new_string.split(' '):

                    syllcount = syllcount + get_syllable_count(eachword.replace('’',"'"))
            except:
                syllcount = 0
            finally:
                goahead = ''
                try: 
                    if '{0.content}'.format(message).lower().startswith(self.settings.longcommand) or '{0.content}'.format(message).lower().startswith(prefix[0]) or syllcount == 17 or prefix[1]:
                        goahead = 'go'

                except:
                    print('Not ready yet or some other problem')
                else:

                    if goahead == 'go':
                        if not self.ninjabotsql.sql_select(self.settings.checkusersql,(message.author.id,))[0][0]:
                            self.ninjabotsql.sql_insert(self.settings.insertusersql,(message.author.id,time.strftime('%Y-%m-%d %H:%M:%S'),0,0))
                        
                        gamemode = self.ninjabotsql.sql_select(self.settings.gamemodesql,(userchannel,))[0]

                        await self.ninjabotresponse.ninjabotresponse(self,message,syllcount,gamemode[0],str(prefix[0]),thisisatest)


intents = nextcord.Intents(messages=True, guilds=True, reactions=True, members=True)

client = MyClient(intents=intents)

poster = ''

if thisisatest == 0:

    poster = dbots.ClientPoster(client, 'discord.py', api_keys = {
        'top.gg': Credentials.topgg,
        'discord.bots.gg': Credentials.discordbotsgg
    })

    client.run(Credentials.prodcreds)

elif thisisatest == 1:

    client.run(Credentials.devcreds)
