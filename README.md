# Codeforces Bot

This is a Discord bot, written in Python, which provides certain basic functionalities helpful to Codeforces users. It interacts with the Codeforces API to obtain the data and uses it to carry out the command requested.

## Commands

|Command|Syntax|Description|
|-------|------|-----------|
|help|`-help`|Displays all the available commands.|
||`-help <command>`|Displays what the command does, as well as its syntax.
user|`-user <handle>`|Displays information about the Codeforces user with the requested handle.
|upcoming|`-upcoming`|Displays the upcoming Codeforces contests, along with the date, time and duration.
|problem|`-problem`|Displays a random problem.
||`-problem <rating>`|Displays a random problem of that rating.
||`-problem <tags>`|Displays a random problem having the requested tags (can include multiple tags, tags with more than one word must be enclosed in double quotes, for eg. "binary search")
||`-problem <rating> <tags>`|Displays a random problem of that rating and having the requested tags. The order does not matter.
|stalk|`-stalk <username> <n>`|Displays the last n problems solved by the user.
|plotrating|`-plotrating <handle>`|Plots the problems done by a user, grouped by rating.
|plotindex|`-plotindex <handle>`|Plots the problems done by a user, grouped by index.
|plottags|`-plottags <handle>`|Plots the problems done by a user, grouped by tags.
|duel|`-duel <user_mention> <rating>`|Challenges the mentioned user to a duel over a problem of the provided rating.
|endduel (only if a duel is in progress)|`endduel`|If sent by one of the users in a duel, ends the duel and checks the result to see who won.
|lockout|`-lockout <user_mention>`|Challenges the mentioned user to a lockout match.

## Setup

### I. Getting your token

Follow the steps <a href="https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token">here</a> to obtain your token and add the bot to the server. You will need it in order to run your bot successfully.

### II. Setting things up on your system

1. Open up your terminal and clone the repository.

```bash
$ git clone https://github.com/coniferousdyer/Codeforces-Bot.git
```

2. Go to the directory you cloned and create a virtual environment.

```bash
$ cd Codeforces-Bot

# Give the virtual environment a name of your choice
python3 -m venv <name_of_virtual_environment>
```

3. Activate the virtual environment (on MacOS/Linux).

```bash
$ source <name_of_virtual_environment>/bin/activate
```

4. Install the required modules within your virtual environment.

```bash
$ pip install -r requirements.txt
```

5. Create a file in the directory and name it `.env`. Take the token you copied earlier and paste it in place of `PASTE_TOKEN_HERE`. Then paste the following line in the `.env` file.

```bash
DISCORD_TOKEN=PASTE_TOKEN_HERE
```

You now have everything set up to run the bot.

<b>NOTE:</b> In order to deactivate your virtual environment,

```bash
$ deactivate
```

### III. Running the bot

In order to run your bot, you simply have to do this:

```bash
$ python3 main.py
```

You're all set! The bot should be online now. 

Keep in mind though, that if you close the terminal, the program will terminate and the bot will go offline.

## Future Plans

* Lockout Matches
* Contest Reminders
* Switching to an SQL-based database system to store data
* Refactoring the code and distributing it for better maintainability

<b>NOTE:</b> This is still in progress, and may not be complete. I'm open to PRs, so if you would like to change, improve or add something, feel free to make a PR!


