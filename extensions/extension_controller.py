import os
import asyncio
import discord
from discord.commands import slash_command
from discord.ext import commands

class extension_controller(commands.Cog):
    def __init__(self,client):
        self.client = client

    #This file **DOES NOT** use /slash_commands
    #This is for privileged users only, and as such does not need a slash command entry.
        
    directory = "extensions"

    #List Cogs
    @commands.command()
    @commands.is_owner()
    async def list_cog(self,ctx):
        list = []
        for filename in os.listdir(f"./{self.directory}"):
            if filename.endswith(".py"):
                list.append(filename[:-3])
        
        list = "\n".join(list)
        cog_list_msg = await ctx.send(f"**Cogs Available:**\n{list}")
        await ctx.message.delete()
        await asyncio.sleep(10)
        await cog_list_msg.delete()
        
    #Reload Cog
    @commands.command()
    @commands.is_owner()
    async def reload_cog(self,ctx,arg):
        #Initiate Unloading
        self.client.unload_extension(f"{self.directory}.{arg}")
        print(f"{ctx.message.author} issued a reload.")
        await ctx.message.delete()
        reload_msg = await ctx.message.channel.send(f"Reloading... {arg}")

        await asyncio.sleep(5)

        #Initiate Loading
        self.client.load_extension(f"{self.directory}.{arg}")
        await reload_msg.delete()

        reload_msg = await ctx.message.channel.send("Reload complete")
        await asyncio.sleep(5)
        await reload_msg.delete()

    #Load Cog
    @commands.command()
    @commands.is_owner()
    async def load_cog(self,ctx,arg):
        self.client.load_extension(f"{self.directory}.{arg}")
        print(f"{ctx.message.author} issued a load. ")
        await ctx.message.delete()
        load_msg = await ctx.message.channel.send(f"Loaded: {arg}")
        await asyncio.sleep(5)
        await load_msg.delete()

    #Unload Cog
    @commands.command()
    @commands.is_owner()
    async def unload_cog(self,ctx,arg):
        self.client.unload_extension(f"{self.directory}.{arg}")
        print(f"{ctx.message.author} issued a Unreload.")
        await ctx.message.delete()
        unload_msg = await ctx.message.channel.send(f"Unloaded: {arg}")
        await asyncio.sleep(5)
        await unload_msg.delete()

def setup(client):
    client.add_cog(extension_controller(client))