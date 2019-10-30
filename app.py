# bot.py
import os
import asyncio
import discord
#from dotenv import load_dotenv
from discord.ext.commands import Bot
from test_python_scrape import ImageScraper
import crawlTweets as tw
from bs4 import BeautifulSoup
import time
import datetime
import pytz

#load_dotenv()
#bot_token = os.getenv('BOT_TOKEN')
bot = Bot(command_prefix='!')
#str(os.environ.get('GOOGLE_CHROME_BIN')) + str(os.environ.get('CHROMEDRIVER_PATH'))

@bot.event
async def on_ready():
    print("I'm ready.")
    global target_channel
    target_channel = bot.get_channel(618957085928980492)
    await target_channel.send("I'm ready. Please talk to me! For commands, go to how-to channel.")

@bot.command(name='test_command')
async def test(ctx, *, arg):
    await ctx.send(arg + ' : is your message')

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = reaction.message.channel
    await channel.send(message.content + " : This message has a reaction added right now.")
    if reaction.emoji == '\U0001F440':
        if user.name == 'discord_bot_1':
            time.sleep(0.001)
        else:
            await channel.send(message.content)

# @bot.event
# async def on_raw_reaction_add(payload):
#     id = message_id
#     channel = bot.get_channel(channel_id)
#     try:
#         msg = await channel.get_message(id)
#     except NotFound:
#         continue

@bot.command(name='twitterL')
async def fetch_twitter_list(ctx, *args):
    channel = ctx.message.channel
    tweets = []
    if len(args) > 0:
        count = int(args[0])
        tweets = tw.seeLists(tweets, count)
    else:
        tweets = tw.seeLists(tweets)
    for tweet in tweets:
        await channel.send(tweet)
    await channel.send("Twitter List is all!")

@bot.command(name='greet')
async def greet_my_bot(ctx, *, arg):
    channel = ctx.message.channel
    message = ctx.message
    thinkReply = message.content.split(" ")
    if len(thinkReply) > 1:
        if thinkReply[1].lower() == 'hello':
            await channel.send('Hello {}'.format(message.author.name))
        else:
            await channel.send("What's up {}? How can help ya?".format(message.author.name))
    else:
        await channel.send("Do you not wanna greet me? Come on! lol")

@bot.command(name='addrole')
async def addrole(ctx):
    guild = ctx.message.guild
    role = discord.utils.get(guild.roles, name="admin")
    try:
        await ctx.message.author.add_roles(role)
    except Exception as e:
        print(e)
        await ctx.message.channel.send("You failed to add role im sorry.")
    # for i in ctx.message.author.roles:
    #     await ctx.message.channel.send("Your roles are {}".format(i))

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name="aggin")
    try:
        await member.add_roles(role)
    except Exception as e:
        print(e)
        channel = bot.get_channel(618957085928980492)
        await channel.send("You failed to add role im sorry.")

@bot.event
async def on_message_delete(message):
    #log to logs channel
    channel = bot.get_channel(637198455978065940)

    name_of_channel_message_was_in = message.channel.name

    try:
        imageAttached = message.attachment[0].url
    except Exception as e:
        print(e)
        await channel.send(imageAttached)

    #fetching current time in PST
    now = datetime.datetime.utcnow()
    utc_time = pytz.utc.localize(now)
    timezone = utc_time.astimezone(pytz.timezone("America/Los_Angeles"))
    #formatting time
    timelog = timezone.strftime("%Y,%B,%d,%a,%X")
    await channel.send("{} : Sent by {} and the message deleted is : {} : This message was sent in following channel : {}".format(timelog, message.author.name, message.content, name_of_channel_message_was_in))


@bot.command(name='twitterS')
async def search_on_twitter(ctx, *, arg):
    channel = ctx.message.channel
    extractCountList = arg.split(',')
    extractKeywordList = extractCountList[0].split(' ')
    tweets = []
    if len(extractCountList) > 1:
        tweets = tw.letscrawl(tweets, extractKeywordList[0], count = int(extractCountList[1]))
    else:
        tweets = tw.letscrawl(tweets, extractKeywordList[0])

    for tweet in tweets:
        await channel.send(tweet)
    await channel.send("Twitter Search Finished!")

@bot.event
async def on_typing(channel, user, when):
    now = when.utcnow()
    utc_time = pytz.utc.localize(now)
    timezone = utc_time.astimezone(pytz.timezone("America/Los_Angeles"))
    #formatting time
    timelog = timezone.strftime("%Y,%B,%d,%a,%X")
    await channel.send("{} is typing at {}".format(user.name, timelog))


@bot.event
async def on_message(message):
    if message.author.name != 'discord_bot_1' or "reaction added right now" not in message.content:
        emoji = '\U0001F440'
        await message.add_reaction(emoji)
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
                if num_of_images - 1 - counter != 0:
                    await channel.send("{} more image(s) are coming right now!".format(num_of_images - 1 - counter))
                else:
                    await channel.send("Image scraping finished.")
                counter = counter + 1
                loopingNth = loopingNth + 1
                numberForScrapeloop = numberForScrapeloop - 1
            print("image scrape done")
            afterElapsed = time.time() - beforeElapsed
            await channel.send("It took {:.2f} seconds to scrape images of {}.".format(afterElapsed, searchKeyword[keyword]))

        #await asyncio.sleep(60)


        elapsed_time = time.time() - start_time
        print("scraping images is done!")
        await channel.send("""I finished scraping all the images!! It took {:.2f} seconds.
Now I'm waiting for commands.""".format(elapsed_time))

        #await bot.process_commands(message)




    await bot.process_commands(message)

bot.run(os.environ.get('BOT_TOKEN'))
