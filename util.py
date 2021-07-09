import os
import pymongo
import random
from pymongo import MongoClient

#Private env variables for API/DB access
mongo_user = os.getenv('MONGOUSER')
mongo_pw = os.getenv('MONGOPW')
mongo_string = os.getenv('MONGOSTRING')
mongo_client_string = f"mongodb+srv://{mongo_user}:{mongo_pw}@{mongo_string}"

#Initialize Mongo client and db
cluster = MongoClient(mongo_client_string)
mdb = cluster["Reco_List"]
mdbc = mdb["reco_records"]

def get_recos(medium):
  """Finds all recommendation titles with the given medium"""
  matches = mdbc.find({"medium":medium})
  title_list = []
  for match in matches:
    title = match.get('title')
    title_list.append(title)
    s = ', '.join(title_list)
  return s

def get_rand_reco(medium):
  """Grabs a random recommendation from the given medium"""
  matches = mdbc.find({"medium":medium})
  title_list = []
  for match in matches:
    title = match.get('title')
    title_list.append(title)
  choice = random.choice(title_list)
  return choice
