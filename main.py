import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Obligatoriu ca să vadă lista de oameni din server

class FishBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        # Lista în care salvăm ID-urile celor care primesc acces
        self.allowed_users = set()

    async def setup_hook(self):
        # Sincronizăm comenzile de tip Slash (/) cu Discord
        await self.tree.sync()

bot = FishBot()

# ID-ul tău suprem de Owner
OWNER_ID = 1429893158740820056

# Interfața cu meniul Dropdown pentru selectarea membrilor
class MemberSelect(discord.ui.Select):
    def __init__(self, bot_instance, members):
        self.bot_instance = bot_instance
        # Generăm opțiunile din listă cu membrii reali din server
        options = [
            discord.SelectOption(label=m.name, value=str(m.id), description=f"ID: {m.id}")
            for m in members if not m.bot or m.id != bot_instance.user.id
        ][:25] # Limitare Discord de max 25 oameni în listă
        super().__init__(placeholder="Alege persoana care primește acces... 🐟", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Doar tu ai voie să interacționezi cu meniul
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Nu ești Zacky ca să împarți pești!", ephemeral=True)
            return
        
        user_id = int(self.values[0])
        self.bot_instance.allowed_users.add(user_id)
        
        await interaction.response.send_message(f"✅ Utilizatorul <@{user_id}> are acum permisiunea să pescuiască!", ephemeral=True)

class MemberSelectView(discord.ui.View):
    def __init__(self, bot_instance, members):
        super().__init__()
        self.add_item(MemberSelect(bot_instance, members))

@bot.event
async def on_ready():
    print(f"S-a aprins brigada! {bot.user.name} e gata să împartă pești! 🐟")

# Comanda Supremă de dat acces
@bot.tree.command(name="access", description="Oferă cuiva acces la comanda /fish (Doar pentru Owner)")
async def access(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Doar Server Owner-ul poate folosi această comandă!", ephemeral=True)
        return

    # Luăm lista de oameni din server
    members = interaction.guild.members
    view = MemberSelectView(bot, members)
    await interaction.response.send_message("⚙️ **Panou Control Pești:** Alege cine primește drepturi:", view=view, ephemeral=True)

# Comanda de Pescuit
@bot.tree.command(name="fish", description="Primește un pește dacă ai permisiune")
async def fish(interaction: discord.Interaction):
    # Verificăm dacă ești tu (Ownerul are mereu acces) SAU dacă ești în lista de acces
    if interaction.user.id == OWNER_ID or interaction.user.id in bot.allowed_users:
        await interaction.response.send_message("𝘗𝘦𝘴𝘵𝘦 🐟")
    else:
        await interaction.response.send_message("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭𝘺 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘢𝘯𝘥.", ephemeral=True)

bot.run(os.environ.get("DISCORD_TOKEN"))
