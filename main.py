import discord
import random
from discord.ext import commands

TOKEN = "MTA4MDk2MDkzOTI1MzMwNTQ2Nw.GGOkWt.NQf-0xy1kFFMoh2Y8sFsGeCEJBvH5vvLd9RyVE"

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = "!" , intents = intents)


#variable#
user_hp = 100
enemy_hp = 200
basic_attack = 20
advanced_attack = 40
special_attack = 60


   def __init__(self, name, hp, max_hp, attack, defense, xp, gold):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.xp = xp
        self.gold = gold

    def fight(self, other):
        defense = min(other.defense, 19) # cap defense value
        chance_to_hit = random.randint(0, 20-defense)
        if chance_to_hit:
            damage = self.attack
        else:
            damage = 0

        other.hp -= damage

        return (self.attack, other.hp <= 0) #(damage, fatal)