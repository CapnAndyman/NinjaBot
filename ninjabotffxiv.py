import nextcord
import requests
from bs4 import BeautifulSoup
import sys, os
import time

class Ninjabotffxiv:
    async def ninjabotffxiv(self,ninjabot,message,prefix):

        try:

            self.settings = ninjabot.settings
            fs = prefix + 'fflookup'

            def pulllist(character):
                urlname = character.replace(' ','+')
                baseurl = 'https://na.finalfantasyxiv.com/lodestone/character/?q='
                wholeurl = baseurl + urlname
                page = requests.get(wholeurl)
                soup = BeautifulSoup(page.content, "html.parser")
                refined = soup.find(class_="ldst__window")
                namelist = refined.find_all("p", class_="entry__name")
                worldlist = refined.find_all("p", class_="entry__world")
                linklist = refined.find_all("a", class_="entry__link")
                res = [[namelist[i].text, '`{}`'.format(worldlist[i].text), linklist[i]['href']] for i in range(len(namelist))]
                return res

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

            def listchars(charlist):
                #chardata = '\r\n'.join([' '.join(char[0:2]) for char in charlist])
                chardata = '\r\n'.join(str(i) + ' ' + [' '.join(char[0:2]) for char in charlist][i] for i in range(len(charlist)))
                if len(charlist) > 10:
                    #chardata = '\r\n'.join([' '.join(char[0:2]) for char in charlist[0:10]])
                    chardata = '\r\n'.join(str(i) + ' ' + [' '.join(char[0:2]) for char in charlist[0:10]][i] for i in range(10))
                listembed=nextcord.Embed(title='Character Results', description='Please select a character to see the stats.')
                listembed.add_field(name="Results", value=chardata)
                return listembed


            
            usermessage = '{0.content}'.format(message).lower()

            if usermessage == fs:
                ffxivhelpembed=nextcord.Embed(title="NinjaBot FFXIV Lookup", description="More Information")
                ffxivhelpembed.add_field(name="Lookup", value='Type `{0}` followed up the character name to look them up.\r\nExample: `{0} John Smith`'.format(fs), inline=False)
                ffxivhelpembed.add_field(name="Browsing", value='Use the numbers below the post to select the character.'.format(prefix), inline=False)
                await message.channel.send(embed=ffxivhelpembed)

            elif usermessage.startswith(fs):
                character = usermessage.replace(fs + ' ','')
                results = pulllist(character)

                if len(results) == 1:
                    await message.channel.send(embed=charactersheet(results[0][2]))

                    

                elif len(results) > 1:
                    # await message.channel.send('Not set up yet')
                    thismessage = await message.channel.send(embed=listchars(results))
                    
                    num2words = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', \
                        6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 0: '0️⃣'}

                    thislength = len(results)

                    ninjabot.ninjabotsql.sql_ffinsert(self.settings.addfflookup,(int(thismessage.id),';'.join([char[2] for char in results]),time.strftime('%Y-%m-%d %H:%M:%S')))

                    if len(results) > 10:
                        thislength = 10

                    for num in range(0,thislength):
                        emoji = num2words[num]
                        await thismessage.add_reaction(emoji)

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))