import discord
import os
import util
import requests
import json
import random
import pymongo
from pymongo import MongoClient
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

#Setting all intent to True so certain retrieval of data can work
intents = discord.Intents.all()
intents.members = True  # Subscribe to the privileged members intent.

#Private env variables for API/DB access
mongo_user = os.getenv('MONGOUSER')
mongo_pw = os.getenv('MONGOPW')
mongo_string = os.getenv('MONGOSTRING')
mongo_client_string = f"mongodb+srv://{mongo_user}:{mongo_pw}@{mongo_string}"

#Initialize Mongo client and db
cluster = MongoClient(mongo_client_string)
mdb = cluster["Reco_List"]
mdbc = mdb["reco_records"]

#This is the instance of the client
client = commands.Bot(command_prefix='$', intents=intents)

#This is the event that is created to store the function
@client.event
#This event is called when the bot is ready to be used.
async def on_ready():
	#When the on_ready function is called then this is printed to the console.
	print('We have logged in as {0.user}'.format(client))

@client.command()
async def recolist(ctx):
	embedVar = discord.Embed(
	    title="Recommendation List",
	    description=
	    'Find below different media suggested by users! If you would like to recommend something, use the .addreco command. Always begin and end your titles with double quotes like this, "Title"',
	    color=0x00ff00)
	embedVar.add_field(name="Books",
	                   value=util.get_recos('book'),
	                   inline=False)
	embedVar.add_field(name="Movies", 
                     value=util.get_recos('movie'), 
                     inline=False)
	embedVar.add_field(name="Television Series", 
                     value=util.get_recos('television'), 
                     inline=False)
	await ctx.channel.send(embed=embedVar)


@client.command()
async def addreco(ctx, title, medium):
  author = ctx.message.author.id
  post = {"title":title,"medium":medium,"author":author}
  mdbc.insert_one(post)


@client.command()
async def delreco(ctx, title, medium):
  author = ctx.message.author.id
  trgttitle = mdbc.find_one({"title":title, "medium":medium})
  recoauthor = trgttitle["author"]
  if trgttitle == None:
    await ctx.channel.send("We didn't find that reco! Check your spelling!")
  elif trgttitle != None:
    if author == recoauthor:
      await ctx.channel.send("We found it! It should be gone now.")
      mdbc.delete_one(trgttitle)
    else:
      await ctx.channel.send("You didn't post this reco. You can't delete another person's reco.")
  else:
    await ctx.channel.send("Somethin' weird is happening. Try again or contanct an admin.")

@client.command()
async def recorandom(ctx, medium):
  choice = util.get_rand_reco(medium)
  await ctx.channel.send(choice)


#this is what runs the client overall. The token is stored in the .env file.
keep_alive()
client.run(os.getenv('DCTOKEN'))