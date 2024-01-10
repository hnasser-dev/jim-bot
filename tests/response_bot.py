from discord import Intents


def run_bot(bot_class, prefix, token):
    bot = bot_class(
        command_prefix=prefix,
        description="Response Bot",
        intents=Intents.all(),
        load_tests=True
    )

    @bot.event
    async def on_ready():
        print("response_bot ready")

    bot.run(token)