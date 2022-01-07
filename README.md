<p align="center">
<img style="width: 35vw" src="assets/img/logo.png">
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
|upcoming|`-upcoming`|Displays the upcoming Codeforces contests, along with the date, time and duration.
|problem|`-problem`|Displays a random problem.
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
* Edit the created `.env` file and replace the `PASTE TOKEN HERE` with the token that you copied earlier. You can also set your preferred command prefix.

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

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/fire.png"><br>

## Future Plans/Issues

* Contest Reminders
* Ensuring users get only unsolved problems to solve
* Expanding to other popular competitive programming sites such as AtCoder, Codechef, etc.

I'm open to PRs, so if you would like to change, improve or add something, feel free to make a PR. Contributions are always welcome!


