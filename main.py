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
  def calculate_heal(self):
    return random.randint(40, 50)

  def __init__(self):
    self.user_hp = 300
    self.enemy_hp = 300
    self.attack_damage = {"basic": 20, "advanced": 40, "special": 60}
    self.game_over = False
    self.advanced_available = False
    self.special_available = False
    self.heal_available = False
    self.turn_count = 0

  def calculate_enemy_damage(self):
    return random.randint(20, 40)

  def calculate_player_damage(self, attack_type):
    return self.attack_damage[attack_type]

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
    self.heal_available = False
    self.turn_count = 0

game = RPGGame()

@client.command()
async def attack(ctx, attack_type: str):
  """
    Check the guide for attack information
    """
  # Check if the user entered a valid attack type
  if attack_type not in ["basic", "advanced", "special"]:
    await ctx.send(
      "Invalid attack type! Enter !guide to learn how to play the game")
    return

  # Calculate the damage based on the attack type
  damage = game.calculate_player_damage(attack_type)

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
  game.special_available = game.turn_count % 4 == 0
  game.heal_available = game.turn_count % 3 == 0

@client.command(name="start")
async def start_game(ctx):
  game = Game()
  await ctx.send("A new game has started! Your health is 100. Enemy's health is 100.")

  # run the game logic in a while loop until the game is over
  while not game.game_over:
    # prompt the user to choose an attack
    await ctx.send("Choose your attack: basic, advanced, special, or heal")

    # wait for the user's response
    attack_type = await client.wait_for("message")

    # simulate the attack
    await attack(ctx, attack_type.content)
    
    # check if the user has lost the game
    if game.get_game_status() == "lost":
      await ctx.send(
        f"You lost the game!\nThe Enemy is still at {game.enemy_hp}. Enter !start game to play again"
      )
      break

#start command
@client.command()
async def start(ctx):
  """
    Starts the game by resetting the player and enemy health.
    """
  game.user_hp = 100
  game.enemy_hp = 200
  await ctx.send(
    "Game started. Your health has been reset to 100, and the enemy's health has been reset to 200.\n Enter !help for if you are new to the game."
  )

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
    Basic attacks do 20 damage.\n
    Advanced attacks do 40 damage and are available every second turn.\n
    Special attacks do 60 damage and are available every fourth turn.\n
    The heal command heals the player for a random amount between 40 and 50 hp and is available every 3rd turn.\n
    The enemy will randomly attack you each turn you take with damage between 20 and 30 hp. You win the game by defeating the enemy before your hp reaches 0.\n
    Good luck!
    """
  await ctx.send(message)

#heal
@client.command()
async def heal(ctx):
    """
    Heals you between 40 and 50 hp
    """
    heal_amount = game.calculate_heal()
    game.user_hp += heal_amount
    enemy_damage = game.calculate_enemy_damage()
    game.user_hp -= enemy_damage
    await ctx.send(f"You healed yourself by {heal_amount}! The enemy dealt {enemy_damage} damage to you. \n user hp: {game.user_hp} \n enemy hp: {game.enemy_hp}")

client.run(TOKEN)