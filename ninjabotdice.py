import nextcord
import random
import re
import sys, os

class Ninjabotdice:
    async def ninjabotdice(self,ninjabot,message,prefix,thisisatest):

        try:

            self.settings = ninjabot.settings

            equations = ['+','-','*','/']

            helpembed=nextcord.Embed(title="Ninjabot Dice", description="How to play NinjaBot Dice", color=nextcord.Color.green())
            helpembed.add_field(name="Single Rolls".format(prefix), value="Example: `{0}dice d20`\r\nRolls a single die with a size of your choosing.\r\nThe number of sides is not limited.\r\nTry `{0}dice d10000`.".format(prefix), inline=False)   
            helpembed.add_field(name="Multi Rolls".format(prefix), value="Example: `{0}dice 5d20`\r\nRolls multiple dice with a size of your choosing.\r\nThe number of sides is not limited, but there is a max of 20 rolls.".format(prefix), inline=False)   
            helpembed.add_field(name="Equation Rolls".format(prefix), value="Examples: `{0}dice d20+5` or `{0}dice 5d20-5`\r\nRolls a single die or multiple dice with sizes of your choosing with added equations.\r\nThe number of sides is not limited, but there is a max of 20 rolls.".format(prefix), inline=False)   
            helpembed.add_field(name="Multiple Individual Rolls".format(prefix), value="Examples: `{0}dice 5d20 4d6` or `{0}dice d20+5 5d6-3`\r\nRolls multiple dice individually with optional equations.\r\nThe number of sides is not limited, but there is a max of 20 rolls.".format(prefix), inline=False)   
            helpembed.add_field(name="Multiple Equation Rolls".format(prefix), value="Examples: `{0}dice 3d20+5d6` or `{0}dice 5d20-5d6`\r\nRolls multiple dice together with sizes of your choosing and added equations.\r\nThe number of sides is not limited, but there is a max of 20 rolls.".format(prefix), inline=False)
            helpembed.add_field(name="More Information".format(prefix), value="You can string together multiple roll-types, so go wild!\r\nExample: `{0}dice 3d20+5d6+5d20-5d6+5+3d10`".format(prefix), inline=False)

            dice = prefix + 'dice'
            
            def rollme(thisroll):

                answerstring = ''
                rolltotal = ''
                
                if thisroll.split('d')[0] == '' or \
                    thisroll.split('d')[0] == '1':
                    
                    rollsides = thisroll.split('d')[1]
                    systemRandom = random.SystemRandom()
                    secureNum1 = systemRandom.randint(1, int(rollsides))
                    answerstring = '(' + str(secureNum1) + ')'
                    rolltotal = secureNum1

                elif thisroll.split('d')[0] == '0':
                    answerstring = '(0)'
                    rolltotal = 0

                elif thisroll.split('d')[0].isdigit():
                    rollamount = thisroll.split('d')[0]
                    rollsides = thisroll.split('d')[1]
                    systemRandom = random.SystemRandom()
                    secureNum1 = systemRandom.randint(1, int(rollsides))
                    rolltotal = secureNum1
                    answerstring = '(' + str(secureNum1)
                    rollamount = int(rollamount) - 1
                    while int(rollamount) > 1:
                        systemRandom = random.SystemRandom()
                        secureNum1 = systemRandom.randint(1, int(rollsides))
                        answerstring = answerstring + '+' + str(secureNum1)
                        rollamount = int(rollamount) - 1
                        rolltotal = rolltotal + secureNum1
                    systemRandom = random.SystemRandom()
                    secureNum1 = systemRandom.randint(1, int(rollsides))
                    rolltotal = rolltotal + secureNum1
                    answerstring = answerstring + '+' + str(secureNum1) + ')'
                
                return answerstring,rolltotal

            if '{0.content}'.format(message).lower() == self.settings.ninjabotdice or '{0.content}'.format(message).lower() == dice:
                await message.channel.send(embed=helpembed)

            
            elif '{0.content}'.format(message).lower().split(' ')[0] == dice:
                
                rollcommand = '{0.content}'.format(message).lower().replace('ninjabot dice ','').replace(dice + ' ','')
                
                diffrolls = ''
                
                diffrolls = rollcommand.split(' ')

                if len(diffrolls) > 10:
                    picture = nextcord.File('data/images/toohigh.jpg', filename="image.jpg")
                    await message.channel.send(file=picture)
                
                elif len(diffrolls) <= 10:
                
                    for singleroll in diffrolls:
                        rolllist = re.split('(\+|-|\*|/)',singleroll)

                        total = 0
                        lastoperator = ''
                        fullstring = ''
                        

                        for idx, item in enumerate(rolllist):
                            
                            if 'd' in item:                        
                                
                                if int(item.split('d')[0]) > 100:
                                    raise Exception("They rolled too many dice.")
                                
                                results = rollme(item)

                                if lastoperator != '':
                                    if lastoperator == '/':
                                        total = total / results[1]

                                        fullstring = fullstring + ' / ' + results[0]

                                    elif lastoperator == '*':
                                        total = total * results[1]

                                        fullstring = fullstring + ' * ' + results[0]

                                    elif lastoperator == '-':
                                        total = total - results[1]

                                        fullstring = fullstring + ' - ' + results[0]

                                    elif lastoperator == '+':
                                        total = total + results[1]
                                        
                                        fullstring = fullstring + ' + ' + results[0]

                                elif lastoperator == '':

                                    results = rollme(item)
                                    total = total + results[1]
                                    fullstring = results[0]



                            elif item in equations:

                                lastoperator = item



                            elif item.isdigit() and lastoperator in equations:


                                if lastoperator == '/':
                                    total = total / int(item)

                                    fullstring = fullstring + ' / ' + item

                                elif lastoperator == '*':
                                    total = total * int(item)

                                    fullstring = fullstring + ' * ' + item

                                elif lastoperator == '-':
                                    total = total - int(item)

                                    fullstring = fullstring + ' - ' + item

                                elif lastoperator == '+':
                                    total = total + int(item)
                                    
                                    fullstring = fullstring + ' + ' + item

                        fullstring = fullstring + ' = {}'.format(str(total))
                        
                        await message.channel.send('<@{}> rolled `{}`: {}'.format(message.author.id,singleroll,fullstring))

        except:
            await message.channel.send('Sorry <@{}>, something went horribly wrong with that roll! Did you throw too many dice at once?\r\nType `{}dice` if you are stuck.'.format(message.author.id,prefix))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))