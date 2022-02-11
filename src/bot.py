from collections import defaultdict
from traceback import print_exception
from typing import Dict

from discord import Intents
from discord.ext.commands import Bot, MissingRequiredArgument
from tortoise import Tortoise

from src.config import token
from src.orm import init

intents = Intents(guilds=True, members=True)
bot = Bot(command_prefix="/", intents=intents)
defaults: Dict[int, Dict[str, str]] = defaultdict(dict)

_original_bot_close = bot.close
_original_bot_login = bot.login


async def on_close(*_, **__):
    await Tortoise.close_connections()
    await _original_bot_close(*_, **__)


async def on_login(*_, **__):
    await init()
    await _original_bot_login(*_, **__)


bot.close = on_close
bot.login = on_login

bot.load_extension("src.commands.note")
bot.load_extension("src.commands.help_command")

@bot.event
async def on_command_error(ctx, error: Exception):
    if isinstance(error, MissingRequiredArgument):
        return await ctx.send(f"Missing required argument `{error.param.name}`.")
    await ctx.send("Bot owner messed up, give him a nudge!")
    print_exception(type(error), error, error.__traceback__)


def main():
    bot.run(token)


if __name__ == '__main__':
    main()
