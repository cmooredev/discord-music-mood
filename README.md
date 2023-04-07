# Music Genre Role Bot

Music Genre Role Bot is a Discord bot that allows users to set and view music genre roles based on YouTube song URLs. The bot uses the Spotify API to determine the genre of a song and then creates and assigns a corresponding role to the user. It also provides the ability to view all users with a specific genre role.

## Features

- **Set Genre Role:** Users can set their genre role based on the genre of a song they provide. The bot determines the genre by using the Spotify API and YouTube-DL.
- **Get Users with Role:** Users can see all members with a specific genre role.

## Slash Commands

The bot uses Discord's slash commands for easy interaction. The following commands are available:

- `/set-genre-role [song_url]`: Set the user's genre role based on the genre of the provided YouTube song URL. The bot will search for the song on Spotify, determine its genre, and create/assign a role to the user based on the genre.
- `/get-users-with-role [genre]`: View all members in the server with the specified genre role. The bot will display an embed listing all users with the role.

## Dependencies

- `discord.py`: Discord API wrapper for Python.
- `spotipy`: Lightweight Python library for the Spotify Web API.
- `yt-dlp`: A powerful command-line program to download videos from YouTube and other video hosting sites.

## Setup

1. Install the required dependencies.
2. Set up the necessary environment variables for the bot, including the Discord bot token, Spotify client ID, and Spotify client secret.
3. Run the bot script.

## Usage

1. Invite the bot to your Discord server.
2. Use the slash commands to interact with the bot.
3. Enjoy setting and viewing genre roles based on your favorite songs!
