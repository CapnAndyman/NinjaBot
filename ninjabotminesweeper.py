from PIL import Image, ImageDraw, ImageFont
import nextcord
import string
import random
import io
import sys, os

class Ninjabotminesweeper:
    async def ninjabotminesweeper(self,ninjabot,message,gamemode,prefix):
        
        try:
        
            self.settings = ninjabot.settings

            mscore = prefix + 'mscore'
            ml = prefix + 'minesweeper'
            ms = prefix + 'mine'
            gamestop = prefix + 'stop'

            minehelpembed=nextcord.Embed(title='NinjaBot Minesweeper', description="More Information")
            minehelpembed.add_field(name="Playing", value='Once you type `{0}mine` the game will begin. Answer by using `{0}` followed by your answer. Example: `{0}c11` if you think c11 is safe.'.format(prefix), inline=False)
            minehelpembed.add_field(name="Scoring", value='Type `{}mscore` to see your score. You recieve one point per successful game.'.format(prefix), inline=False)

            userchannel = '{0.channel.id}'.format(message)
            userid = '{0.author.id}'.format(message)
            userinput = '{0.content}'.format(message).lower()
            useranswer = userinput.replace(prefix + ' ','').replace(prefix,'')   
            freeanswer = ''

            if not userinput.startswith(prefix):
                freeanswer = 1

            gamefile = ''

            answerblockid = ''

            self.nonsafes = ['boom','unboom','0','mine','blank','1o','2o','3o','4o','5o','6o','7o','8o']

            self.safes = ['blank','1o','2o','3o','4o','5o','6o','7o','8o']

            self.numbers = ['0','1','2','3','4','5','6','7','8']

            self.img = ''
            self.d = ''

            self.game = []

            def initrender():
                #Start Initial Image Render
                self.img = Image.new('RGB', (500, 500), color = (0, 0, 0))
                self.d = ImageDraw.Draw(self.img)
                fnt = ImageFont.truetype('fonts/American Captain.ttf', 17)
                #Draw lines
                for num in range(1, 17):           
                    currentline = 1           
                    for letter in range(65, 81):
                        currentitem = chr(letter) + str(num)               
                        if num < 10:                   
                            self.d.rectangle([(31*(num-1)) + 2,(31*(currentline-1)) + 2, (31*(num-1)) + 32,(31*(currentline-1)) + 32], fill=(0,0,0), outline="white")                   
                        else:                    
                            self.d.rectangle([(31*(num-1)) + 2,(31*(currentline-1)) + 2, (31*(num-1)) + 32,(31*(currentline-1)) + 32], fill=(0,0,0), outline="white")                      
                        currentline = currentline + 1
                #Draw Letters
                for num in range(1, 17):         
                    currentline = 1          
                    for letter in range(65, 81):
                        currentitem = chr(letter) + str(num)              
                        if num < 10 and letter != 73:              
                            self.d.text((((31 * (currentline-1)) + 10),((31 * (num-1))) + 10), currentitem, font=fnt, fill=(255,255,255))        
                        elif num < 10 and letter == 73:        
                            self.d.text((((31 * (currentline-1)) + 12),((31 * (num-1))) + 10), currentitem, font=fnt, fill=(255,255,255))
                        elif letter == 73:       
                            self.d.text((((31 * (currentline-1)) + 11),((31 * (num-1))) + 10), currentitem, font=fnt, fill=(255,255,255))
                        else:        
                            self.d.text((((31 * (currentline-1)) + 8),((31 * (num-1))) + 10), currentitem, font=fnt, fill=(255,255,255))            
                        currentline = currentline + 1

            #Function to unveil blanks if they exist
            def unveilblanks(block):
                if self.game[block] not in self.nonsafes:
                    self.game[block] = str(self.game[block]) + 'o'           
                elif self.game[block] == '0':
                    #Check if first row so as not to check negative rows
                    self.game[block] = 'blank'
                    if block < 16:
                        #Check if not first block, then add to previous block
                        if block != 0:
                            #check left block
                            if self.game[block - 1] == '0':                    
                                unveilblanks(block - 1)
                            if self.game[block - 1] not in self.nonsafes:
                                self.game[block - 1] = str(self.game[block - 1]) + 'o'
                            #check bottem left block
                            if self.game[block + 15] == '0':
                                unveilblanks(block + 15)
                            if self.game[block + 15] not in self.nonsafes:
                                self.game[block + 15] = str(self.game[block + 15]) + 'o'
                        #If last block of first row, do not add bottom right block and right block
                        if block != 15:
                            #check bottem right block
                            if self.game[block + 17] == '0':                   
                                unveilblanks(block + 17)
                            if self.game[block + 17] not in self.nonsafes:
                                self.game[block + 17] = str(self.game[block + 17]) + 'o'
                            #Check next block
                            if self.game[block + 1] == '0':                    
                                unveilblanks(block + 1)
                            if self.game[block + 1] not in self.nonsafes:
                                self.game[block + 1] = str(self.game[block + 1]) + 'o'
                        #check bottem block
                        if self.game[block + 16] == '0':                        
                            unveilblanks(block + 16)
                        if self.game[block + 16] not in self.nonsafes:
                            self.game[block + 16] = str(self.game[block + 16]) + 'o'
                    elif block in range(16,240):
                        #Check if block is not at beginning of row to add top left, bottom left, and left blocks
                        if (block % 16) != 0:
                            #left block
                            if self.game[block - 1] == '0':                            
                                unveilblanks(block - 1)
                            if self.game[block - 1] not in self.nonsafes:
                                self.game[block - 1] = str(self.game[block - 1]) + 'o'
                            #bottom left block
                            if self.game[block + 15] == '0':                            
                                unveilblanks(block + 15)
                            if self.game[block + 15] not in self.nonsafes:
                                self.game[block + 15] = str(self.game[block + 15]) + 'o'
                            #top left block
                            if self.game[block - 17] == '0':                            
                                unveilblanks(block - 17)
                            if self.game[block - 17] not in self.nonsafes:
                                self.game[block - 17] = str(self.game[block - 17]) + 'o'
                        #Check if block is not at the end of the row to add right-side blocks
                        if ((block + 1) % 16) != 0:
                            #right block
                            if self.game[block + 1] == '0':                            
                                unveilblanks(block + 1)
                            if self.game[block + 1] not in self.nonsafes:
                                self.game[block + 1] = str(self.game[block + 1]) + 'o'
                            #bottom right block
                            if self.game[block + 17] == '0':                            
                                unveilblanks(block + 17)
                            if self.game[block + 17] not in self.nonsafes:
                                self.game[block + 17] = str(self.game[block + 17]) + 'o'
                            #top right block
                            if self.game[block - 15] == '0':                            
                                unveilblanks(block - 15)
                            if self.game[block - 15] not in self.nonsafes:
                                self.game[block - 15] = str(self.game[block - 15]) + 'o'
                        #bottom block
                        if self.game[block + 16] == '0':                        
                            unveilblanks(block + 16)
                        if self.game[block + 16] not in self.nonsafes:
                            self.game[block + 16] = str(self.game[block + 16]) + 'o'
                        #top block
                        if self.game[block - 16] == '0':                        
                            unveilblanks(block - 16)
                        if self.game[block - 16] not in self.nonsafes:
                            self.game[block - 16] = str(self.game[block - 16]) + 'o'
                    #Check last row so as not to exceed max blocks
                    elif block > 239:
                        if (block % 16) != 0:
                            #left block
                            if self.game[block - 1] == '0':                            
                                unveilblanks(block - 1)
                            if self.game[block - 1] not in self.nonsafes:
                                self.game[block - 1] = str(self.game[block - 1]) + 'o'
                            #top left block
                            if self.game[block - 17] == '0':                            
                                unveilblanks(block - 17)
                            if self.game[block - 17] not in self.nonsafes:
                                self.game[block - 17] = str(self.game[block - 17]) + 'o'
                        if ((block + 1) % 16) != 0:
                            #right block
                            if self.game[block + 1] == '0':                            
                                unveilblanks(block + 1)
                            if self.game[block + 1] not in self.nonsafes:
                                self.game[block + 1] = str(self.game[block + 1]) + 'o'
                            #top right block
                            if self.game[block - 15] == '0':                            
                                unveilblanks(block - 15)  
                            if self.game[block - 15] not in self.nonsafes:
                                self.game[block - 15] = str(self.game[block - 15]) + 'o'               
                        #top block
                        if self.game[block - 16] == '0':                       
                            unveilblanks(block - 16)
                        if self.game[block - 16] not in self.nonsafes:
                            self.game[block - 16] = str(self.game[block - 16]) + 'o'
                
            
            #Function to draw current board status per gamedata including bombs if they have exploded
            def drawstatus():
                fnt = ImageFont.truetype('fonts/American Captain.ttf', 17)
                for idx, val in enumerate(self.game):
                    row = int(idx / 16) #-1
                    column = (idx % 16) #+1
                    if val == 'blank':
                        shape = [((column * 31) + 2, (row * 31) + 2 ), ((column * 31) + 32, (row * 31) + 32 )] 
                        self.d.rectangle(shape, fill=(200,200,200), outline ="white")
                    elif val in self.safes[1:]:
                        shape = [((column * 31) + 2, (row * 31) + 2 ), ((column * 31) + 32, (row * 31) + 32 )] 
                        self.d.rectangle(shape, fill=(200,200,200), outline ="white")
                        self.d.text(((column * 31) + 14, (row * 31) + 10), val[0], font=fnt, fill=(0,0,0))
                    elif val == 'boom':
                        shape = [((column * 31) + 2, (row * 31) + 2 ), ((column * 31) + 32, (row * 31) + 32 )] 
                        self.d.rectangle(shape, fill=(255,0,0), outline ="white")
                    elif val == 'unboom':
                        shape = [((column * 31) + 2, (row * 31) + 2 ), ((column * 31) + 32, (row * 31) + 32 )] 
                        self.d.rectangle(shape, fill=(255,0,255), outline ="white")
                        
            #Function to generate mines for a fresh game
            def genmines():
                #Generate mines
                self.game = []
                for num in range(0,256):
                    self.game.append(random.choice(('0','0','0','0','0','mine')))

                #Generate self.numbers around mines
                for idx, val in enumerate(self.game):
                    #If mine, add self.numbers around it
                    if val == 'mine':
                        #Check if first row so as not to check negative rows
                        if idx < 16:
                            #Check if not first block, then add to previous block
                            if idx != 0:
                                if self.game[idx - 1] != 'mine':
                                    self.game[idx - 1] = str(int(self.game[idx - 1]) + 1)
                                #check bottem left block
                                if self.game[idx + 15] != 'mine':
                                    self.game[idx + 15] = str(int(self.game[idx + 15]) + 1)
                            #If last block of first row, do not add bottom right block and right block
                            if idx != 15:
                                #check bottem right block
                                if self.game[idx + 17] != 'mine':
                                    self.game[idx + 17] = str(int(self.game[idx + 17]) + 1)
                                #Check next block
                                if self.game[idx + 1] != 'mine':
                                    self.game[idx + 1] = str(int(self.game[idx + 1]) + 1)
                            #check bottem block
                            if self.game[idx + 16] != 'mine':
                                self.game[idx + 16] = str(int(self.game[idx + 16]) + 1)

                        #Check middle blocks
                        elif idx in range(16,240):
                            #Check if block is not at beginning of row to add top left, bottom left, and left blocks
                            if (idx % 16) != 0:
                                #left block
                                if self.game[idx - 1] != 'mine':
                                    self.game[idx - 1] = str(int(self.game[idx - 1]) + 1)
                                #bottom left block
                                if self.game[idx + 15] != 'mine':
                                    self.game[idx + 15] = str(int(self.game[idx + 15]) + 1)
                                #top left block
                                if self.game[idx - 17] != 'mine':
                                    self.game[idx - 17] = str(int(self.game[idx - 17]) + 1)
                            #Check if block is not at the end of the row to add right-side blocks
                            if ((idx + 1) % 16) != 0:
                                #right block
                                if self.game[idx + 1] != 'mine':
                                    self.game[idx + 1] = str(int(self.game[idx + 1]) + 1)
                                #bottom right block
                                if self.game[idx + 17] != 'mine':
                                    self.game[idx + 17] = str(int(self.game[idx + 17]) + 1)
                                #top right block
                                if self.game[idx - 15] != 'mine':
                                    self.game[idx - 15] = str(int(self.game[idx - 15]) + 1)
                            #bottom block
                            if self.game[idx + 16] != 'mine':
                                self.game[idx + 16] = str(int(self.game[idx + 16]) + 1)
                            #top block
                            if self.game[idx - 16] != 'mine':
                                self.game[idx - 16] = str(int(self.game[idx - 16]) + 1)

                        #Check last row so as not to exceed max blocks
                        elif idx > 239:
                            if (idx % 16) != 0:
                                #left block
                                if self.game[idx - 1] != 'mine':
                                    self.game[idx - 1] = str(int(self.game[idx - 1]) + 1)
                                #top left block
                                if self.game[idx - 17] != 'mine':
                                    self.game[idx - 17] = str(int(self.game[idx - 17]) + 1)
                            if ((idx + 1) % 16) != 0:
                                #right block
                                if self.game[idx + 1] != 'mine':
                                    self.game[idx + 1] = str(int(self.game[idx + 1]) + 1)
                                #top right block
                                if self.game[idx - 15] != 'mine':
                                    self.game[idx - 15] = str(int(self.game[idx - 15]) + 1)                    
                            #top block
                            if self.game[idx - 16] != 'mine':
                                self.game[idx - 16] = str(int(self.game[idx - 16]) + 1)
            
            #Function to convert image to something usable by nextcord
            def convertimage(img):
                arr = io.BytesIO()
                img.save(arr, format='PNG')
                arr.seek(0)
                gamefile = nextcord.File(arr, 'mine_image.png')
                return gamefile

            #Function to unveil bomb data upon failure or win
            def unveilbombs():
                for idx, val in enumerate(self.game):
                    if val == 'mine':
                        self.game[idx] = 'unboom' 

            #Check for score command
            if userinput == mscore:
                userscore = ninjabot.ninjabotsql.sql_select(self.settings.minegetscore,(userid,))
                await message.channel.send('<@{0.author.id}> has a Minesweeper score of '.format(message) + str(userscore[0][0]))

            #Check for help command
            elif userinput == self.settings.minesweeper:
                await message.channel.send(embed=minehelpembed)

            elif userinput == ml or userinput == ms:
                initrender()
                genmines()
                drawstatus()
                gamefile = convertimage(self.img)
                ninjabot.ninjabotsql.sql_insert(self.settings.minewritesql,(','.join(self.game),userchannel))
                ninjabot.ninjabotsql.sql_insert(self.settings.minesetcontsql,('none',userchannel))
                
                embed=nextcord.Embed(title="Ninjabot Minesweeper", description='`Here is your game!`'.format(message), color=nextcord.Color.green())            
                embed.set_image(url="attachment://mine_image.png")
                await message.channel.send(file=gamefile, embed=embed)

                if userinput == ml:
                    await message.channel.send('Reminder: you can also type `{}` instead of `{}`.'.format(ms,ml))

            #Stop block
            elif userinput == gamestop and gamemode:
                self.game = ninjabot.ninjabotsql.sql_select(self.settings.minegetsql,(userchannel,))[0][0].split(',')
                ninjabot.ninjabotsql.sql_insert(self.settings.minestopsql,(userchannel,))
                initrender()
                unveilbombs()
                drawstatus()
                gamefile = convertimage(self.img)

                embed=nextcord.Embed(title="Ninjabot Minesweeper", description='`Game has been stopped by {}`'.format(message.author.name), color=nextcord.Color.red())            
                embed.set_image(url="attachment://mine_image.png")
                await message.channel.send(file=gamefile, embed=embed)

            #Answering block
            elif (gamemode and userinput.startswith(prefix)) or freeanswer:
                try:
                    if useranswer[0] in list(string.ascii_lowercase)[0:16] and int(useranswer[1:]) in range(1,17):
                        self.game = ninjabot.ninjabotsql.sql_select(self.settings.minegetsql,(userchannel,))[0][0].split(',')
                        answerblockid = ((ord(useranswer[0]) - 96) + (16 * (int(useranswer[1:])-1))) -1
                        #Check if block has already been opened
                        if not any(item in self.safes for item in self.game):
                            while self.game[answerblockid] == 'mine':
                                genmines()
                                #print('mines regened')

                        if self.game[answerblockid] in self.safes:
                            await message.channel.send('Sorry <@{0.author.id}>, that block has already been opened.'.format(message))
                        #Check if block is a mine
                        elif self.game[answerblockid] == 'mine':
                            ninjabot.ninjabotsql.sql_insert(self.settings.minestopsql,(userchannel,))
                            self.game[answerblockid] = 'boom'
                            initrender()
                            unveilbombs()
                            drawstatus()
                            gamefile = convertimage(self.img)

                            embed=nextcord.Embed(title="Ninjabot Minesweeper", description='`YOU LOSE!`', color=nextcord.Color.red())            
                            embed.set_image(url="attachment://mine_image.png")
                            await message.channel.send(file=gamefile, embed=embed)
                            
                        #Unveil block and continue. Send win condition if no more blocks.
                        else:
                            contributors = ninjabot.ninjabotsql.sql_select(self.settings.minegetcontsql,(userchannel,))[0][0]
                            if contributors == 'none':
                                ninjabot.ninjabotsql.sql_insert(self.settings.minesetcontsql,(userid,userchannel))
                            
                            elif str(userid) not in str(contributors):
                                contributors = str(contributors) + ';' + str(userid)
                                ninjabot.ninjabotsql.sql_insert(self.settings.minesetcontsql,(contributors,userchannel))
                            unveilblanks(answerblockid)
                            initrender()
                            drawstatus()
                            
                            #Check win condition
                            if not any(item in self.numbers for item in self.game):
                                ninjabot.ninjabotsql.sql_insert(self.settings.minestopsql,(userchannel,))
                                unveilbombs()
                                drawstatus()
                                gamefile = convertimage(self.img)
                                for player in contributors.split(';'):
                                    ninjabot.ninjabotsql.sql_insert(self.settings.minesetscore,(player,))

                                embed=nextcord.Embed(title="Ninjabot Minesweeper", description='`YOU WIN!`', color=nextcord.Color.gold())            
                                embed.set_image(url="attachment://mine_image.png")
                                await message.channel.send(file=gamefile, embed=embed)

                            #Just continue
                            else:
                                gamefile = convertimage(self.img)
                                
                                embed=nextcord.Embed(title="Ninjabot Minesweeper", description='`YOU ARE SAFE!`', color=nextcord.Color.green())            
                                embed.set_image(url="attachment://mine_image.png")
                                await message.channel.send(file=gamefile, embed=embed)
                                
                                ninjabot.ninjabotsql.sql_insert(self.settings.minewritesql,(','.join(self.game),userchannel))

                            
                    elif not freeanswer:
                        await message.channel.send('Sorry <@{}>, that block is invalid. Type `{}stop` if you want to stop Minesweeper.'.format(message.author.id,prefix))
                
                except:
                    if not freeanswer:
                        await message.channel.send('Sorry <@{}>, that block is invalid. Type `{}stop` if you want to stop Minesweeper.'.format(message.author.id,prefix))

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            await ninjabot.startupchannel.send('@here\r\n{}\r\n{}\r\n{}\r\n{}'.format(str(exc_type),str(exc_obj),str(fname),str('line {}'.format(exc_tb.tb_lineno))))