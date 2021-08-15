import aiohttp
from discord.ext import commands
from aiohttp import web

import asyncio
import aiohttp_cors

class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.site = None
        print(f"Loaded {self.__class__.__name__} Cog")
    
    async def get_status(self, request):
        return web.json_response({"guilds":len(self.bot.guilds),"ping":round(self.bot.latency * 1000)})

    async def start_server(self):
        app = web.Application()
        cors = aiohttp_cors.setup(app)

        resource = cors.add(app.router.add_resource('/status'))

        cors.add(resource.add_route('GET', self.get_status),{
            '*': aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers='*',
                allow_headers='*',
            )
        })

        #app.router.add_get('/status', self.get_status)

        runner = web.AppRunner(app)
        await runner.setup()

        self.site = web.TCPSite(runner, '0.0.0.0', 6969)

        await self.bot.wait_until_ready()
        await self.site.start()
        print('Server has been started')

    def __unload(self):
        asyncio.ensure_future(self.site.stop())
        print('Server has been stopped')


def setup(bot: commands.Bot):
    cog = Server(bot)
    bot.add_cog(cog)
    bot.loop.create_task(cog.start_server())