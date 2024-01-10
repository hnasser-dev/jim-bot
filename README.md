# Jim Bot
### A Discord bot that helps you track your gym visits.

This is a remade version of my [previous Discord bot](https://github.com/finahdinner/discord-gym-bot), with additional functionality and a more robust design.

### Invite link: <b>https://discord.com/api/oauth2/authorize?client_id=1001599833586552993&permissions=2048&scope=bot</b>


## Commands

`jim/registerserver`<br>
Register the current server in the bot's database. Allows users to register themselves (with `jim/register` - see below) via the current server.

`jim/register`<br>
Register yourself, as an individual, in the bot's database. You can only register yourself while in a server that is itself registered.

`jim/joinserver`<br>
Associate yourself with the current (registered) server. This causes you to show up on `jim/table` when it is used. You must already be registered as an individual in order to 'join' a server.

`jim/leaveserver`<br>
Disassociate yourself from the current (registered) server. Prevents you from appearing on `jim/table` when it is used.

`jim/sesh [OPTIONAL_day_offset]`<br>
By default, this will record a gym visit for the current date and time. `day_offset` allows you to specify an integer, between -7 and 0 inclusive, indicating how many days you wish to backdate the session. EG to record a gym visit for 2 days ago, you would use `jim/sesh -2`.

`jim/seshterday`<br>
Alias for `jim/sesh -1`. Adds a gym visit backdated to yesterday.

`jim/visits [@user]`<br>
Retrieve the number of gym visits you have made in total. Can specify a `[@user]`, either by their ID or by directly pinging them, to retrieve their number of gym visits.

`jim/last <N>`<br>
Retrieve the dates of your last `N` gym visits (max 10). Can specify a `[@user]`, either by their ID or by directly pinging them, to retrieve the dates of their last `N` gym visits.

`jim/lastvisit [@user]`<br>
Alias for `jim/last 1`.

`jim/graph [@user]`<br>
View a calendar, which shows all of your recorded gym visits in an easily-viewable format. Can specify a `[@user]`, either by their ID or by directly pinging them, to a calendar for their gym visits instead.

`jim/table`<br>
Shows the `name`, `discord id` and `number of visits` for each registered user in the current server.

`jim/all`<br>
Alias for `jim/all`.

`jim/timezone`<br>
Retrieve the timezone (default UTC) which is listed alongside your account in the database. Having your local timezone set means that all dates (eg with `jim/last <N>` and `jim/graph`) will be according to your own timezone.

`jim/settimezone <timezone>`<br>
Set your timezone, by specifiying a `<timezone>` corresponding to a valid timezone identifier (listed in the [IANA timezone database](https://en.wikipedia.org/wiki/Tz_database)). Using the command `jim/settimezone details` will redirect the user to a [list of all valid timezone identifiers](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

`jim/updatename`<br>
Update the name associated with your Discord account in the database. Will only work if your current Discord username is different to your username recorded in the database.

`jim/invite`<br>
Retrieve an invite link for the bot, which may be used to invite the bot to your own Discord server.

`jim/help`<br>
Display information relating to each command.


## Creating your own instance of this bot

### Quick start guide

- Clone this repository, using `git clone git@github.com:finahdinner/jim-bot.git`.<br>
Ensure you have a suitable SSH key set up on your machine (see [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) for information regarding this).
- Create a Python virtual environment, then activate it and use `pip install -r requirements.txt` to install the required dependencies.
- Create your own [Discord Application](https://discord.com/developers/applications), and create a Bot.<br>
Note down this bot's **Token** and generate a suitable invite link (it should end in `&permissions=2048&scope=bot`).
- Create an `.env` file, and place it in the root of your project.<br>
Ensure that it has the following key-value pairs listed.

    ```
    DEBUG="False"
    DISCORD_GYM_BOT_TOKEN="<bot_token>"
    BOT_TEST_TOKEN="<put_anything_here>"
    DISCORD_ADMIN_ID="<your_personal_discord_ID>"
    DISCORD_INVITE_LINK="<bot_invite_link>"
    ```
- Whilst in the root of the project folder, run `python main.py` (or `py`/`python3` if needed) to start up the bot.
    