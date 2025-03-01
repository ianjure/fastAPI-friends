import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Character schema
class Character(BaseModel):
    name: str
    age: int
    favorite_food: str
    quote: str

# Function to save the character as a new row to CSV file
def save_character(name, age, favorite_food):
    file_name = "characters.csv"
    df = pd.read_csv(file_name)
    df.loc[len(df)] = [id, name, age, favorite_food]
    df.to_csv(file_name, index=False)

# Function to save the character's quote as a new row to CSV file
def save_quote(name, quote):
    file_name = "quotes.csv"
    df = pd.read_csv(file_name)
    df.loc[len(df)] = [id, name, quote]
    df.to_csv(file_name, index=False)

# POST: Create a character route
@app.post("/create_character")
async def create_character(data: Character):
    name = data.name
    age = data.age
    favorite_food = data.favorite_food
    quote = data.quote
    save_character(name, age, favorite_food)
    save_quote(name, quote)
    return {
        "msg": "Character Created!",
        "name": name,
        "age": age,
        "favorite_food": favorite_food,
        "quote": quote
    }

# GET: Get all characters route
@app.get("/characters")
def get_characters():
    df = pd.read_csv("characters.csv")
    json_df = df.to_json(orient="records")
    return json.loads(json_df)

# GET: Get a character route
@app.get("/characters/{name}")
async def get_character(name):
    df = pd.read_csv("characters.csv")
    df = df[df["name"].str.contains(name)]
    json_df = df.to_json(orient="records")
    return json.loads(json_df)

# GET: Get a random quote route
@app.get("/quote")
def get_quote():
    df = pd.read_csv("quotes.csv")
    df = df.drop(columns=['name'])
    df = df.sample()
    json_df = df.to_json(orient="records")
    return json.loads(json_df)