#from textstat import syllable_count
from pysyllables import get_syllable_count
import nextcord
import sys, os

class Ninjabothaiku:
    
    async def ninjabothaiku(self,ninjabot,message):

        try:

            self.settings = ninjabot.settings

            userchannel = '{0.channel.id}'.format(message)

            haikustatus = ninjabot.ninjabotsql.sql_select(self.settings.haikuchecksql,(userchannel,))[0][0]

            def wordsanitize(new_string):
                characters_to_remove = '!?,."-'
                
                for character in characters_to_remove:
                    new_string = new_string.replace(character, "")

                return new_string
            
            if '{0.content}'.format(message).lower() == self.settings.haiku:

                haikustatus = int(haikustatus) * -1

                if haikustatus == -1:

                    await message.channel.send("NinjaBot Haiku is now disabled for this channel.")

                elif haikustatus == 1:

                    await message.channel.send("NinjaBot Haiku is now enabled for this channel.")

                ninjabot.ninjabotsql.sql_insert(self.settings.haikuswapsql,(haikustatus,userchannel))

            elif haikustatus == 1:
            
                splitmessage = '{0.content}'.format(message).replace('  ',' ').replace('\r\n',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ').split(' ')
                
                haikuone = ''
                haikutwo = ''
                haikuthree = ''

                haikucountone = 0
                haikucounttwo = 0
                haikucountthree = 0

                author = '- {0.author.name}'.format(message)

                while haikucountone < 5:

                    if not haikuone:

                        haikucountone = haikucountone + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                        haikuone += splitmessage.pop(0)

                    elif haikuone:
                        
                        haikucountone = haikucountone + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                        haikuone += ' ' + splitmessage.pop(0)

                
                if haikucountone == 5:

                    haikuone = '_' + haikuone + '_'

                    while haikucounttwo < 7:

                        if not haikutwo:

                            haikucounttwo = haikucounttwo + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                            haikutwo += splitmessage.pop(0)

                        elif haikutwo:

                            haikucounttwo = haikucounttwo + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                            haikutwo += ' ' + splitmessage.pop(0)

                if haikucounttwo == 7:

                    haikutwo = '_' + haikutwo + '_'
                    
                    while haikucountthree < 5:

                        if not haikuthree:

                            haikucountthree = haikucountthree + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                            haikuthree += splitmessage.pop(0)

                        elif haikuthree:

                            haikucountthree = haikucountthree + get_syllable_count(wordsanitize(splitmessage[0]).replace('’',"'"))
                            haikuthree += ' ' + splitmessage.pop(0)

                if haikucountthree == 5:

                    haikuthree = '_' + haikuthree + '_'
                    
                    haikulines = haikuone,haikutwo,haikuthree,author

                    fullhaiku = '\r\n\r\n'.join(haikulines)

                    haikuresponse=nextcord.Embed(title="NinjaBot Haiku", description=fullhaiku)
                    
                    await message.channel.send(embed=haikuresponse)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))
