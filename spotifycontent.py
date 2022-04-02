import discord 
import requests
import dateutil.parser

from discord.ext import commands

intents=discord.Intents.all()
bot=commands.Bot(command_prefix="::", intents=intents)

@bot.command()
async def help(ctx):
  embed=discord.Embed(
    title="help command",
    description="`help` : **このコマンド**\n\
                 `track (id or mention)` : ユーザーの現在聞いている楽曲のURLを送信\n\
                 `spotify[sp]` : 楽曲の詳細を送信",
    color=0x6dc1d1
    )
  await ctx.send(embed=embed)

@bot.command()
async def track(ctx, user:discord.Member=None):
    if not user:
        user=ctx.author
    
    spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

    if spotify_result is None:
        await ctx.send(f"{user.name} is not listening to SPotify!")
    
    if spotify_result:
        await ctx.send(f"https://open.spotify.com/track/{spotify_result.track_id}")

@bot.command(aliases=["sp"])
async def spotify(ctx, user:discord.Member=None):
    if not user:
        user=ctx.author
    spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

    if spotify_result is None:
        await ctx.send(f"{user.name} is not listening to Spotify!")

    if spotify_result:
        embed=discord.Embed(
            title=f"{spotify_result.title}",
            color=0x6dc1d1
            )
        embed.set_thumbnail(url=spotify_result.album_cover_url)
        embed.add_field(name="Name", value=f"```{spotify_result.title}```")
        artists = spotify_result.artists
        if not artists[0]:
            re_result=spotify_result.artist
        else:
            re_result = ',\n'.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```")
        embed.add_field(name="Album", value=f"```{spotify_result.album}```", inline=False)
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(spotify_result.duration)).strftime('%M:%S')}```")
        embed.add_field(name="URL", value=f"```https://open.spotify.com/track{spotify_result.track_id}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        await ctx.send(embed=embed)

bot.run("")
