from discord.ext import commands
from utils.helpers import DiscordCtx, extract_id
from database import DBErrorHandler


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        """
        Register to be tracked by the bot
        Automatically joins the current server (joinserver), too
        """
        contxt = DiscordCtx(ctx)
        err1 = self.bot.database.register_user(user_id=contxt.user_id)
        if isinstance(err1, DBErrorHandler):
            await contxt.report(err1.text, log_level=err1.level)
            return
        err2 = self.bot.database.add_user_to_server(user_id=contxt.user_id, server_id=contxt.server_id)
        if isinstance(err2, DBErrorHandler):
            await contxt.report(err2.text, log_level=err1.level)
            return
        await contxt.report("placeholder")

    @commands.command()
    async def deregister(self, ctx):
        """
        Deregister from the bot
        """
        contxt = DiscordCtx(ctx)
        self.bot.database.deregister_user(user_id=contxt.user_id)
        self.bot.database.remove_user_from_all_servers(user_id=contxt.user_id)
        await contxt.report("placeholder")

    @commands.command()
    async def joinserver(self, ctx):
        """
        Associate yourself with the current server
        """
        contxt = DiscordCtx(ctx)
        self.bot.database.add_user_to_server(user_id=contxt.user_id, server_id=contxt.server_id)
        await contxt.report("placeholder")

    @commands.command()
    async def leaveserver(self, ctx):
        """
        Disassociate yourself from the current server
        """
        contxt = DiscordCtx(ctx)
        self.bot.database.remove_user_from_server(user_id=contxt.user_id, server_id=contxt.server_id)
        await contxt.report("placeholder")

    @commands.command()
    async def timezone(self, ctx):
        contxt = DiscordCtx(ctx)
        timezone = self.bot.database.get_timezone(user_id=contxt.user_id)
        await contxt.report(f"Your current timezone is {timezone}.")

    @commands.command()
    async def settimezone(self, timezone, ctx):
        contxt = DiscordCtx(ctx)
        new_timezone = self.bot.database.set_timezone(user_id=contxt.user_id, timezone=timezone)
        await contxt.report(f"Timezone set to {new_timezone}.")

    @commands.command()
    async def updatename(self, ctx):
        """
        Updates a user's name to their current discord user_name
        """
        contxt = DiscordCtx(ctx)
        old_name, new_name = self.bot.database.update_name(user_id=contxt.user_id, new_name=contxt.user_name)
        if old_name == new_name:
            await contxt.report(f"Display name already set to {new_name}.")
        else:
            await contxt.report(f"Display name updated to {new_name}.")

    @commands.command()
    async def sesh(self, ctx):
        contxt = DiscordCtx(ctx)
        self.bot.database.add_sesh_for_user(user_id=contxt.user_id)
        await contxt.report("placeholder")

    @commands.command()
    async def seshterday(self, ctx):
        """
        Alias for 'sesh yesterday'
        """
        contxt = DiscordCtx(ctx)
        self.bot.database.add_sesh_for_user(user_id=contxt.user_id, day_offset=-1)
        await contxt.report("placeholder")

    @commands.command()
    async def graph(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        visits = self.bot.database.get_user_visits(user_id=user_to_lookup)
        graph = self.bot.database.graphify(data=visits)
        await contxt.report("placeholder")

    @commands.command()
    async def table(self, ctx):
        contxt = DiscordCtx(ctx)
        table_data = self.bot.database.get_data_for_server(server_id=contxt.server_id)
        await contxt.report("placeholder")

    @commands.command()
    async def visits(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        visits = self.bot.database.get_user_visits(user_id=user_to_lookup)
        await contxt.report("placeholder")

    @commands.command()
    async def lastvisit(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        last_visit = self.bot.database.get_user_visits(user_id=user_to_lookup, last_n=1)
        await contxt.report("placeholder")

    @commands.command()
    async def last(self, ctx, num_visits, other=None):
        """
        Display the last <num_visits> visits for yourself or <other>
        """
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        last_n_visits = self.bot.database.get_user_visits(user_id=user_to_lookup, last_n=num_visits)
        await contxt.report("placeholder")

    @commands.command()
    async def helpme(self, ctx):
        contxt = DiscordCtx(ctx)
        await contxt.report("placeholder")


async def setup(bot):
    await bot.add_cog(Commands(bot))