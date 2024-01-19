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
    @commands.has_role("Admin")
    async def list_cog(self,ctx):
        list = []
        for filename in os.listdir(f"./{self.directory}"):
            if filename.endswith(".py"):
                list.append(filename[:-3])
        
        list = "\n".join(list)
        await ctx.send(f"**Cogs Available:**\n{list}")

    #Reload Cog
    @commands.command()
    @commands.has_role("Admin")
    async def reload_cog(self,ctx,arg):
        #Initiate Unloading
        self.client.unload_extension(f"{self.directory}.{arg}")
        reload_msg = await ctx.message.channel.send(f"Reloading... {arg}")
        
        await asyncio.sleep(5)

        #Initiate Loading
        self.client.load_extension(f"{self.directory}.{arg}")
        await reload_msg.delete()
        await ctx.message.channel.send("Reload complete")

    #Load Cog
    @commands.command()
    @commands.has_role("Admin")
    async def load_cog(self,ctx,arg):
        self.client.load_extension(f"{self.directory}.{arg}")
        await ctx.message.channel.send(f"Loaded: {arg}")

    #Unload Cog
    @commands.command()
    @commands.has_role("Admin")
    async def unload_cog(self,ctx,arg):
        self.client.unload_extension(f"{self.directory}.{arg}")
        await ctx.message.channel.send(f"Unloaded: {arg}")

def setup(client):
    client.add_cog(extension_controller(client))