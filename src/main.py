from discord.ext import commands
import discord
import random
import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 0000  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

####################################################
# Warm-up

## name
@bot.command(name='name')
async def get_name(ctx):
    author_name = ctx.message.author.name
    response = f"{author_name}"
    await ctx.send(response)

## d6
@bot.command(name='d6')
async def get_d6(ctx):
    response = random.randint(1, 6)
    await ctx.send(response)

## Salut tout le monde
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'Salut tout le monde':
        response = f"Salut tout seul {message.author.mention}"
        await message.channel.send(response)
    await bot.process_commands(message)


####################################################
# Administration

## admin
@bot.command(name='admin')
async def admin(ctx, nickname):
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin is None:
        admin = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())

    member = discord.utils.get(ctx.guild.members, nick=nickname)
    if not member:
        member = discord.utils.get(ctx.guild.members, name=nickname)

    if member:
        await member.add_roles(admin)
        response = f"{nickname} is now an Admin!"
        await ctx.send(response)
    else:
        response = f"Member with nickname {nickname} not found."
        await ctx.send(response)

## ban
@bot.command(name='ban')
async def ban(ctx, nickname, *args):
    member = discord.utils.get(ctx.guild.members, nick=nickname)
    if not member:
        member = discord.utils.get(ctx.guild.members, name=nickname)

    reason = " ".join(args)
    reasons = ["Annoying person", "The member was boring", "It was an alien"]
    if not reason:
        reason = random.choice(reasons)

    response = f"Member {nickname} ban: {reason}"
    await member.ban(reason = reason)
    await ctx.send(response)

## flood
counts = {}

@bot.command(name='flood')
async def flood(ctx, action):
    global flood_on

    if action == 'on':
        flood_on = True
        response = "Flood detection is now enabled."
    elif action == 'off':
        flood_on = False
        response = "Flood detection is now disabled."

    await ctx.send(response)

@bot.event
async def on_message(message):
    if flood_on:
        author = message.author

        if author not in counts or (datetime.datetime.now() - counts[author]['timestamp']).total_seconds() >= (1 * 60):
            counts[author] = {'count': 1, 'timestamp': datetime.datetime.now()}
        else:
            counts[author]['count'] += 1

        if counts[author]['count'] > 5:
            await message.channel.send(f"{author.mention}, you are flooding the chat. Please slow down!")

    await bot.process_commands(message)

flood_on = False


####################################################
# It's all fun and games
## poll
@bot.command(name='poll')
async def poll(ctx, *args):
    question = " ".join(args)
    # Mention @here and post the question
    poll = f"@here {question} ?"
    poll = await ctx.send(poll)

    # Add :thumbsup: and :thumbsdown: reactions to the message

    await poll.add_reaction("👍")
    await poll.add_reaction("👎")

token = "token"
bot.run(token)  # Starts the bot