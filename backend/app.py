from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage
from sanic_cors import CORS


import constants
import hikari
import aiohttp

try:
    import uvloop

    uvloop.install()
except:
    pass

app = Sanic("My Hello, world app")
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
    token=request.headers.get('access_token')
    
    if not token:
        raise InvalidUsage("Invalid request")
    
    async with rest_client.acquire(token) as client:
        user = await client.fetch_my_user()
    
    return json({
        'id': str(user.id),
        'username': user.username,
        'discriminator': user.discriminator,
        'avatar_url': f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar_hash}.png?size=256'
    })

if __name__ == "__main__":
    app.run(debug=True)
