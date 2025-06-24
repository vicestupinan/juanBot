import discord
import praw
import random
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "memebot/1.0")

SUBREDDITS = [
    "memesESP",      
    "SpanishMemes",
    "memesenespanol", 
    "memeslatinos"    
]

def get_random_meme():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit_name = random.choice(SUBREDDITS)
    subreddit = reddit.subreddit(subreddit_name)
    posts = [post for post in subreddit.hot(limit=20) if not post.stickied and not post.over_18]
    meme = random.choice(posts)
    return {
        "title": meme.title,
        "url": meme.url,
        "author": meme.author.name,
        "permalink": f"https://reddit.com{meme.permalink}"
    }

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(":meme"):
        try:
            meme_data = await asyncio.to_thread(get_random_meme)
            embed = discord.Embed(
                title=meme_data["title"],
                url=meme_data["permalink"]
            )
            embed.set_image(url=meme_data["url"])
            embed.set_footer(text=f"Publicado por u/{meme_data['author']}")

            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send("❌ Error al obtener el meme.")
            print(f"Error: {e}")

client.run(DISCORD_TOKEN)
