import discord
import random
from discord.ext import commands

TOKEN = "MTA4MDk2MDkzOTI1MzMwNTQ2Nw.GP4Q82.AXcL6YsznKuDJGjv2J4LOskOj72jXlY3-PZxZ4"

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

user_hp = 100
enemy_hp = 200
basic_attack = 20
advanced_attack = 40
special_attack = 60

@client.command()
async def attack(ctx, attack_type):
    global user_hp
    global enemy_hp

    # Check if the user entered a valid attack type
    if attack_type not in ["basic", "advanced", "special"]:
        await ctx.send("Invalid attack type!")
        return

    # Calculate the damage based on the attack type
    if attack_type == "basic":
        damage = basic_attack
    elif attack_type == "advanced":
        if ctx.command.called_count % 2 == 0:
            damage = advanced_attack
        else:
            await ctx.send("Advanced attack not available yet!")
            return
    elif attack_type == "special":
        if ctx.command.called_count % 4 == 0:
            damage = special_attack
        else:
            await ctx.send("Special attack not available yet!")
            return

    # Calculate the enemy's attack damage and subtract it from the user's health
    enemy_damage = random.randint(30, 60)
    user_hp -= enemy_damage

    # Subtract the damage from the enemy's health
    enemy_hp -= damage

    # Send a message with the results of the attack
    await ctx.send(f"You dealt {damage} damage to the enemy! The enemy dealt {enemy_damage} damage to you. \n user hp: {user_hp} \n enemy hp: {enemy_hp}")

    # Check if the game is over
    if user_hp <= 0:
        await ctx.send("You lost the game!")
        quit()
    elif enemy_hp <= 0:
        await ctx.send("You won the game!")
        quit()


@client.command()
async def guide(ctx):
    """
    Shows a help message with instructions on how to play the game.
    """
    message = """
    Welcome to the game!
    Use the !attack command to attack the enemy.
    You can use basic, advanced, or special attacks.
    Basic attacks do 20 damage.
    Advanced attacks do 40 damage and are available every other turn.
    Special attacks do 60 damage and are available every fourth turn.
    The enemy will randomly attack you each turn.
    You win the game by defeating the enemy before your health reaches 0.
    Good luck!
    """
    await ctx.send(message)

@client.command()
async def start(ctx):
    """
    Starts the game by resetting the player and enemy health.
    """
    global user_hp
    global enemy_hp
    user_hp = 100
    enemy_hp = 200
    await ctx.send("Game started. Your health has been reset to 100, and the enemy's health has been reset to 200.")

client.run(TOKEN)
