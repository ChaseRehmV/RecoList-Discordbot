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

# setting all intent to True so certain retrieval of data can work
intents = discord.Intents.all()
# subscribe to the privileged members intent.
intents.members = True

# private env variables for API/DB access. If using replit, you will need to create "secrets" in your replit project for each of the variables preceded by 'os.getenv'. The mongo user, password, and string you will get from your mongo account. The mongo string is your connection string for your mongo database. 
mongo_user = os.getenv('MONGOUSER')
mongo_pw = os.getenv('MONGOPW')
mongo_string = os.getenv('MONGOSTRING')
mongo_client_string = f"mongodb+srv://{mongo_user}:{mongo_pw}@{mongo_string}"

# initialize Mongo client and db
cluster = MongoClient(mongo_client_string)
mdb = cluster[<"your mongo cluster>"]
mdbc = mdb[<"your mongo collection">]

# instance of the client
client = commands.Bot(command_prefix='reco:', intents=intents)

# event that is created to store the function
@client.event
# called when the bot is ready to be used.
async def on_ready():
	# when the on_ready function is called then this is printed to the console
	print('We have logged in as {0.user}'.format(client))

# command for displaying all recommendations. more recommendation types can be added by copy/pasting the embedVar and then editing the <reco type>.
@client.command()
async def recolist(ctx):
	embedVar = discord.Embed(
	    title="Recommendation List",
	    description=
	    'Find below different media suggested by users! If you would like to recommend something, use the .addreco command. Always begin and end your titles with double quotes like this, "Title", then follow that with a space and then your reco type',
	    color=0x00ff00)
	embedVar.add_field(name="<reco type">,
	                   value=util.get_recos('<reco type>'),
	                   inline=False)
	embedVar.add_field(name="<reco type>", 
                     value=util.get_recos('<reco type>'), 
                     inline=False)
	embedVar.add_field(name="<reco type>", 
                     value=util.get_recos('<reco type>'), 
                     inline=False)
	await ctx.channel.send(embed=embedVar)

# command for adding a reco. example: < reco:addreco "Movie Title" movie >
@client.command()
async def addreco(ctx, title, medium):
  author = ctx.message.author.id
  post = {"title":title,"medium":medium,"author":author}
  mdbc.insert_one(post)

# command for deleting a reco. recos can only be deleted by the user that added them.
# example: < reco:delreco "Movie Title" movie >
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
    await ctx.channel.send("Something weird is happening. Try again or contanct an admin.")

# command for choosing a random recommendation from a given recommendation type.
# example: < reco:recorandom movie >
@client.command()
async def recorandom(ctx, medium):
  choice = util.get_rand_reco(medium)
  await ctx.channel.send(choice)


# runs the bot. the token is stored in your replit secrets, similar to prior mongo variables.
keep_alive()
client.run(os.getenv('DCTOKEN'))