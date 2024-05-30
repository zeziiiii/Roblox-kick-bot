import nextcord
from nextcord.ext import commands
import requests
import json

bot = commands.Bot()

url_kick = "https://apis.roblox.com/messaging-service/v1/universes/experianceid/topics/ServerKick"
url_ban = "https://apis.roblox.com/messaging-service/v1/universes/experianceid/topics/ServerBan"
url_unban = "https://apis.roblox.com/messaging-service/v1/universes/experianceid/topics/ServerUnban"

def getuserid(username):
    url = f"https://api.newstargeted.com/roblox/users/v2/user.php?username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        userid = data.get('userId')
        return userid

def hotimage(userid):
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=420x420&format=Png&isCircular=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            imageUrl = data["data"][0]["imageUrl"]
            return imageUrl

headers = {
    'x-api-key': 'robloxapikey',
    'Content-Type': 'application/json'
}

class ConfirmationView(nextcord.ui.View):
    def __init__(self, action, username, userid, reason):
        super().__init__()
        self.value = None
        self.action = action
        self.username = username
        self.userid = userid
        self.reason = reason

    @nextcord.ui.button(label='✅ Confirm', style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.MessageInteraction):
        self.value = True
        try:
            if self.action == "kick":
                ObjectToSend = {'Username': self.username, 'Reason': self.reason}
                response = requests.post(url_kick, json={'message': json.dumps(ObjectToSend)}, headers=headers)
            elif self.action == "ban":
                ObjectToSend = {'Username': self.username, 'Reason': self.reason}
                response = requests.post(url_ban, json={'message': json.dumps(ObjectToSend)}, headers=headers)
            elif self.action == "unban":
                Object = {'Username': self.username}
                response = requests.post(url_unban, json={'message': json.dumps(Object)}, headers=headers)
            
            if response.status_code == 200:
                embed = nextcord.Embed(title=f"✅ Successfully {self.action}ed User", color=0x00FF00)
                embed.add_field(name="Username", value=self.username, inline=False)
                embed.add_field(name="User ID", value=self.userid, inline=False)
                embed.add_field(name="Reason", value=self.reason, inline=False)
                embed.set_thumbnail(url=hotimage(self.userid))
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                await interaction.response.edit_message(content="**Failed to perform action.**", view=None)
        except requests.exceptions.RequestException as err:
            await interaction.response.edit_message(content=f"**Error:** {err}", view=None)

    @nextcord.ui.button(label='❌ Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.MessageInteraction):
        self.value = False
        await interaction.response.edit_message(content="**Action cancelled.**", view=None)

@bot.slash_command()
async def kick(interaction: nextcord.Interaction, username: str, reason: str):
    userid = getuserid(username)
    headshot_url = hotimage(userid)

    confirmation_view = ConfirmationView("kick", username, userid, reason)
    embed = nextcord.Embed(title="❗ Confirmation", description=f"Are you sure you want to **kick**?\n\n**Username:** {username}\n**User ID:** {userid}\n**Reason:** {reason}", color=0xff0000)
    embed.set_thumbnail(url=headshot_url)

    await interaction.response.send_message(embed=embed, view=confirmation_view)

@bot.slash_command()
async def ban(interaction: nextcord.Interaction, username: str, reason: str):
    userid = getuserid(username)
    headshot_url = hotimage(userid)

    confirmation_view = ConfirmationView("ban", username, userid, reason)
    embed = nextcord.Embed(title="❗ Confirmation", description=f"Are you sure you want to **ban**?\n\n**Username:** {username}\n**User ID:** {userid}\n**Reason:** {reason}", color=0xff0000)
    embed.set_thumbnail(url=headshot_url)

    await interaction.response.send_message(embed=embed, view=confirmation_view)

@bot.slash_command()
async def unban(interaction: nextcord.Interaction, username: str):
    userid = getuserid(username)
    head = hotimage(userid)

    confirmation_view = ConfirmationView("unban", username, userid, "")
    embed = nextcord.Embed(title="❗ Confirmation", description=f"Are you sure you want to **unban**?\n\n**Username:** {username}\n**User ID:** {userid}", color=0xff0000)
    embed.set_thumbnail(url=head)

    await interaction.response.send_message(embed=embed, view=confirmation_view)

bot.run('botoken')
