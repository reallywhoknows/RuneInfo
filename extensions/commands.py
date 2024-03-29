import requests
import json
import discord
from discord.commands import slash_command
from discord.ext import commands
from datetime import date

headers = {
        "User-Agent": "RuneInfo",
        "From": "https://github.com/reallywhoknows/RuneInfo"
    }

class commands(commands.Cog):
    def __init__(self,client):
        self.client = client
#guild_ids=[1087515364017066135]
    @slash_command(name='lookup',description='Check the stats of any OSRS user!')
    async def lookup(self,ctx: discord.ApplicationContext,rsn):

        with requests.Session() as session:
            request = session.get(f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={rsn.replace(' ', '%20')}",headers=headers)
            #Catch if RSN returns 404 (Invalid username)
            if request.status_code == 404:
                #Build the error message with styling for more pleasant presentation
                embed = discord.Embed(
                    title = "Error! User could not be found!",
                    description = f"Please check if `{rsn}` is a valid username otherwise please report the issue.\nhttps://github.com/reallywhoknows/RuneInfo/issues",
                    color = discord.Colour.brand_red(),
                    )
                file = discord.File("./assets/warning.png")
                embed.set_thumbnail(url="attachment://warning.png")
                embed.set_footer(text=date.today().strftime("%B %d, %Y"))

                await ctx.respond(embed=embed, file=file)
                return
            
        json_data = request.json()


        #Creating a dict and adding the values from json_data skills into it for use later
        stats = {}
        for i in json_data['skills']:
            stats[i['name']] = i['level']
        
        #Unfortunately due to limitations, this is going to get a bit ugly. We will need to reference a custom emoji to include the icon in an embed.
        #File uploads are restricted 10 per message & URLs don't embed the icon and instead show as hyperlink.
        #If there is a better way to do this please let me know.

        with open("./assets/resource.json") as content:
            icons = json.load(content)

        embed = discord.Embed(
            title = f"**{rsn}**",
            description = f"",
            color = discord.Colour.brand_red(),
            )
        embed.add_field(name="", value=f"{icons['attack']} {stats['Attack']}\n{icons['strength']} {stats['Strength']}\n{icons['defence']} {stats['Defence']}\n{icons['ranged']} {stats['Ranged']}\n{icons['prayer']} {stats['Prayer']}\n{icons['runecraft']} {stats['Runecraft']}\n{icons['magic']} {stats['Magic']}\n{icons['construction']} {stats['Construction']}", inline=True)
        embed.add_field(name="", value=f"{icons['hitpoints']} {stats['Hitpoints']}\n{icons['agility']} {stats['Agility']}\n{icons['herblore']} {stats['Herblore']}\n{icons['thieving']} {stats['Thieving']}\n{icons['crafting']} {stats['Crafting']}\n{icons['fletching']} {stats['Fletching']}\n{icons['slayer']} {stats['Slayer']}\n{icons['hunter']} {stats['Hunter']}", inline=True)
        embed.add_field(name="", value=f"{icons['mining']} {stats['Mining']}\n{icons['smithing']} {stats['Smithing']}\n{icons['fishing']} {stats['Fishing']}\n{icons['cooking']} {stats['Cooking']}\n{icons['firemaking']} {stats['Firemaking']}\n{icons['woodcutting']} {stats['Woodcutting']}\n{icons['farming']} {stats['Farming']}\n{icons['overall']} {stats['Overall']}", inline=True)
        embed.set_footer(text=date.today().strftime("%B %d, %Y"))

        await ctx.respond(embed=embed)

    @slash_command(name='price',description='Get the latest buy/sell information for the item of your choice.')
    async def price(self,ctx: discord.ApplicationContext,item):
        #Add headers, or osrs api will complain. Ref github repo for contact information.

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
                break
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