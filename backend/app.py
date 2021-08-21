from utils import return_token_or_raise, filter_guilds
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage,Unauthorized
from sanic_cors import CORS
from json import loads


import constants
import hikari
import aiohttp

try:
    import uvloop

    uvloop.install()
except:
    pass

app = Sanic("My Hello, world app")
app.config.FALLBACK_ERROR_FORMAT = "json"

CORS(app)
rest_client = hikari.RESTApp()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/oauth/callback", methods=['POST'])
async def callback(request):
    code = request.json.get("code")

    if not code:
        raise InvalidUsage("Invalid request")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": constants.CLIENT_ID,
                "client_secret": constants.CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": constants.REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ) as resp:
            data = await resp.json()
    print(data)
    return json({'access_token':data.get('access_token')})

@app.route('/users/me')
async def get_own_user(request):
    token= await return_token_or_raise(request)
    
    try:
        async with rest_client.acquire(token) as client:
            user = await client.fetch_my_user()
    except hikari.errors.UnauthorizedError:
        raise Unauthorized("Invalid access token")
    
    return json({
        'id': str(user.id),
        'username': user.username,
        'discriminator': user.discriminator,
        'avatar_url': f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar_hash}.png?size=256'
    })

@app.route('/guilds')
async def get_mutual_guilds(request):
    token= await return_token_or_raise(request)

    try:
        async with rest_client.acquire(token) as client:
            user_guilds = await client.fetch_my_guilds()
    except hikari.errors.UnauthorizedError:
        raise Unauthorized("Invalid access token")

    valid_guilds = await filter_guilds(user_guilds)
    guild_ids = [str(x.id) for x in valid_guilds]

    async with aiohttp.ClientSession() as session:
        response = await session.post("http://localhost:6969/guilds", json={"guilds": guild_ids})
        guilds = await response.text()
    
    return json(loads(guilds))

if __name__ == "__main__":
    app.run(debug=True)
