import nextcord
from nextcord.ext import commands
import requests
import json
import datetime

bot = commands.Bot()

url_kick = "https://apis.roblox.com/messaging-service/v1/universes/universeidhere/topics/ServerKick"

headers = {
    'x-api-key': 'apikeywithpermission',
    'Content-Type': 'application/json'
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command()
async def kick(interaction: nextcord.Interaction, username: str, reason: str):
    ObjectToSend = {'Username': username, 'Reason': reason}
    try:
        response = requests.post(url_kick, json={'message': json.dumps(ObjectToSend)}, headers=headers)
        if response.status_code == 200:
            embed = nextcord.Embed(description=f"Success: Kicked {username} for {reason}", color=0x00bfff)
        else:
            embed = nextcord.Embed(description="Error: Failed to kick user", color=0xff0000)
    except requests.exceptions.RequestException as err:
        embed = nextcord.Embed(description=f"Error: {err}", color=0xff0000)
    await interaction.response.send_message(embed=embed)
    

bot.run('botokenhere')
