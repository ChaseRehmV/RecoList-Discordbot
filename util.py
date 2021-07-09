import os
import pymongo
import random
from pymongo import MongoClient

# private env variables for API/DB access. If using replit, you will need to create "secrets" in your replit project for each of the variables preceded by 'os.getenv'. The mongo user, password, and string you will get from your mongo account. The mongo string is your connection string for your mongo database. 
mongo_user = os.getenv('MONGOUSER')
mongo_pw = os.getenv('MONGOPW')
mongo_string = os.getenv('MONGOSTRING')
mongo_client_string = f"mongodb+srv://{mongo_user}:{mongo_pw}@{mongo_string}"

# initialize Mongo client and db
cluster = MongoClient(mongo_client_string)
mdb = cluster[<"your mongo cluster>"]
mdbc = mdb[<"your mongo collection">]

# function used when retrieving and displaying all recommendations
def get_recos(medium):
  """Finds all recommendation titles with the given medium"""
  matches = mdbc.find({"medium":medium})
  title_list = []
  for match in matches:
    title = match.get('title')
    title_list.append(title)
    s = ', '.join(title_list)
  return s

# function used when retrieving a random recommendation from given medium
def get_rand_reco(medium):
  """Grabs a random recommendation from the given medium"""
  matches = mdbc.find({"medium":medium})
  title_list = []
  for match in matches:
    title = match.get('title')
    title_list.append(title)
  choice = random.choice(title_list)
  return choice
