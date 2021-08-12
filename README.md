# Codeforces Bot

This is a Discord bot which provides certain basic functionalities helpful to Codeforces users. It interacts with the Codeforces API to obtain the data and uses it to carry out the command requested.

## Commands

|Command|Syntax|Description|
|-------|------|-----------|
|help|`-help`|Displays all the available commands, along with descriptions of what they do.|
user|`-user <handle>`|Displays information about the Codeforces user with the requested handle.
|upcoming|`-upcoming`|Displays the upcoming Codeforces contests, along with the date, time and duration.
|problem|`-problem`|Displays a random problem.
||`-problem <rating>`|Displays a random problem of that rating.
||`-problem <tags>`|Displays a random problem having the requested tags (can include multiple tags, tags with more than one word must be enclosed in double quotes, for eg. "binary search")
||`-problem <rating> <tags>`|Displays a random problem of that rating and having the requested tags. The order does not matter.
|stalk|`-stalk <username> <n>`|Displays the last n submissions of the user, and their verdict.