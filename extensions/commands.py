import requests
import discord
from discord.commands import slash_command
from discord.ext import commands
from datetime import date

class commands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @slash_command(guild_ids=[1087515364017066135],name='price',description='Get the latest buy/sell information for the item of your choice.')
    async def price(self,ctx: discord.ApplicationContext,item):
        #Add headers, or osrs api will complain. Ref github repo for contact information.
        headers = {
            "User-Agent": "RuneInfo",
            "From": "https://github.com/reallywhoknows/RuneInfo"
        }

        #GET api request, convert into JSON data for usage.
        with requests.Session() as session:
            request = session.get("https://prices.runescape.wiki/api/v1/osrs/mapping",headers=headers)
        json_data = request.json()

        #Check if request is numbers or text. In order to alowing passing through raw ID
        if item.isnumeric():
            item = int(item)
            key = "id"
        else:
            item = item.lower()
            item = item.capitalize()
            key = "name"

        for i in json_data:
            if i[key] == item:
                #Convert json data into usable variables. id, name examine and icon. id is required for pathing to GE information. 
                item_id = i["id"]
                item_name = i["name"]
                item_examine = i["examine"]
            else:
                #Build the error message with styling for more pleasant presentation
                embed = discord.Embed(
                    title = "Error! Item not found!",
                    description = f"Please check if `{item}` is a valid item name or id otherwise please report the issue.\nhttps://github.com/reallywhoknows/RuneInfo/issues",
                    color = discord.Colour.brand_red(),
                    )
                file = discord.File("./assets/warning.png")
                embed.set_thumbnail(url="attachment://warning.png")
                embed.set_footer(text=date.today().strftime("%B %d, %Y"))

                await ctx.respond(embed=embed, file=file)
                return

        #Some URLs do not like passing integers in the url.
        item_id = str(item_id)

        #GET api request, converting JSON data for usage.
        with requests.Session() as session:
            request = session.get(f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}",headers=headers)
        json_data = request.json()

        item_high = json_data["data"][item_id]["high"]
        item_low = json_data["data"][item_id]["low"]

        #Grabs icon from runelite, which logically uses item id to reference image.
        item_icon = f"https://static.runelite.net/cache/item/icon/{item_id}.png"

        #Build the message with styling for more pleasant presentation
        embed = discord.Embed(
            title = item_name,
            description = f"*{item_examine}*",
            color = discord.Colour.brand_red(),
        )
        embed.add_field(name="",value=f"Buy now price: {item_high:,}\nSell now price: {item_low:,}")
        embed.set_thumbnail(url = item_icon)
        embed.set_footer(text=date.today().strftime("%B %d, %Y"))

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(commands(client))