from discord.ext import commands


class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix

    @commands.Cog.listener()
    async def on_message(self, full_command_msg):        
        if full_command_msg.content.startswith(self.prefix):
            command_name, args = self.parse_full_command_str(full_command_msg.content)
            fake_ctx = await self.bot.get_context(full_command_msg)
            fake_ctx.command = self.bot.get_command(command_name)
            await self.bot.invoke(fake_ctx)

    @commands.command()
    async def sayhello(self, ctx):
        await ctx.reply("hello")

    @commands.command()
    async def saygoodbye(self, ctx, name):
        await ctx.reply(f"goodbye, {name}")

    def parse_full_command_str(self, full_command_str):
        prefix_and_command, *args = full_command_str.split()
        command_name = prefix_and_command.replace(self.prefix, "")
        return command_name, args


async def setup(bot):
    await bot.add_cog(Tests(bot))