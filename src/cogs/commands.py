from discord.ext import commands
from src.utils.helpers import DiscordCtx, ExecutionOutcome, DBTimezone
from src.utils.error_handling import ExecutionError, DatabaseError, OtherError
from src.utils.globals import TZ_LIST_URL, BOT_PREFIX, DISCORD_INVITE_LINK
import src.utils.graphing as graphing
from table2ascii import table2ascii
import textwrap


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        await ctx.reply(f"Bot invite link:\n{DISCORD_INVITE_LINK}")

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
        await contxt.reply_to_user(f"Your current timezone is `{outcome}`.")

    @commands.command()
    async def settimezone(self, ctx, tz_identifier=None):
        contxt = DiscordCtx(ctx)
        if not tz_identifier:
            outcome = OtherError(
                contxt,
                text=(f"Usage: `{BOT_PREFIX}settimezone <timezone_identifier>`\n"
                f"If you wish to find your timezone identifier, use `{BOT_PREFIX}settimezone details`.")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        if tz_identifier.lower() == "details":
            outcome = OtherError(
                contxt,
                text = ("List of timezone identifiers (use the `TZ identifier` column - eg `America/New_York`):\n"
                f"**{TZ_LIST_URL}**")
            )
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        tz = DBTimezone(tz_identifier)
        if tz.pytz_tz is None:
            outcome = OtherError(
                contxt,
                level = ExecutionOutcome.WARNING,
                text = (f"{tz_identifier} is not a valid timezone identifier.\n"
                        f"If you wish to find your timezone identifier, use `{BOT_PREFIX}settimezone details`.")
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
    async def sesh(self, ctx, offset="0"):
        contxt = DiscordCtx(ctx)
        if isinstance(offset, str) and offset.lower() == "yesterday":
            offset = -1
        else:
            try:
                offset = int(offset)
            except ValueError as e:
                outcome = OtherError(
                    contxt,
                    ExecutionOutcome.WARNING,
                    "Invalid date offset provided. Please supply a valid day offset between -7 and 0 inclusive",
                    exception=e
                )
                await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
                return
        outcome = self.bot.database.add_sesh_for_user(contxt=contxt, offset=offset)
        if isinstance(outcome, ExecutionError):
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
        await self.sesh(ctx, offset="-1")

    @commands.command()
    async def removelast(self, ctx):
        """ Remove your last gym visit """
        contxt = DiscordCtx(ctx)
        err = self.bot.database.remove_last_visit_for_user(contxt=contxt)
        if isinstance(err, DatabaseError):
            await contxt.reply_to_user(err.text, err.level)
            return
        new_num_visits = self.bot.database.get_num_user_visits(
            contxt=contxt,
            lookup_id=contxt.user_id
        )
        if isinstance(new_num_visits, DatabaseError):
            await contxt.reply_to_user(new_num_visits.text, new_num_visits.level)
            return
        await contxt.reply_to_user(
            f"Successfully removed your last visit. Your sesh count is now {new_num_visits}.",
            exec_outcome=ExecutionOutcome.SUCCESS
        )

    @commands.command()
    async def visits(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        lookup_id = contxt.user_id if not other else DiscordCtx.extract_id(other)
        self_lookup = True if lookup_id == contxt.user_id else False
        lookup_name = self.bot.database.get_user_name_from_id(user_id=lookup_id)
        if not lookup_name:
            err_msg = "You are not registered in the database." if self_lookup else "The provided user is not registered in the database."
            err = DatabaseError(contxt, ExecutionOutcome.WARNING, err_msg)
            await contxt.reply_to_user(err.text, err.level)
            return
        num_visits = self.bot.database.get_num_user_visits(contxt, lookup_id)
        match self_lookup:
            case True:
                if num_visits == 0: msg = "You have not been to the gym yet."
                elif num_visits == 1: msg = "You have been to the gym once."
                else: msg = f"You have been to the gym {num_visits} times."
            case False:
                if num_visits == 0: msg = f"{lookup_name} has not been to the gym yet."
                elif num_visits == 1: msg = f"{lookup_name} has been to the gym once."
                else: msg = f"{lookup_name} has been to the gym {num_visits} times."
        await contxt.reply_to_user(msg)

    @commands.command()
    async def last(self, ctx, num_visits, other=None):
        contxt = DiscordCtx(ctx)
        lookup_id = contxt.user_id if not other else DiscordCtx.extract_id(other)
        self_lookup = True if lookup_id == contxt.user_id else False
        lookup_name = self.bot.database.get_user_name_from_id(user_id=lookup_id)
        if not lookup_name:
            err_msg = "You are not registered in the database." if self_lookup else "The provided user is not registered in the database."
            err = DatabaseError(contxt, ExecutionOutcome.WARNING, err_msg)
            await contxt.reply_to_user(err.text, err.level)
            return
        outcome = self.bot.database.get_last_n_visits_dates(contxt, lookup_id, n=num_visits)
        if isinstance(outcome, ExecutionError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        timezone_id = self.bot.database.get_timezone(contxt, lookup_info=(lookup_name, lookup_id))
        timezone = DBTimezone(timezone_id)
        if not timezone.pytz_tz: # if for some reason the timezone in the db is not valid
            err = OtherError(contxt, ExecutionOutcome.ERROR)
            await contxt.reply_to_user(err.text, err.level)
            return
        unix_dates, column_names = outcome
        # get localised dates in a readable format
        dates = []
        for unix_date, in unix_dates: # leave the , --> needed to unpack size 1 tuple
            local_dt = DBTimezone.get_local_time(unix_date, timezone.pytz_tz)
            local_date, local_time = local_dt.strftime("%d %b %Y"), local_dt.strftime("%H:%M:%S")
            # insert dates in reverse chronological order
            dates.insert(0, (local_date, local_time, DBTimezone.days_ago_str(contxt.timestamp, unix_date)))
        refer_to_as = "You" if self_lookup else lookup_name
        if int(num_visits) == 1:
            msg = f"{refer_to_as} last visited the gym on {dates[0][0]}, at {dates[0][1]} ({dates[0][2]})."
        else:
            column_names += ["time"] + ["days_ago"] # [date, time, days_ago]
            data_table = table2ascii(header=column_names, body=dates)
            msg = f"```Last {num_visits} gym visits for {lookup_name}:\n{data_table}```"
        await contxt.reply_to_user(msg)

    @commands.command()
    async def lastvisit(self, ctx, other=None):
        await self.last(ctx, num_visits=1, other=other)

    @commands.command()
    async def table(self, ctx):
        contxt = DiscordCtx(ctx)
        outcome = self.bot.database.get_visits_data_for_server(contxt=contxt)
        if isinstance(outcome, DatabaseError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        data, column_names = outcome
        if not data:
            err = OtherError(contxt, ExecutionOutcome.WARNING, f"No users have yet registered in {contxt.server_name}.")
            await contxt.reply_to_user(err.text, err.level)
            return
        data_table = table2ascii(header=column_names, body=data)
        await contxt.reply_to_user(f"```Gym visits data for {contxt.server_name}:\n{data_table}```")

    @commands.command()
    async def all(self, ctx):
        """ Alias for jim/table """
        await self.table(ctx)

    @commands.command()
    async def graph(self, ctx, other=None):
        contxt = DiscordCtx(ctx)
        lookup_id = contxt.user_id if not other else DiscordCtx.extract_id(other)
        self_lookup = True if lookup_id == contxt.user_id else False
        lookup_name = self.bot.database.get_user_name_from_id(user_id=lookup_id)
        if not lookup_name:
            err_msg = "You are not registered in the database." if self_lookup else "The provided user is not registered in the database."
            err = DatabaseError(contxt, ExecutionOutcome.WARNING, err_msg)
            await contxt.reply_to_user(err.text, err.level)
            return
        outcome = self.bot.database.get_all_user_visits(contxt, lookup_id)
        if isinstance(outcome, ExecutionError):
            await contxt.reply_to_user(outcome.text, exec_outcome=outcome.level)
            return
        if len(outcome) < 1:
            err_msg = "You haven't been to the gym yet!" if self_lookup else f"{lookup_name} hasn't been to the gym yet!"
            err = OtherError(contxt, ExecutionOutcome.DEFAULT, err_msg)
            await contxt.reply_to_user(err.text, err.level)
            return
        timezone_id = self.bot.database.get_timezone(contxt, lookup_info=(lookup_name, lookup_id))
        timezone = DBTimezone(timezone_id)
        if not timezone.pytz_tz: # if for some reason the timezone in the db is not valid
            err = OtherError(contxt, ExecutionOutcome.ERROR)
            await contxt.reply_to_user(err.text, err.level)
            return
        # graphing
        unix_dates = outcome
        user_added_time = self.bot.database.get_user_join_time_from_id(lookup_id)
        user_added_time_local_dt = DBTimezone.get_local_time(user_added_time, timezone.pytz_tz)
        if not user_added_time: # if for some reason the user join_time can't be found
            err = OtherError(contxt, ExecutionOutcome.ERROR)
            await contxt.reply_to_user(err.text, err.level)
            return
        local_dates = []
        for unix_date, in unix_dates: # leave the , --> needed to unpack size 1 tuple
            local_dt = DBTimezone.get_local_time(unix_date, timezone.pytz_tz)
            local_dates.append(local_dt)
        curr_dt_local = DBTimezone.get_local_time(contxt.timestamp, timezone.pytz_tz)
        graph_file = graphing.graph_data(
            start_dt_local=user_added_time_local_dt,
            curr_date_dt_local=curr_dt_local,
            visit_dates_dt_local=local_dates,
            user_name=lookup_name
        )
        await contxt.ctx.reply(file=graph_file, mention_author=False)

    @commands.command()
    async def help(self, ctx):
        contxt = DiscordCtx(ctx)
        commands_msg = textwrap.dedent(f"""\
            `{BOT_PREFIX}register` --> register yourself for tracking
            `{BOT_PREFIX}deregister` --> deregister yourself from tracking
            `{BOT_PREFIX}registerserver` --> register this server for tracking
            `{BOT_PREFIX}joinserver` --> associate yourself with this server
            `{BOT_PREFIX}leaveserver` --> disassociate yourself from this server
            `{BOT_PREFIX}sesh [day_offset]` --> record a gym session (`day_offset` can record seshes `up to 7 days into the past`)
            `{BOT_PREFIX}seshterday` --> record a gym session for yesterday (`day offset = -1`)
            `{BOT_PREFIX}removelast` --> remove your last recorded gym session from the database
            `{BOT_PREFIX}visits [@user]` --> see how many times you (or someone else) has been to the gym
            `{BOT_PREFIX}last <N> [@user]` --> look at your (or someone else's) `last N gym visits`
            `{BOT_PREFIX}lastvisit [@user]` --> look up when you (or someone else) last went to the gym
            `{BOT_PREFIX}table` --> show details for users registered in this server
            `{BOT_PREFIX}all` --> same as `{BOT_PREFIX}table`
            `{BOT_PREFIX}timezone` --> retrieve your current timezone (default UTC)
            `{BOT_PREFIX}settimezone <timezone>` --> set yourself a new timezone (`{BOT_PREFIX}settimezone details` for more details)
            `{BOT_PREFIX}graph [@user]` --> view your (or someone else's) gym visits as a graph
            `{BOT_PREFIX}updatename` --> update your name in the database to your current Discord username
            `{BOT_PREFIX}invite` --> retrieve the invite link for this bot
            `{BOT_PREFIX}help` --> *commandception intensifies*
        """)
        await contxt.reply_to_user(commands_msg)


async def setup(bot):
    await bot.add_cog(Commands(bot))