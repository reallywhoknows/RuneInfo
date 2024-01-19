import requests
import discord
from discord.commands import slash_command
from discord.ext import commands

class commands(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    #Used to restrict to specific role
    #@commands.has_role("Admin")

    @slash_command(guild_ids=[1087515364017066135],name='ping',description='return bot latency')
    async def price(self,ctx: discord.ApplicationContext,arg):
        #Add headers, or osrs api will complain. Ref github repo for contact information.
        headers = {
            "User-Agent": "RuneInfo",
            "From": "https://github.com/reallywhoknows/RuneInfo"
        }

        #GET api request, convert into JSON data for usage
        with requests.Session() as session:
            request = session.get("https://prices.runescape.wiki/api/v1/osrs/mapping",headers=headers)
        json_data = request.json()

        for i in json_data:
            if i["name"].lower() == arg.lower():
                item_id = i["id"]
                item_name = i["name"]
                item_examine = i["examine"]

        print(f"{item_id},{item_name},{item_examine}")

def setup(client):
    client.add_cog(commands(client))