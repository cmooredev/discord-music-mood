import discord
from discord import app_commands
from discord.ext import commands
import requests
import yt_dlp  # Updated import
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import DISCORD_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

class MusicRoleBot(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="set-genre-role")
    async def set_genre_role(self, interaction: discord.Interaction, song_url: str) -> None:
        """ /set-genre-role """
        genre = get_genre_from_song_url(spotify, song_url)
        if genre is None:
            await interaction.response.send_message("Failed to extract genre from the provided URL.", ephemeral=True)
            return

        role = await get_or_create_role(interaction.guild, genre)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Role '{genre}' has been added!", ephemeral=True)  # Updated response

    @app_commands.command(name="get-users-with-role")
    async def get_users_with_role(self, interaction: discord.Interaction, genre: str) -> None:
        """ /get-users-with-role """
        role = discord.utils.get(interaction.guild.roles, name=genre)
        if not role:
            await interaction.response.send_message(f"No role with name '{genre}' found.", ephemeral=True)
            return

        members = [member for member in interaction.guild.members if role in member.roles]
        description = "\n".join([f"{member.mention}" for member in members])

        embed = discord.Embed(title=f"Users with '{genre}' role", description=description, color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="sync_commands")
    @commands.is_owner()
    async def sync_commands(self, ctx: commands.Context) -> None:
        await self.bot.tree.sync()
        await ctx.send("Slash commands have been synced globally.")

async def setup(bot: commands.Bot) -> None:
    cog = MusicRoleBot(bot)
    await bot.add_cog(cog)
    await bot.tree.sync()

async def get_or_create_role(guild: discord.Guild, genre: str) -> discord.Role:
    role = discord.utils.get(guild.roles, name=genre)
    if not role:
        role = await guild.create_role(name=genre, reason="Genre role created.")
    return role

def authenticate_spotify(client_id: str, client_secret: str) -> spotipy.Spotify:
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_genre_from_song_url(spotify: spotipy.Spotify, url: str) -> str:
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Updated usage
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        if not video_title:
            return None

        results = spotify.search(q=video_title, type="track", limit=1)
        tracks = results.get("tracks")
        if not tracks:
            return None

        items = tracks.get("items")
        if not items:
            return None

        first_item = items[0]
        artists = first_item.get("artists")
        if not artists:
            return None

        first_artist = artists[0]
        artist_id = first_artist.get("id")
        if not artist_id:
            return None

        artist_info = spotify.artist(artist_id)
        genres = artist_info.get("genres")
        if not genres:
            return None

        primary_genre = genres[0]
        return primary_genre
    except youtube_dl.utils.DownloadError:
        return None

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready.")
    await setup(bot)  # Run the setup function after the bot is ready

spotify = authenticate_spotify(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
bot.run(DISCORD_KEY)