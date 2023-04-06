# Import necessary modules
import os
import discord
import random
from discord.ext import commands

# Retrieve token from environment variable
TOKEN = os.environ['TOKEN']

# Define Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Create Discord bot instance
client = commands.Bot(command_prefix="!", intents=intents)

# Define the RPGGame class to store game-related variables and methods
class RPGGame:
  
  # Method to calculate heal amount
  def calculate_heal(self):
    return random.randint(80, 110)

  # Constructor method to initialize game variables
  def __init__(self):
    self.user_hp = 300
    self.enemy_hp = 300
    self.attack_damage = {"basic": 20, "advanced": 40, "special": 60}
    self.game_over = False
    self.advanced_available = False
    self.special_available = False
    self.heal_available = False
    self.turn_count = 0

  # Method to calculate enemy damage
  def calculate_enemy_damage(self):
    return random.randint(30, 40)

  # Method to calculate player damage
  def calculate_player_damage(self, attack_type):
    return self.attack_damage[attack_type]

  # Method to check if the game is over
  def is_game_over(self):
    return self.user_hp <= 0 or self.enemy_hp <= 0

  # Method to get the current game status
  def get_game_status(self):
    if self.is_game_over():
      if self.user_hp <= 0:
        return "lost"
      else:
        return "won"
    else:
      return "playing"

  # Method to reset the game
  def reset_game(self):
    self.user_hp = 300
    self.enemy_hp = 300
    self.game_over = False
    self.advanced_available = False
    self.special_available = False
    self.heal_available = False
    self.turn_count = 0

# Create a new instance of the RPGGame class
game = RPGGame()

# Command to handle player attacks
@client.command()
async def attack(ctx, attack_type: str):
  """
  Check the guide for attack information
  """

  # Check if the user entered a valid attack type
  while attack_type not in ["basic", "advanced", "special"]:
    await ctx.send("Invalid attack type! Enter !guide to learn how to play the game")
    return

  # Check if the game is over
  if game.is_game_over():
    await ctx.send("The game is over. Enter !start game to play again")
    return

  # Calculate the damage based on the attack type
  damage = game.calculate_player_damage(attack_type)

  # Check if the selected attack type is available
  if attack_type == "advanced" and not game.advanced_available:
    await ctx.send("Advanced attack not available yet!")
    return

  if attack_type == "special" and not game.special_available:
    await ctx.send("Special attack not available yet!")
    return

  if attack_type == "heal" and not game.heal_available:
    await ctx.send("Heal not available yet!")
    return

  # Calculate the enemy's attack damage and subtract it from the user's health
  enemy_damage = game.calculate_enemy_damage()
  
  # If the enemy's attack damage is less than 33, increase the user's basic attack damage by 5
  enemy_damage = game.calculate_enemy_damage()
  if enemy_damage < 33:
    game.attack_damage["basic"] += 5
    await ctx.send("The enemy's attack was weak! You have capitalized and your basic attack has increased by +5 damage!")
  game.user_hp -= enemy_damage

  # Subtract the damage from the enemy's health
  game.enemy_hp -= damage

  # Send a message with the results of the attack
  await ctx.send(
    f"You dealt {damage} damage to the enemy! The enemy dealt {enemy_damage} damage to you. \n user hp: {game.user_hp} \n enemy hp: {game.enemy_hp}"
  )


  # Update game status
  game.turn_count += 1
  game.advanced_available = game.turn_count % 2 == 0
  game.special_available = game.turn_count % 3 == 0
  game.heal_available = game.turn_count % 3 == 0

  # Check if the game is over
  if game.is_game_over():
    game.game_over = True
    if game.get_game_status() == "lost":
      await ctx.send(
        f"You lost the game!\nThe Enemy is still at {game.enemy_hp} HP! Enter !start game to play again!"
      )
    elif game.get_game_status() == "won":
      await ctx.send(
        f"You have won the game! Your enemy has been slayed while you are still {game.user_hp} HP!"
      )

#heal command
@client.command()
async def heal(ctx):
  """
    Heals you between 80 and 110 hp
    """
  if not game.heal_available:
    await ctx.send("Heal not available yet!")
    return

  # Calculate the heal amount and add it to the user's health
  heal_amount = game.calculate_heal()
  game.user_hp += heal_amount

  # Calculate the enemy's attack damage and subtract it from the user's health
  enemy_damage = game.calculate_enemy_damage()
  game.user_hp -= enemy_damage

  # Send a message with the results of the heal
  await ctx.send(
    f"You healed {heal_amount} HP! The enemy dealt {enemy_damage} damage to you. \n user hp: {game.user_hp} \n enemy hp: {game.enemy_hp}"
  )

#start command
@client.command()
async def start(ctx):
  """
    Starts the game by resetting the player and enemy health.
    """
  #resets user health
  game.user_hp = 300
  game.enemy_hp = 300
  await ctx.send(
    "Game started! Your health has been reset to 300, and the enemy's health has been reset to 300.\n Enter !help for if you are new to the game."
  )

#help command
@client.command()
async def guide(ctx):
  """
    Total Explanation of the game and how to play.
    
    """
  message = """
    Welcome to the game!\n
    To start simply type !start.\n
    There are three types of attacks.\n
    You can use basic, advanced, or special attacks.\n
    Basic attacks are commanded through !attack basic.\n
    Advanced attacks are commanded through !attack advanced.\n
    Speicial attacks are commanded through !attack special.\n
    Basic attacks do 20 damage and are available every turn.\n
    Advanced attacks do 40 damage and are available after two turns.\n
    Special attacks do 60 damage and are available after three turns.\n
    The heal command heals the player for a random amount between 80 and 110 hp and is available after three turns.\n
    The enemy will randomly attack you each turn you take with damage between 30 and 40 hp.
    If the enemy attack goes below 33 your basic attack increases by plus 5 damage.\n
    You win the game by defeating the enemy before your hp reaches 0.\n
    Good luck!
    """
  await ctx.send(message)




client.run(TOKEN)
