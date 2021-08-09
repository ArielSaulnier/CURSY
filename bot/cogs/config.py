from discord.ext import commands
from models import GuildConfig, WelcomeConfig, LeaveConfig
import discord
import typing
import constants


class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f"Loaded {self.__class__.__name__} Cog")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx: commands.Context, _prefix: typing.Optional[str] = None):
        config = await GuildConfig.filter(id=ctx.guild.id).get_or_none()
        if not _prefix:
            return await ctx.send(
                f"Current prefix for this server is **{config.prefix if config else constants.DEFAULT_PREFIX}**"
            )
        if not config:
            new_config = GuildConfig(id=ctx.guild.id, prefix=_prefix)
            await new_config.save()
        else:
            config.prefix = _prefix
            await config.save()

        return await ctx.send(f"Set the prefix for this server to **{_prefix}**")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def welcome(self, ctx: commands.context):
        config = await GuildConfig.filter(id=ctx.guild.id).get_or_none()
        welcome_config = await WelcomeConfig.filter(id=ctx.guild.id).get_or_none()

        if config.welcome_enabled:
            welcome_channel = discord.utils.get(
                ctx.guild.channels, id=welcome_config.channel_id
            )
            return await ctx.send(
                f"Welcome messages are enabled in this guild. All member_join events will be sent to {welcome_channel.mention}"
            )
        else:
            await ctx.send(f"Welcome messages are not enabled in this guild.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def leave(self, ctx: commands.context):
        config = await GuildConfig.filter(id=ctx.guild.id).get_or_none()
        leave_config = await LeaveConfig.filter(id=ctx.guild.id).get_or_none()

        if config.leave_enabled:
            leave_channel = discord.utils.get(
                ctx.guild.channels, id=leave_config.channel_id
            )
            return await ctx.send(
                f"Leaving messages are enabled in this guild. All member_leave events will be sent to {leave_channel.mention}"
            )
        else:
            await ctx.send(f"Leaving messages are not enabled in this guild.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welcome(self, ctx: commands.context):
        async def ask_welcome_message():
            try:
                msg: discord.Message = await self.bot.wait_for(
                    "message", check=lambda x: x.author.id == ctx.author.id
                )
                return await commands.TextChannelConverter().convert(ctx, msg.content)
            except commands.errors.ChannelNotFound as e:
                await ctx.send(
                    f"Invalid channel `{e.argument}`. Please enter a channel name again"
                )
                return await ask_welcome_message()

        await ctx.send(
            "Please enter the channel were all the welcome messages will be sent."
        )
        channel = await ask_welcome_message()

        await ctx.send(
            "Please enter your welcome message. Use `{}` where you want to mention the user"
        )
        welcome_msg = (
            await self.bot.wait_for(
                "message", check=lambda x: x.author.id == ctx.author.id, timeout=20
            )
        ).content

        config = await GuildConfig.filter(id=ctx.guild.id).get_or_none()
        welcome_config = await WelcomeConfig.filter(id=ctx.guild.id).get_or_none()

        config.welcome_enabled = True
        await config.save()

        if not welcome_config:
            new_welcome_config = WelcomeConfig(
                id=ctx.guild.id, channel_id=channel.id, message=welcome_msg
            )
            await new_welcome_config.save()
            return await ctx.send(
                f"Enabled welcomme messages. All member_join events will be sent to {channel.mention}."
            )
        else:
            welcome_config.channel_id = channel.id
            welcome_config.message = welcome_msg
            await welcome_config.save()
        return await ctx.send(
            f"Updates welcomme messages config. All member_join events will be sent to {channel.mention}."
        )

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def set_leave(self, ctx: commands.context):
        async def ask_leave_message():
            try:
                msg: discord.Message = await self.bot.wait_for(
                    "message", check=lambda x: x.author.id == ctx.author.id
                )
                return await commands.TextChannelConverter().convert(ctx, msg.content)
            except commands.errors.ChannelNotFound as e:
                await ctx.send(
                    f"Invalid channel `{e.argument}`. Please enter a channel name again"
                )
                return await ask_leave_message()

        await ctx.send(
            "Please enter the channel were all the leaving messages will be sent."
        )
        channel = await ask_leave_message()

        await ctx.send(
            "Please enter your leaving message. Use `{}` where you want to mention the user"
        )
        leaving_msg = (
            await self.bot.wait_for(
                "message", check=lambda x: x.author.id == ctx.author.id, timeout=20
            )
        ).content

        config = await GuildConfig.filter(id=ctx.guild.id).get_or_none()
        leave_config = await LeaveConfig.filter(id=ctx.guild.id).get_or_none()

        config.leave_enabled = True
        await config.save()

        if not leave_config:
            new_leave_config = LeaveConfig(
                id=ctx.guild.id, channel_id=channel.id, message=leaving_msg
            )
            await new_leave_config.save()
            return await ctx.send(
                f"Enabled welcomme messages. All member_join events will be sent to {channel.mention}."
            )
        else:
            leave_config.channel_id = channel.id
            leave_config.message = leaving_msg
            await leave_config.save()
        return await ctx.send(
            f"Updates welcomme messages config. All member_join events will be sent to {channel.mention}."
        )


def setup(bot: commands.Bot):
    bot.add_cog(Config(bot))
