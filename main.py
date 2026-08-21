import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class FishBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.allowed_users = set()

    async def setup_hook(self):
        # Enrolls the command directly into the native Discord Apps Menu
        await self.tree.sync()

bot = FishBot()

# Your Supreme Bot Owner ID
BOT_OWNER_ID = 1429893158740820056

@bot.event
async def on_ready():
    print(f"The squad is up! {bot.user.name} is ready in the Apps Menu! 🐟")
    await bot.change_presence(activity=discord.CustomActivity(name="Thinking about fishes 🐟"))

# ==================== THE ULTIMATE TWO-TEXTBOX COMMAND ====================

@bot.tree.command(name="run", description="Execute a command in private")
@app_commands.describe(
    command="The action you want to perform (e.g., fish, access, unaccess, aclist, status, status2, cmd)",
    args="The value or user ID required for the command (leave empty if not needed)"
)
async def run_command(interaction: discord.Interaction, command: str, args: str = None):
    cmd_lower = command.lower().strip()
    user_id = interaction.user.id

    # 1. FISH COMMAND
    if cmd_lower == "fish":
        if user_id == BOT_OWNER_ID or user_id in bot.allowed_users:
            await interaction.response.send_message("Here is ya fish 🐟")
        else:
            await interaction.response.send_message("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭𝘺 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷ε 𝘱ε𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴ε 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘢𝘯𝘥.", ephemeral=True)
        return

    # 2. TROLL CMD COMMAND
    if cmd_lower == "cmd":
        await interaction.response.send_message("Imagine using this command only to realize that it does nothing. 🫵😂")
        return

    # --- ALL COMMANDS BELOW THIS LINE REQUIRE BOT OWNER PERMISSIONS ---
    if user_id != BOT_OWNER_ID:
        await interaction.response.send_message("❌ Only the bot owner can use this command argument!", ephemeral=True)
        return

    # 3. ACCESS COMMAND
    if cmd_lower == "access":
        if not args:
            await interaction.response.send_message("❌ Missing argument! Please provide a User ID in the args textbox.", ephemeral=True)
            return
        try:
            target_id = int(args.strip())
            bot.allowed_users.add(target_id)
            await interaction.response.send_message(f"✅ Access GRANTED! User <@{target_id}> can now use the fish command.")
        except ValueError:
            await interaction.response.send_message("❌ Invalid User ID in args! Please enter numbers only.", ephemeral=True)

    # 4. UNACCESS COMMAND
    elif cmd_lower == "unaccess":
        if not args:
            await interaction.response.send_message("❌ Missing argument! Please provide a User ID in the args textbox.", ephemeral=True)
            return
        try:
            target_id = int(args.strip())
            if target_id in bot.allowed_users:
                bot.allowed_users.remove(target_id)
                await interaction.response.send_message(f"❌ Access REVOKED! User <@{target_id}> can no longer fish.")
            else:
                await interaction.response.send_message(f"ℹ️ User <@{target_id}> didn't have access anyway.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid User ID in args! Please enter numbers only.", ephemeral=True)

    # 5. ACCESS LIST COMMAND
    elif cmd_lower == "aclist":
        if not bot.allowed_users:
            await interaction.response.send_message("ℹ️ The access list is currently empty.", ephemeral=True)
            return
        list_mentions = [f"• <@{u_id}>" for u_id in bot.allowed_users]
        await interaction.response.send_message("📋 **Users with access to fish:**\n" + "\n".join(list_mentions), ephemeral=True)

    # 6. STATUS COMMAND (PLAYING)
    elif cmd_lower == "status":
        if not args:
            await interaction.response.send_message("❌ Please provide the status text in the args textbox.", ephemeral=True)
            return
        await bot.change_presence(activity=discord.Game(name=args))
        await interaction.response.send_message(f"⚙️ Activity updated successfully to: **Playing {args}**", ephemeral=True)

    # 7. STATUS2 COMMAND (SPEECH BUBBLE)
    elif cmd_lower == "status2":
        if not args:
            await interaction.response.send_message("❌ Please provide the custom bubble text in the args textbox.", ephemeral=True)
            return
        await bot.change_presence(activity=discord.CustomActivity(name=args))
        await interaction.response.send_message(f"⚙️ Custom Status bubble updated successfully to: **{args}**", ephemeral=True)

    # UNKNOWN COMMAND
    else:
        await interaction.response.send_message(f"❌ Unknown command: `{command}`. Available: fish, cmd, access, unaccess, aclist, status, status2", ephemeral=True)

bot.run(os.environ.get("DISCORD_TOKEN"))
