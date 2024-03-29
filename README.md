<p align="center">
<img style="width: 10vw" src="assets/img/logo.png">
</p>

<div align="center">

# Botforces - A Codeforces Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](https://www.python.org/)
[![GitHub issues](https://img.shields.io/github/issues/coniferousdyer/Botforces)](https://github.com/coniferousdyer/Botforces/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg?style=flat-square)](http://makeapullrequest.com)

</div>

This is a Discord bot, written in Python, which provides certain functionalities helpful to users in a Codeforces-based Discord server. It interacts with the Codeforces API to obtain the required real-time data and uses it to carry out the command requested.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png"><br>

## Features

* Displays information about any user, their submission history, and visualizations of their performance.

* Suggests random problems to users, with optional ratings and tags so that users can easily find problems they are interested in and improve their skills.

* Displays information about upcoming Codeforces contests.

* Lets users engage in duels, battles of logic and skill, where two users attempt to solve the same problem faster than each other.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png"><br>

## Commands

The prefix here has been assumed to be `-`, but you can set it to whatever you like.

|Command|Syntax|Description|
|-------|------|-----------|
|help|`-help`|Displays all the available commands.|
||`-help <command>`|Displays what the command does, as well as its syntax.
user|`-user <handle>`|Displays information about the Codeforces user with the requested handle.
|register|`-register <handle>`|Stores a mapping between the Discord account that sent the command and the Codeforces handle.
|unregister|`-unregister`|Removes a stored mapping if any between the Discord account that sent the command and their stored Codeforces handle.
|upcoming|`-upcoming`|Displays the upcoming Codeforces contests, along with the date, time and duration.
|problem|`-problem`|Displays a random problem (unsolved by the user if registered).
||`-problem <rating>`|Displays a random problem of that rating.
||`-problem <tags>`|Displays a random problem having the requested tags (can include multiple tags, tags with more than one word must be enclosed in double quotes, for eg. "binary search")
||`-problem <rating> <tags>`|Displays a random problem of that rating and having the requested tags. The order does not matter.
|stalk|`-stalk <username> <n>`|Displays the last n problems solved by the user.
|plotrating|`-plotrating <handle>`|Plots the problems done by a user, grouped by rating.
|plotindex|`-plotindex <handle>`|Plots the problems done by a user, grouped by index.
|plottags|`-plottags <handle>`|Plots the problems done by a user, grouped by tags.
|duel|`-duel <user_mention> <optional_rating> <optional_tags`|Challenges the mentioned user to a duel (over a problem of the provided rating/tags, if mentioned).
|endduel (only if a duel is in progress)|`-endduel`|If sent by one of the users in a duel, ends the duel and checks the result to see who won.
|duelstats|`-duelstats`|Displays information about all ongoing duels.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png"><br>

## Setup

If you would rather not go through the hassle of setting up the bot locally, you can use the [invite link](https://discord.com/api/oauth2/authorize?client_id=873139272377573426&permissions=534723951680&scope=bot) instead to add the bot to your server.

But if you do wish to set it up locally, you can do so by following the steps below.

### I. Getting your token

Follow the steps <a href="https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token">here</a> to obtain your token and add the bot to the server. You will need it in order to run your bot successfully.

### II. Setting things up on your system

1. Open up your terminal and clone the repository.

2. Go to the directory you cloned and create a virtual environment.

```bash
cd Botforces

# Give the virtual environment a name of your choice
python3 -m venv <name_of_virtual_environment>
```

3. Activate the virtual environment (on MacOS/Linux).

```bash
source <name_of_virtual_environment>/bin/activate
```

4. Install the required modules within your virtual environment.

```bash
pip install -r requirements.txt
```

5. A `.env.template` file has been added. You can run the following command to create your `.env` file from the template.
```bash
cp .env.template .env
```
* Edit the created `.env` file and replace the `PASTE TOKEN HERE` with the token that you copied earlier. You can also set your preferred command prefix (`-` by default).

* Optionally, you can set up error logging with Sentry for the bot. All you need to do is copy the Sentry DSN from the Sentry website and paste it in the `SENTRY_DSN` variable in the `.env` file. Note, however, that this is not required for the bot to run.

You now have everything set up to run the bot.

<b>Note:</b> In order to deactivate your virtual environment,

```bash
deactivate
```

### III. Running the bot

In order to run your bot, you simply have to do this:

```bash
python main.py
```

You're all set! The bot should be online now. 

Keep in mind though, that if you close the terminal, the program will terminate and the bot will go offline.

### IV. User Registration

While Botforces does provide unsolved problems only as part of the problem suggestion feature, this is possible only if the user performs the `register` command. A registration is basically a mapping between their Discord account and a Codeforces handle of their choice. This mapping would be used by the `problem` command to ensure that suggested problems have not been solved by the user.

In order to do this, send the following command via Discord text after the bot has been added to the server. For example, if my Codeforces handle is "abcdef",
```
-register abcdef
```

The bot would automatically store the mapping between your Discord account and the "abcdef" account on Codeforces. Now, if this Discord user requests a problem, they would only get problems that have not been solved by "abcdef" on Codeforces.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png"><br>

## Future Plans/Issues

* Contest Reminders
* Expanding to other popular competitive programming sites such as AtCoder, Codechef, etc.

I'm open to PRs, so if you would like to change, improve or add something, feel free to make a PR. Contributions are always welcome!

## License

This software is open source, licensed under the [MIT License](https://github.com/coniferousdyer/Botforces/blob/master/LICENSE).
