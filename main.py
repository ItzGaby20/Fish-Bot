import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOT_OWNER_ID = 1429893158740820056

# Dicționar pentru permisiuni dinamice per comandă
cmd_permissions = {}

@bot.event
async def on_ready():
    print(f"The squad is up! {bot.user.name} is running smoothly! 🐟")
    await bot.change_presence(activity=discord.CustomActivity(name="Thinking about fishes 🐟"))


# ==================== ADVANCED PERMISSION SYSTEM ====================

@bot.command(name="cmdaccess")
async def cmdaccess(ctx, member: discord.Member = None, cmd_name: str = None):
    if ctx.author.id != BOT_OWNER_ID:
        return

    if not member or not cmd_name:
        await ctx.reply("❌ Usage: `!cmdaccess @user [command_name]`\nExample: `!cmdaccess @John gberease`")
        return

    cmd_name = cmd_name.lower().replace("!", "")

    if not bot.get_command(cmd_name):
        await ctx.reply(f"❌ The command `!{cmd_name}` does not exist.")
        return

    if member.id not in cmd_permissions:
        cmd_permissions[member.id] = []
    
    if cmd_name not in cmd_permissions[member.id]:
        cmd_permissions[member.id].append(cmd_name)
        await ctx.reply(f"✅ Access GRANTED! {member.mention} can now use `!{cmd_name}`.")
    else:
        await ctx.reply(f"ℹ️ {member.mention} already has access to `!{cmd_name}`.")


@bot.command(name="access")
async def access(ctx, member: discord.Member = None):
    if ctx.author.id != BOT_OWNER_ID: return
    if member:
        if member.id not in cmd_permissions:
            cmd_permissions[member.id] = []
        if "fish" not in cmd_permissions[member.id]:
            cmd_permissions[member.id].append("fish")
        await ctx.reply(f"✅ Access GRANTED to {member.mention} for `!fish`.")

@bot.command(name="unaccess")
async def unaccess(ctx, member: discord.Member = None):
    if ctx.author.id != BOT_OWNER_ID: return
    if member and member.id in cmd_permissions:
        cmd_permissions.pop(member.id, None)
        await ctx.reply(f"❌ Revoked ALL custom command access from {member.mention}.")


# ==================== CLASSIC CHAT COMMANDS ====================

@bot.command(name="fish")
async def fish(ctx):
    has_perm = member_has_perm(ctx.author.id, "fish")
    if ctx.author.id == BOT_OWNER_ID or has_perm: 
        await ctx.reply("Here is ya fish 🐟")
    else: 
        await ctx.reply("❌ 𝘚𝘰𝘳𝘳ÿ ÿ𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭ÿ 𝘥ｏｎ’ｔ 𝘩ａｖｅ 𝘱ｅ𝘳𝘮𝘪𝘴𝘴𝘪ｏｎ...")

@bot.command(name="ping")
async def ping(ctx):
    has_perm = member_has_perm(ctx.author.id, "ping")
    if ctx.author.id == BOT_OWNER_ID or has_perm:
        latency = round(bot.latency * 1000)
        await ctx.reply(f"🏓 **Pong!** Latency is **{latency}ms**.")
    else:
        await ctx.reply("❌ 𝘚𝘰𝘳𝘳ÿ ÿ𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭ÿ 𝘥ｏｎ’ｔ 𝘩ａｖｅ 𝘱ｅ𝘳𝘮𝘪𝘴𝘴𝘪ｏｎ...")


# ==================== BOT MESSAGE PURGE COMMAND ====================

@bot.command(name="gberase")
async def gberease(ctx):
    # REPARAT: Acum verifică dacă utilizatorul este owner SAU are permisiune primită prin !cmdaccess
    has_perm = member_has_perm(ctx.author.id, "gberease")
    
    if ctx.author.id != BOT_OWNER_ID and not has_perm:
        await ctx.reply("❌ Only the bot owner or authorized users can use this command!")
        return

    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    def is_bot(message):
        return message.author.id == bot.user.id

    try:
        deleted = await ctx.channel.purge(limit=100, check=is_bot)
        await ctx.send(f"🧹 Successfully deleted {len(deleted)} of my messages from this channel.", delete_after=3)
    except discord.Forbidden:
        await ctx.send("❌ I do not have the `Manage Messages` permission required to delete messages.", delete_after=5)


# ==================== HELPER FUNCTIONS ====================

def member_has_perm(user_id: int, cmd_name: str) -> bool:
    if user_id in cmd_permissions:
        return cmd_name in cmd_permissions[user_id]
    return False

bot.run(os.environ.get("DISCORD_TOKEN"))
