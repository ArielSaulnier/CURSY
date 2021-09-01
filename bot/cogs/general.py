from models import GuildConfig
import json
import os
import platform
import random
import sys
import numpy as np
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        print(f"Loaded {self.__class__.__name__} Cog")

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get some information about the bot.
        """
        config = await GuildConfig.filter(id=context.guild.id).get_or_none()
        usercount = [x.member_count for x in self.bot.guilds]
        usercount = np.sum(usercount)
        embed = discord.Embed(
            description="Bot Cursy",
            color=0x42F56C
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="<@284846671773302784>",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config.prefix}",
            inline=False
        )
        embed.add_field(
            name="Servers",
            value=f"{len(self.bot.guilds)}"
        )
        embed.add_field(
            name="Users",
            value=f"{usercount}"
        )
        embed.add_field(
            name="Ping",
            value=f"{round(self.bot.latency * 1000)} ms"
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(
            text=f"Requested by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Get some useful (or not) information about the server.
        """
        server = context.message.guild
        roles=[]
        for x in server.roles:
            roles.append(f"**{x.name}**")
        role_length = len(roles)
        
        
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"<@{server.owner.id}>"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, context, *, title):
        """
        Create a poll where members can vote.
        """
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="doge")
    async def dogecoin(self, context):
        """
        Get the current price of dogecoin.
        """
        url = "https://sochain.com//api/v2/get_price/DOGE/USD"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title="DOGE",
                description=f"**Dogecoin price is: ${response['data']['prices'][0]['price']} USD**",
                color=0x42F56C
            )
            embed.set_footer(
            text=f"Fetched at: {datetime.fromtimestamp(response['data']['prices'][0]['time']).strftime('%H:%M:%S')}"
        )
            embed.set_thumbnail(url="https://dogecoin.com/assets/img/dogecoin-300.png")
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))