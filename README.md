# DrunkLofiBot

"DrunkLofiBot.py is a Discord bot script that plays lo-fi music in a Discord server. The bot uses the discord.py library to interact with Discord's API and the yt_dlp library to download and play audio from YouTube.

The bot maintains a dictionary of song titles and URLs, which it updates by running a separate script, YTScraper.py. The bot reads the updated song data from an output.txt file and stores it in the dictionary for easy access.

The bot includes a custom audio player class, YTDLSource, which uses discord.py's PCM volume transformer to control the volume of the played audio. The class includes a method to download and play audio from a YouTube URL.

The bot supports commands to play and stop songs. The 'play' command includes an autocomplete feature that suggests song titles based on the user's input. The bot can connect to a voice channel that the user is in and play a song from the dictionary. If the bot is already connected to a voice channel, it disconnects before connecting to a new one.

The bot also includes a 'stop' command that stops the current song and disconnects the bot from the voice channel.

The bot uses a command prefix and has all intents enabled. It syncs its commands with Discord when it establishes a connection. The bot is started using a bot token."
