import discord
import praw
import random
import asyncio

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "memebot/1.0")

SUBREDDITS = [
    "memesESP",      
    "SpanishMemes",
    "memesenespanol", 
    "latinoamerica",  
    "memeslatinos"    
]

def get_random_meme_url():
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit_name = random.choice(SUBREDDITS)
    subreddit = reddit.subreddit(subreddit_name)
    posts = [post for post in subreddit.hot(limit=20) if not post.stickied and not post.over_18]
    meme = random.choice(posts)
    return meme.url

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(":meme"):
        try:
            meme_url = await asyncio.to_thread(get_random_meme_url)
            await message.channel.send(meme_url)
        except Exception:
            await message.channel.send("❌ Error al obtener el meme.")

client.run(DISCORD_TOKEN)
