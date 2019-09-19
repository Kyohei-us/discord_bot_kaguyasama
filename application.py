# bot.py
import os

import asyncio

import discord
from dotenv import load_dotenv

from discord.ext.commands import Bot

from test_python_scrape import ImageScraper
import crawlTweets as tw

from bs4 import BeautifulSoup

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
        thinkReply = message.content[7:]
        if thinkReply.startswith('hello') or thinkReply.startswith('Hello'):
            await channel.send('Hello {}'.format(message.author.name))
        else:
            await channel.send("What's up {}?".format(message.author.name))

    if message.content.startswith("$twitterS"):
        channel = message.channel
        message.content = message.content[10:]
        tweets = []
        tweets = tw.letscrawl(tweets, message.content)
        for tweet in tweets:
            await channel.send(tweet)
        await channel.send("Twitter Search Finished!")

    if message.content.startswith("$twitterL"):
        channel = message.channel
        tweets = []
        tweets = tw.seeLists(tweets)
        for tweet in tweets:
            await channel.send(tweet)
        await channel.send("Twitter List is all!")

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
            beforeElapsed = time.time()
            await channel.send("I'm scraping images of {} for {}!".format(searchKeyword[keyword], message.author.name))
            selectSoup = scraper.scrape_images(search_image = searchKeyword[keyword], num_of_images = num_of_images)
            numberForScrapeloop = num_of_images
            loopingNth = 0
            counter = 0
            while numberForScrapeloop > 0:
                scraped_image = scraper.sliceImageList(selectSoup, loopingNth)
                while scraped_image == "#" or scraped_image.startswith('https://support.google.com/legal/answer/3463239?'):
                    loopingNth = loopingNth + 1
                    scraped_image = scraper.sliceImageList(selectSoup, loopingNth)
                await channel.send(scraped_image)
                await channel.send("{} more image(s) are coming right now!".format(num_of_images - 1 - counter))
                counter = counter + 1
                loopingNth = loopingNth + 1
                numberForScrapeloop = numberForScrapeloop - 1
            print("image scraped")
            afterElapsed = time.time() - beforeElapsed
            await channel.send("It took {:.2f} seconds.".format(afterElapsed))

        #await asyncio.sleep(60)


        elapsed_time = time.time() - start_time
        print("scraping images is done!")
        await channel.send("I finished scraping images!! It took {:.2f} seconds. \n I'm waiting for commands.".format(elapsed_time))



bot.run(bot_token)
