from discord.ext import commands
from utils.helpers import DiscordCtx, ExecutionOutcome, extract_id
from database import DatabaseError


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
        outcome1 = self.bot.database.register_user(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
            return
        outcome2 = self.bot.database.add_user_to_server(contxt=contxt)
        if isinstance(outcome2, DatabaseError):
            await contxt.reply_to_user(outcome2.text, exec_outcome=outcome2.level)
            return
        await contxt.reply_to_user("Successfully registered.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def deregister(self, ctx):
        """
        Deregister from the bot
        """
        contxt = DiscordCtx(ctx)
        outcome1 = self.bot.database.mark_user_as_inactive(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
            return
        outcome2 = self.bot.database.remove_user_from_all_servers(contxt=contxt)
        if isinstance(outcome2, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
            return
        await contxt.reply_to_user("Successfully deregistered.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def registerserver(self, ctx):
        """
        Add the server to the database
        """
        contxt = DiscordCtx(ctx)
        outcome1 = self.bot.database.register_server(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
            return
        await contxt.reply_to_user(f"Successfully registered {contxt.server_name} as a server.")

    @commands.command()
    async def joinserver(self, ctx):
        """
        Associate yourself with the current server
        """
        contxt = DiscordCtx(ctx)
        outcome1 = self.bot.database.add_user_to_server(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
        await contxt.reply_to_user("Successfully registered in this server.")

    @commands.command()
    async def leaveserver(self, ctx):
        """
        Disassociate yourself from the current server
        """
        contxt = DiscordCtx(ctx)
        outcome1 = self.bot.database.remove_user_from_server(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
        await contxt.reply_to_user("Successfully deregistered from this server.")

    @commands.command()
    async def timezone(self, ctx):
        contxt = DiscordCtx(ctx)
        timezone = self.bot.database.get_timezone(contxt=contxt)
        await contxt.reply_to_user(f"Your current timezone is {timezone}.")

    @commands.command()
    async def settimezone(self, timezone, ctx):
        contxt = DiscordCtx(ctx)
        new_timezone = self.bot.database.set_timezone(contxt=contxt)
        await contxt.reply_to_user(f"Timezone set to {new_timezone}.")

    @commands.command()
    async def updatename(self, ctx):
        """
        Updates a user's name to their current discord user_name
        """
        contxt = DiscordCtx(ctx)
        old_name, new_name = self.bot.database.update_name(contxt=contxt)
        if old_name == new_name:
            await contxt.reply_to_user(f"Display name already set to {new_name}.")
        else:
            await contxt.reply_to_user(f"Display name updated to {new_name}.")

    @commands.command()
    async def sesh(self, ctx):
        contxt = DiscordCtx(ctx)
        outcome1 = self.bot.database.add_sesh_for_user(contxt=contxt)
        if isinstance(outcome1, DatabaseError):
            await contxt.reply_to_user(outcome1.text, exec_outcome=outcome1.level)
        await contxt.reply_to_user(f"Session added! You have now been to the gym {outcome1} times.")

    @commands.command()
    async def seshterday(self, ctx):
        """
        Alias for 'sesh yesterday'
        """
        contxt = DiscordCtx(ctx)
        self.bot.database.add_sesh_for_user(contxt=contxt, day_offset=-1)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def graph(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        visits = self.bot.database.get_user_visits(user_id=user_to_lookup)
        graph = self.bot.database.graphify(data=visits)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def table(self, ctx):
        contxt = DiscordCtx(ctx)
        table_data = self.bot.database.get_data_for_server(contxt=contxt)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def visits(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        visits = self.bot.database.get_user_visits(contxt=contxt, user_id=user_to_lookup)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def lastvisit(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        last_visit = self.bot.database.get_user_visits(contxt=contxt, user_id=user_to_lookup, last_n=1)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def last(self, ctx, num_visits, other=None):
        """
        Display the last <num_visits> visits for yourself or <other>
        """
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        last_n_visits = self.bot.database.get_user_visits(contxt=contxt, user_id=user_to_lookup, last_n=num_visits)
        await contxt.reply_to_user("placeholder")

    @commands.command()
    async def helpme(self, ctx):
        contxt = DiscordCtx(ctx)
        await contxt.reply_to_user("placeholder")


async def setup(bot):
    await bot.add_cog(Commands(bot))