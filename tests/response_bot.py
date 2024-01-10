from discord import Intents


def run_bot(bot_class, prefix, discord_admin_id, token):
    bot = bot_class(
        command_prefix=prefix,
        description="Response Bot",
        intents=Intents.all(),
        admin_id=discord_admin_id,
        load_tests=True,
        load_admin_commands=True
    )

    bot.run(token)