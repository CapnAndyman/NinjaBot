import nextcord
import sys

class Ninjabotfunctions:
    
    async def ninjabotembed(self,channel,data,image = 'none',color = 'none',author = 'none'):

        try:
            embed = ''

            firstline = data.pop(0)

            if color == 'none':
                embed=nextcord.Embed(title=firstline[0], description=firstline[1])
            else:
                embed=nextcord.Embed(title=firstline[0], description=firstline[1], color=color)
            
            if author != 'none':
                embed.set_author(name=author[0], icon_url=author[1])

            for item in data:      
                embed.add_field(name=item[0], value=item[1], inline=item[2])

            if image != 'none':
                embed.set_image(url=image)

            await channel.send(embed=embed)
        except:
            await self.startupchannel.send('Ninjabot embed failed. @here\r\n{}\r\n{}\r\n{}'.format(str(sys.exc_info()[0]),str(sys.exc_info()[1]),str(sys.exc_info()[2])))