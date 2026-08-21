import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required to scan the server members for the dropdown

class FishBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        # Set to store IDs of users allowed to use /fish
        self.allowed_users = set()

    async def setup_hook(self):
        # Syncs the slash commands with Discord instantly
        await self.tree.sync()

bot = FishBot()

# Your Supreme Server Owner ID
OWNER_ID = 1429893158740820056

# Dropdown selection menu for giving access
class MemberSelect(discord.ui.Select):
    def __init__(self, bot_instance, members):
        self.bot_instance = bot_instance
        # Generate menu options using real members from the server
        options = [
            discord.SelectOption(label=m.name, value=str(m.id), description=f"ID: {m.id}")
            for m in members if not m.bot or m.id != bot_instance.user.id
        ][:25]  # Discord limit: max 25 items per dropdown
        super().__init__(placeholder="Choose a user to grant access... 🐟", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Only you (the Owner) can interact with this menu
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ You are not Zacky to distribute fishes!", ephemeral=True)
            return
        
        user_id = int(self.values[0])
        self.bot_instance.allowed_users.add(user_id)
        
        await interaction.response.send_message(f"✅ User <@{user_id}> now has permission to fish!", ephemeral=True)

class MemberSelectView(discord.ui.View):
    def __init__(self, bot_instance, members):
        super().__init__()
        self.add_item(MemberSelect(bot_instance, members))

@bot.event
async def on_ready():
    print(f"The squad is up! {bot.user.name} is ready to grant fishes! 🐟")

# Admin Access Command
@bot.tree.command(name="access", description="Grant a user access to the /fish command (Owner Only)")
async def access(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Only the bot owner can access this command.", ephemeral=True)
        return

    # Fetch all members currently in the server
    members = interaction.guild.members
    view = MemberSelectView(bot, members)
    await interaction.response.send_message("⚙️ **Fish Control Panel:** Choose who gets access below:", view=view, ephemeral=True)

# Fish Command
@bot.tree.command(name="fish", description="Receive a fish if you have permission")
async def fish(interaction: discord.Interaction):
    # Owner always has access, others must be in the allowed_users set
    if interaction.user.id == OWNER_ID or interaction.user.id in bot.allowed_users:
        await interaction.response.send_message("𝘗𝘦𝘴𝘵𝘦 🐟")
    else:
        await interaction.response.send_message("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭𝘺 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘢𝘯𝘥.", ephemeral=True)

bot.run(os.environ.get("DISCORD_TOKEN"))
