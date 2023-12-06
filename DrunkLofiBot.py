# Import necessary modules
import discord
from discord.ext import commands
from discord import app_commands
from youtube_dl.utils import DownloadError
import yt_dlp
import asyncio
import typing
from dotenv import dotenv_values

# Load the environment variables from the .env file
config = dotenv_values("DISCORD_TOKEN.env")
token = config["DISCORD_TOKEN"]

# Define an empty dictionary for the songs
SONGS = {}

# Read the data from output.txt
with open("24_7 Lofi", "r", encoding="utf-8") as f:
    for line in f:
        # Split the line into a title and a URL
        title, url = line.strip().split(": ", 1)
        # Add the title and URL to the SONGS dictionary
        SONGS[title] = url

# Define a class for playing audio from YouTube
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    # Class method to download and play audio from a YouTube URL
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        try:
            # Download the audio from the YouTube URL
            data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL({'format': 'bestaudio'}).extract_info(url, download=not stream))
            # Return an instance of the class with the downloaded audio
            return cls(discord.FFmpegPCMAudio(data['url']), data=data)
        except DownloadError:
            # If there's an error downloading the audio, print a message and skip the song
            print("Error downloading song, skipping...")

# Create a bot instance with a command prefix and all intents enabled
bot = commands.Bot(command_prefix="!",
                   intents=discord.Intents.all())

# Define a command for the bot to play a song
@bot.tree.command(name="play")
async def play(interaction: discord.Interaction, song: str):
    """
    Play a song in the voice channel.

    Parameters:
    - interaction (discord.Interaction): The interaction object representing the user's command.
    - song (str): The name of the song to be played.

    Returns:
    None
    """
    # Get the URL of the song from the SONGS dictionary
    url = SONGS[song]
    # Get the voice channel that the user is in
    voice_channel = interaction.user.voice.channel
    channel = None
    # If the bot is already connected to a voice channel, disconnect it
    if bot.voice_clients:
        await bot.voice_clients[0].disconnect()

    # If the user is in a voice channel, connect the bot to it and play the song
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        vc.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    else:
        # If the user is not in a voice channel, send a message to inform them
        await interaction.response.send_message(content=str(interaction.user) + "is not in a channel.")
    # Send a message to inform the user that the bot has connected to the voice channel
    await interaction.response.send_message(content='Bot is connected to ' + channel)

# Define an autocomplete function for the 'song' option of the 'play' command
@play.autocomplete("song")
async def play_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    """
    Autocomplete function for the 'song' option of the 'play' command.

    Parameters:
    - interaction (discord.Interaction): The interaction object representing the user's command.
    - current (str): The current input value for the 'song' option.

    Returns:
    typing.List[app_commands.Choice[str]]: The autocomplete choices for the 'song' option.
    """
    # Initialize an empty list for the data
    data = []

    # For each song in the SONGS dictionary
    for song_choice in SONGS.keys():
        # If the data list already has 20 songs, break the loop
        if len(data) >= 20:
            break

        # If the current song matches the user's choice, add it to the data list
        if current.lower() in song_choice.lower():
            data.append(app_commands.Choice(name=song_choice, value=song_choice))
    # Return the autocomplete choices
    return data

# Define a command for the bot to stop playing a song
@bot.tree.command(name="stop")
async def stop(interaction: discord.Interaction):
    """
    Stop playing the current song.

    Parameters:
    - interaction (discord.Interaction): The interaction object representing the user's command.

    Returns:
    None
    """
    # Get the voice client for the current guild
    voice_client = interaction.guild.voice_client
    # If the voice client is playing a song, stop it and send a message to inform the user
    if voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message(content='Stopping...')
    # Disconnect the voice client from the voice channel
    await voice_client.disconnect()

# This event is triggered when the bot has established a connection with Discord
@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready.

    Returns:
    None
    """
    # Print a message to the console to indicate that the bot is ready
    print("Bot is Up and Ready!")
    try:
        # Sync the bot's commands with Discord
        synced = await bot.tree.sync()
        # Print a message to the console to indicate how many commands were synced
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        # If an error occurs while syncing commands, print the error message to the console
        print(f"Error syncing commands: {e}")

# Start the bot using your bot token
bot.run(token)

