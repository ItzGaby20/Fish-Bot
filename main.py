import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista VIP cu ID-ul tău și al lui Smart Kitty
VIP_USERS = [953181827415441438, 1278148946764501062]

@bot.event
async def on_ready():
    print(f"S-a aprins brigada! {bot.user.name} este online! 🐟")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        if message.author.id in VIP_USERS:
            await message.reply("Here is ya fish 🐟")

    await bot.process_commands(message)

bot.run(os.environ.get("DISCORD_TOKEN"))
