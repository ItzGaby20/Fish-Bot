import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOT_OWNER_ID = 1429893158740820056
allowed_users = set()

@bot.event
async def on_ready():
    print(f"The squad is up! {bot.user.name} is running with pop-up panels! 🐟")
    await bot.change_presence(activity=discord.CustomActivity(name="Thinking about fishes 🐟"))

# ==================== FORMULARE POP-UP (MODALS) ====================

class AccessModal(discord.ui.Modal, title="Grant Access Control"):
    user_id_input = discord.ui.TextInput(label="User ID", placeholder="Enter the 18+ digit Discord User ID here...", min_length=15, max_length=25)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            u_id = int(self.user_id_input.value)
            allowed_users.add(u_id)
            await interaction.response.send_message(f"✅ Access GRANTED! User <@{u_id}> can now use `!fish`.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid ID! Please make sure you enter numbers only.", ephemeral=True)

class UnaccessModal(discord.ui.Modal, title="Revoke Access Control"):
    user_id_input = discord.ui.TextInput(label="User ID", placeholder="Enter the 18+ digit Discord User ID here...", min_length=15, max_length=25)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            u_id = int(self.user_id_input.value)
            if u_id in allowed_users:
                allowed_users.remove(u_id)
                await interaction.response.send_message(f"❌ Access REVOKED! User <@{u_id}> can no longer use `!fish`.", ephemeral=True)
            else:
                await interaction.response.send_message("ℹ️ This user didn't have access anyway.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid ID! Please make sure you enter numbers only.", ephemeral=True)

class StatusModal(discord.ui.Modal, title="Change Bot Activity"):
    status_input = discord.ui.TextInput(label="Activity Text", placeholder="What should the bot play? (e.g. coding...)", max_length=100)
    async def on_submit(self, interaction: discord.Interaction):
        text = self.status_input.value
        await bot.change_presence(activity=discord.Game(name=text))
        await interaction.response.send_message(f"⚙️ Activity updated successfully to: **Playing {text}**", ephemeral=True)

class Status2Modal(discord.ui.Modal, title="Change Bot Custom Status Bubble"):
    status2_input = discord.ui.TextInput(label="Custom Status Bubble Text", placeholder="Type your custom bubble text here...", max_length=100)
    async def on_submit(self, interaction: discord.Interaction):
        text = self.status2_input.value
        await bot.change_presence(activity=discord.CustomActivity(name=text))
        await interaction.response.send_message(f"⚙️ Custom Status bubble updated successfully to: **{text}**", ephemeral=True)


# ==================== INTERFEȚE CU BUTOANE (VIEWS) ====================

class PublicCmdBarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fish 🐟", style=discord.ButtonStyle.green)
    async def fish_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == BOT_OWNER_ID or interaction.user.id in allowed_users:
            await interaction.response.send_message("Here is ya fish 🐟", ephemeral=False)
        else:
            await interaction.response.send_message("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭𝘺 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷ε 𝘱ε𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴ε 𝘵𝘩𝘪𝕤 𝘤𝘰𝘮𝘢𝘯𝘥.", ephemeral=True)

    @discord.ui.button(label="Troll Cmd 🫵", style=discord.ButtonStyle.gray)
    async def troll_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Imagine using this command only to realize that it does nothing. 🫵😂", ephemeral=False)


class OwnerCmdBarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Access User ✅", style=discord.ButtonStyle.green)
    async def access_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("❌ Only the bot owner can use this panel!", ephemeral=True)
            return
        await interaction.response.send_modal(AccessModal())

    @discord.ui.button(label="Unaccess User ❌", style=discord.ButtonStyle.danger)
    async def unaccess_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("❌ Only the bot owner can use this panel!", ephemeral=True)
            return
        await interaction.response.send_modal(UnaccessModal())

    @discord.ui.button(label="Check Access List 📋", style=discord.ButtonStyle.primary)
    async def aclist_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("❌ Only the bot owner can use this panel!", ephemeral=True)
            return
        if not allowed_users:
            await interaction.response.send_message("ℹ️ The access list is currently empty.", ephemeral=True)
            return
        list_mentions = [f"• <@{u_id}>" for u_id in allowed_users]
        await interaction.response.send_message("📋 **Users with access to `!fish`:**\n" + "\n".join(list_mentions), ephemeral=True)

    @discord.ui.button(label="Set Activity 🎮", style=discord.ButtonStyle.gray)
    async def status_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("❌ Only the bot owner can use this panel!", ephemeral=True)
            return
        await interaction.response.send_modal(StatusModal())

    @discord.ui.button(label="Set Bubble Status 💭", style=discord.ButtonStyle.gray)
    async def status2_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("❌ Only the bot owner can use this panel!", ephemeral=True)
            return
        await interaction.response.send_modal(Status2Modal())


# ==================== COMEDZI CLASICE PE CHAT ====================

@bot.command(name="cmdbar")
async def cmdbar(ctx):
    # Trimitere panou public
    await ctx.reply("🎛️ **Public Command Bar:** Click a button below to interact:", view=PublicCmdBarView())

@bot.command(name="cmdbar2")
async def cmdbar2(ctx):
    if ctx.author.id != BOT_OWNER_ID:
        await ctx.reply("❌ Only the bot owner can use this command!")
        return
    # Trimitere panou privat (doar tu îl poți butona)
    await ctx.reply("👑 **Bot Owner Control Panel:** Manage the bot securely below:", view=OwnerCmdBarView())

# Păstrăm și variantele vechi text în caz de urgență
@bot.command(name="access")
async def access(ctx, member: discord.Member = None):
    if ctx.author.id != BOT_OWNER_ID: return
    if member: allowed_users.add(member.id); await ctx.reply(f"✅ Access GRANTED to {member.mention}.")

@bot.command(name="unaccess")
async def unaccess(ctx, member: discord.Member = None):
    if ctx.author.id != BOT_OWNER_ID: return
    if member and member.id in allowed_users: allowed_users.remove(member.id); await ctx.reply(f"❌ Access REVOKED from {member.mention}.")

@bot.command(name="fish")
async def fish(ctx):
    if ctx.author.id == BOT_OWNER_ID or ctx.author.id in allowed_users: await ctx.reply("Here is ya fish 🐟")
    else: await ctx.reply("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝒏𝘵𝘭ÿ 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯...")

bot.run(os.environ.get("DISCORD_TOKEN"))
