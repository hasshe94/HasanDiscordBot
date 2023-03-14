import os
import discord
import random
from discord.ext import commands

TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

# define the RPGGame class to store game-related variables and methods
class RPGGame:
    def __init__(self):
        self.user_hp = 100
        self.enemy_hp = 200
        self.basic_attack = 20
        self.advanced_attack = 40
        self.special_attack = 60
        self.game_over = False
        self.advanced_available = False
        self.special_available = False
        self.turn_count = 0

    def calculate_enemy_damage(self):
        return random.randint(20, 30)

    def calculate_player_damage(self, attack_type):
        if attack_type == "basic":
            return self.basic_attack
        elif attack_type == "advanced":
            return self.advanced_attack
        elif attack_type == "special":
            return self.special_attack

    def is_game_over(self):
        return self.user_hp <= 0 or self.enemy_hp <= 0

    def get_game_status(self):
        if self.is_game_over():
            if self.user_hp <= 0:
                return "lost"
            else:
                return "won"
        else:
            return "playing"

    def reset_game(self):
        self.user_hp = 100
        self.enemy_hp = 200
        self.game_over = False
        self.advanced_available = False
        self.special_available = False
        self.turn_count = 0

game = RPGGame()

@client.command()
async def attack(ctx, attack_type : str):
    """
    Check the guide for attack information
    """
    # Check if the user entered a valid attack type
    if attack_type not in ["basic", "advanced", "special"]:
        await ctx.send("Invalid attack type! Enter !guide to learn how to play the game")
        return

    # Calculate the damage based on the attack type
    damage = game.calculate_player_damage(attack_type)

    if attack_type == "advanced" and not game.advanced_available:
        await ctx.send("Advanced attack not available yet!")
        return

    if attack_type == "special" and not game.special_available:
        await ctx.send("Special attack not available yet!")
        return

    # Calculate the enemy's attack damage and subtract it from the user's health
    enemy_damage = game.calculate_enemy_damage()
    game.user_hp -= enemy_damage

    # Subtract the damage from the enemy's health
    game.enemy_hp -= damage

    # Send a message with the results of the attack
    await ctx.send(f"You dealt {damage} damage to the enemy! The enemy dealt {enemy_damage} damage to you. \n user hp: {game.user_hp} \n enemy hp: {game.enemy_hp}")

    # Update game status
    game.turn_count += 1
    game.advanced_available = game.turn_count % 2 == 0
    game.special_available = game.turn_count % 4 == 0

    # Check if the game is over
    if game.is_game_over():
        game.game_over = True
        if game.get_game_status() == "lost":
            await ctx.send(f"You lost the game!\nThe Enemy is still at {game.enemy_hp}. Enter !start game to play again")



#start command
@client.command()
async def start(ctx):
    """
    Starts the game by resetting the player and enemy health.
    """
    game.user_hp = 100
    game.enemy_hp = 200
    await ctx.send("Game started. Your health has been reset to 100, and the enemy's health has been reset to 200.\n Enter !help for if you are new to the game.")


client.run(TOKEN)