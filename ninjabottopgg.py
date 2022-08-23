import dbl
import nextcord
from nextcord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, ninjabot):
        self.bot = ninjabot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc1NTUwNDI0MzMyMjEyNjQyNiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA0ODY2NDI0fQ.5je6lRvVapb8wyKu_n7KczrDeO_DJyHmp-zqraPk6SA' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))