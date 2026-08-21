import os
import discord
from discord.ext import commands

# Setting up intents so the bot can read messages and track tags
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Your Supreme Bot Owner ID (Updated!)
BOT_OWNER_ID = 1429893158740820056

# Set to store IDs of users allowed to use !fish
allowed_users = set()

@bot.event
async def on_ready():
    print(f"The squad is up! {bot.user.name} is running for Bot Owner Gaby! 🐟")

# 1. Grant Access Command (!access @user)
@bot.command(name="access")
async def access(ctx, member: discord.Member = None):
    # Only you (the Bot Owner) can run this command
    if ctx.author.id != BOT_OWNER_ID:
        await ctx.reply("❌ Only the bot owner can use this command!")
        return

    if member is None:
        await ctx.reply("❌ Please mention a user! Example: `!access @user`")
        return

    allowed_users.add(member.id)
    await ctx.reply(f"✅ Access GRANTED! {member.mention} can now use `!fish`.")

# 2. Revoke Access Command (!unaccess @user)
@bot.command(name="unaccess")
async def unaccess(ctx, member: discord.Member = None):
    # Only you (the Bot Owner) can run this command
    if ctx.author.id != BOT_OWNER_ID:
        await ctx.reply("❌ Only the bot owner can use this command!")
        return

    if member is None:
        await ctx.reply("❌ Please mention a user! Example: `!unaccess @user`")
        return

    if member.id in allowed_users:
        allowed_users.remove(member.id)
        await ctx.reply(f"❌ Access REVOKED! {member.mention} can no longer use `!fish`.")
    else:
        await ctx.reply(f"ℹ️ {member.name} didn't have access anyway.")

# 3. View Access List Command (!aclist)
@bot.command(name="aclist")
async def aclist(ctx):
    # Only you (the Bot Owner) can run this command
    if ctx.author.id != BOT_OWNER_ID:
        await ctx.reply("❌ Only the bot owner can use this command!")
        return

    if not allowed_users:
        await ctx.reply("ℹ️ The access list is currently empty. No one has permission to fish.")
        return

    # Build the list of users with access
    list_mentions = [f"• <@{user_id}>" for user_id in allowed_users]
    access_list_msg = "📋 **Users with access to `!fish`:**\n" + "\n".join(list_mentions)
    
    await ctx.reply(access_list_msg)

# 4. Classic Fish Command (!fish)
@bot.command(name="fish")
async def fish(ctx):
    # Bot Owner always has access, others must be in the allowed_users set
    if ctx.author.id == BOT_OWNER_ID or ctx.author.id in allowed_users:
        await ctx.reply("Here is ya fish 🐟")
    else:
        await ctx.reply("❌ 𝘚𝘰𝘳𝘳𝘺 𝘺𝘰𝘶 𝘤𝘶𝘳𝘳𝘦𝘯𝘵𝘭𝘺 𝘥𝘰𝘯’𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘢𝘯𝘥.")

bot.run(os.environ.get("DISCORD_TOKEN"))
