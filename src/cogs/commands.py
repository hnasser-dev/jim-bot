from discord.ext import commands
from src.utils.helpers import DiscordCtx, ExecutionOutcome, DBTimezone
from src.utils.error_handling import ExecutionError, DatabaseError, OtherError
from asyncio import TimeoutError
from src.utils.globals import TZ_LIST_URL, BOT_PREFIX


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
        server_in_db = self.bot.database.server_in_db(server_id=contxt.server_id)
        if not server_in_db:
            outcome = DatabaseError(
                contxt,
                ExecutionOutcome.WARNING,
                ("This server is not registered in the database.\n"
                f"Please use `{BOT_PREFIX}registerserver` before registering yourself.")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        outcome = self.bot.database.add_user_to_users(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        outcome = self.bot.database.add_user_to_server(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user("Successfully registered.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def deregister(self, ctx):
        """
        Deregister from the bot
        """
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.remove_user_from_all_servers(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        outcome = self.bot.database.remove_user_from_users(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user("Successfully deregistered.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def registerserver(self, ctx):
        """
        Add the server to the database
        """
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.register_server(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user(f"Successfully registered {contxt.server_name} as a server.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def joinserver(self, ctx):
        """
        Associate yourself with the current server
        """
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.add_user_to_server(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user("Successfully registered in this server.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def leaveserver(self, ctx):
        """
        Disassociate yourself from the current server
        """
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.remove_user_from_server(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user("Successfully deregistered from this server.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def timezone(self, ctx):
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.get_timezone(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user(f"Your current timezone is `{outcome}`.")

    @commands.command()
    async def settimezone(self, ctx, tz_identifier=None):
        contxt = DiscordCtx(ctx)
        if not tz_identifier:
            outcome = OtherError(
                contxt,
                ExecutionOutcome.WARNING,
                (f"Usage: `{BOT_PREFIX}settimezone <timezone_identifier>`"
                "If you wish to find your timezone identifier, use `{BOT_PREFIX}settimezone <timezone_identifier>`.")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        if tz_identifier.lower() == "options":
            outcome = OtherError(
                contxt,
                text = ("List of timezone identifiers (use the `TZ identifier` column - eg `America/New_York`):\n"
                "f**{TZ_LIST_URL}**")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        tz = DBTimezone(tz_identifier)
        if tz.pytz_tz is None:
            outcome = OtherError(
                contxt,
                level = ExecutionOutcome.WARNING,
                text = (f"{tz_identifier} is not a valid timezone identifier."
                        "If you wish to find your timezone identifier, use `{BOT_PREFIX}settimezone <timezone_identifier>`.")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        outcome = self.bot.database.set_timezone(contxt=contxt, timezone_id=tz.identifier)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user(f"Timezone successfully set to {outcome}.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def updatename(self, ctx):
        """
        Updates a user's name to their current discord user_name
        """
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.update_name(contxt=contxt)
        if isinstance(outcome, ExecutionError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user(f"Display name updated to {outcome}.", exec_outcome=ExecutionOutcome.SUCCESS)

    @commands.command()
    async def sesh(self, ctx, offset=None):
        contxt = DiscordCtx(ctx)
        if isinstance(offset, str) and offset.lower() == "yesterday":
            offset = -1
        if not isinstance(offset, int):
            await contxt.reply_to_user(
                "Invalid date offset provided. Please supply a valid date offset between -7 and 0 inclusive",
                exec_outcome=ExecutionOutcome.WARNING
            )
            return
        outcome = self.bot.database.add_sesh_for_user(contxt=contxt)
        if isinstance(outcome, OtherError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        self.bot.database.conn.commit()
        await contxt.reply_to_user(
            f"Session added! You have now been to the gym {outcome} times.",
            exec_outcome=ExecutionOutcome.SUCCESS
        )

    @commands.command()
    async def seshterday(self, ctx):
        """
        Alias for 'sesh yesterday'
        """
        await self.sesh(ctx, offset=-1)

    # TODO - the below commands
    @commands.command()
    async def table(self, ctx):
        contxt = DiscordCtx(ctx)
        table_data = self.bot.database.get_data_for_server(contxt=contxt)
        self.bot.database.conn.commit()
        await contxt.reply_to_user("<table>")



    @commands.command()
    async def graph(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        user_to_lookup = extract_id(other) if other else contxt.user_id
        visits = self.bot.database.get_user_visits(user_id=user_to_lookup)
        graph = self.bot.database.graphify(data=visits)
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