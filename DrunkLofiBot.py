# Import necessary modules
import discord
from discord.ext import commands, tasks
from discord import app_commands
from youtube_dl.utils import DownloadError
import yt_dlp
import asyncio
import os
import typing

# Define an empty dictionary for the songs
SONGS = {}

# Define a command for the bot to update the list of all available songs
@tasks.loop(hours=24)
async def update_songs():
    # Run the YTScraper.py script
    os.system("python YTScraper.py")

    # Clear the SONGS dictionary
    SONGS.clear()

    # Read the updated data from output.txt
    with open("output.txt", "r", encoding="utf-8") as f:
        for line in f:
            # Split the line into a title and a URL
            title, url = line.strip().split(": ", 1)
            # Add the title and URL to the SONGS dictionary
            SONGS[title] = url

# This event is triggered before the update_songs task starts
@update_songs.before_loop
async def before_update_songs():
    await bot.wait_until_ready()  # wait until the bot logs in
    await update_songs()  # run the task once immediately

# Read the data from output.txt
with open("output.txt", "r", encoding="utf-8") as f:
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
    # Updates the Lofi Songs list once a day
    update_songs.start()
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
bot.run('MTE4MTExNzk1Mjk1NTc4MTIwMA.GJ-Tol.rBSu8cCZe2wDoRAYyL-PWWl22wA6v05eVvjwME')
