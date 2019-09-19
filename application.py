# bot.py
import os

import asyncio

import discord
from dotenv import load_dotenv

from discord.ext.commands import Bot

from test_python_scrape import ImageScraper
import crawlTweets as tw

import time

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("I'm ready.")
    global target_channel
    target_channel = bot.get_channel(618957085928980492)
    await target_channel.send("I'm ready. Please talk to me! For commands, go to how-to channel.")



@bot.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello! ' +  message.author.name)

    if message.content.startswith("$twitter"):
        channel = message.channel
        tweets = []
        tweets = tw.letscrawl(tweets)
        for tweet in tweets:
            await channel.send(tweet)

    if message.content.startswith('$scrape'):
        start_time = time.time()
        channel = message.channel
        print("received command")
        await channel.send("I received scraping command")
        scraper = ImageScraper()
        print("Scraper is generated")
        await channel.send("Scraper is generated")
        message.content = message.content[8:]
        print(message.content)
        searchKeyword = message.content.split(", ")
        print(searchKeyword)
        lengthOfSearchKeyword = len(searchKeyword)
        num_of_images = int(searchKeyword[lengthOfSearchKeyword-1])
        for keyword in range(lengthOfSearchKeyword-1):
            await channel.send("I'm scraping images of {} for {}!".format(searchKeyword[keyword], message.author.name))
            image_list = scraper.scrape_images(search_image = searchKeyword[keyword], num_of_images = num_of_images)
            print("image scraped")

        await channel.send("Pls be patient. I'm giving you out the images!")
        #await asyncio.sleep(60)

        for i in image_list:
            await channel.send(i)

        elapsed_time = time.time() - start_time
        print("scraping images is done!")
        await channel.send("I finished scraping images!! It took {:.2f} seconds. \n I'm waiting for commands.".format(elapsed_time))



bot.run(bot_token)
