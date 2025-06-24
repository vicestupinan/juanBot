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
    url = meme.url
    is_image = url.endswith((".jpg", ".png", ".gif", ".webp", ".jpeg", ".gifv"))
    return {
        "title": meme.title,
        "url": url,
        "author": meme.author.name,
        "permalink": f"https://reddit.com{meme.permalink}",
        "is_image": is_image
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

            if meme_data["is_image"]:
                embed = discord.Embed(
                    title=meme_data["title"],
                    url=meme_data["permalink"]
                )
                embed.set_image(url=meme_data["url"])
                embed.set_footer(text=f"Publicado por u/{meme_data['author']}")
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(
                    f"**{meme_data['title']}**\n {meme_data['url']} \n Publicado por u/{meme_data['author']}"
                )
        except Exception:
            await message.channel.send("❌ Error al obtener el meme.")

client.run(DISCORD_TOKEN)
