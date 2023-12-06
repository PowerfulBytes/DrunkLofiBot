# Drunk Lofi Discord Music Bot

This is a simple Discord bot that can play music from YouTube in a voice channel. It uses the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library to download and stream audio from YouTube videos. It also reads a list of songs from a text file and allows the user to choose one of them.

## Requirements

To run this bot, you will need:

- Python 3.8 or higher
- discord.py 1.7.3 or higher
- yt-dlp 2021.10.22 or higher
- A Discord bot token
- A text file named output.txt with song titles and URLs in the format: `title: url`

## Usage

To use this bot, follow these steps:

- Install the required libraries using `pip install -r requirements.txt`
- Create a file named `DISCORD_TOKEN.env` and write your bot token in it as `DISCORD_TOKEN=your_token`
- Invite the bot to your server using the OAuth2 URL generator
- Run the bot using `DrunkLofiBot.py`
- In a voice channel, type `/play` to see the list of songs available
- Enjoy the music!

## Commands

The bot has the following commands:

- `/play`: Shows the list of songs available and prompts the user to choose one
- `/stop`: Stops the current song and disconnects the bot from the voice channel

## License

This project is licensed under a Custom License. See the LICENSE file for details.
