import discord
from discord.ext.commands import Bot
import os
import traceback

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_BOT_GUILD_ID'))
ROLE_ID = int(os.getenv('DISCORD_BOT_ROLE_ID'))
WORD = os.getenv('DISCORD_BOT_WORD')

intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix='?', intents=intents)

guild = None
role = None


@bot.event
async def on_ready():
  global guild
  global role
  guild = bot.get_guild(GUILD_ID)
  role = guild.get_role(ROLE_ID)


@bot.event
async def on_command_error(ctx, error):
  orig_error = getattr(error, "original", error)
  error_msg = ''.join(
    traceback.TracebackException.from_exception(orig_error).format())
  await ctx.send(error_msg)


def is_DM(message):
  return isinstance(message.channel, discord.DMChannel)


@bot.command(name='r')
async def add_role(ctx, *args):
  """DM経由かつ合言葉が合っていれば役職を付与"""
  # 「?r あああ いいい」 → add_role(ctx, ['あああ', 'いいい']) → 'あああ いいい'
  # 「?r」 → add_role(ctx, []) → ''
  word = ' '.join(args)
  if role is not None and is_DM(ctx.message) and word == WORD:
    user = guild.get_member(ctx.message.author.id)
    await ctx.send("役職を付与しました。")
    await user.add_roles(role)
  else:
    await ctx.send('合言葉が間違っています。')


bot.run(TOKEN)
