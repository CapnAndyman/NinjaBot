import nextcord

class Ninjabotdictionary:
    async def ninjabotdictionary(self,ninjabot,message,prefix):

        try:

            self.settings = ninjabot.settings
            userinput = '{0.content}'.format(message).lower()
            

            if userinput == prefix + 'define':

                await message.channel.send('Type `{0}define` followed by your word. Example: `{0}define discord`'.format(prefix))  

            elif len(userinput.split(' ')[0]) >= 2 and userinput.split(' ')[0] == prefix + 'define':
            
                word = userinput.replace(prefix + 'define ','')

                result = ninjabot.ninjabotsql.sql_dictionaryselect(self.settings.dictget,(word,))

                if result:
                    
                    embed=nextcord.Embed(title="NinjaBot Dictionary", description='Here is the definition(s) for `{}`'.format(word), color=nextcord.Color.green())
                    data = ''
                    typelist = []
                    datawithtypes = []
                    currentline = 1
                    typenumber = 0
                    for item in result:                    

                        if item[1]:                    
                        
                            if item[1] not in typelist:
                                typelist.append(item[1])
                                
                                datawithtypes.append((typenumber,item[2]))

                                typenumber = typenumber + 1

                            else:
                                thistype = typelist.index(item[1])
                                datawithtypes.append((thistype,item[2]))
                        
                        else:

                            data = data + '`{}.` {}\r\n'.format(str(currentline),item[2])
                            currentline = currentline + 1                        

                    if typelist != []:
                        for idx,item in enumerate(typelist):
                            embeddata = ''
                            typedataline = 1
                            for singleresult in datawithtypes:
                                
                                if singleresult[0] == idx:
                                    embeddata = embeddata + '`{}.` {}\r\n'.format(str(typedataline),singleresult[1])
                                    typedataline = typedataline + 1
                            embed.add_field(name='`{}`'.format(item), value=embeddata, inline=False) 
                    
                    if data != '':
                        embed.add_field(name='Other', value=data, inline=False)

                    await message.channel.send(embed=embed)
            
                else:
                    original = ' '.join('{0.content}'.format(message).split(' ')[1:])
                    await message.channel.send('Sorry <@{0.author.id}>, I do not have a definition for `'.format(message) + original + '`.')                    

        except:
            original = ' '.join('{0.content}'.format(message).split(' ')[1:])
            await message.channel.send('Sorry <@{0.author.id}>, I do not have a definition for `'.format(message) + original + '`.')
                

