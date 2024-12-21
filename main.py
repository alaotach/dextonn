import os
import uuid
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from flask import Flask, jsonify, request
import time
import threading
import motor.motor_asyncio
from bson.objectid import ObjectId

# MongoDB Connection
MONGODB_URI = os.environ.get("mongodb+srv://aryan:aryan@dextton.ue89v.mongodb.net/?retryWrites=true&w=majority&appName=dextton")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client.dextton
keys_collection = db.keys

app = Flask(__name__)

latest_text = ""
latest_timestamp = ""

@app.route("/api")
async def index():
    apikey = request.args.get("apikey")
    if not apikey:
        return "Missing API key", 401
        
    key_doc = await keys_collection.find_one({"api_key": apikey})
    if not key_doc:
        return "Invalid API key", 403

    return jsonify({"text": latest_text, "timestamp": latest_timestamp})

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents)

@bot.slash_command(description="Create or show your API key")
async def key(interaction: Interaction):
    user_id = str(interaction.user.id)
    key_doc = await keys_collection.find_one({"user_id": user_id})
    
    if key_doc:
        await interaction.response.send_message(f"Your API key: {key_doc['api_key']}", ephemeral=True)
    else:
        new_key = str(uuid.uuid4())
        await keys_collection.insert_one({
            "user_id": user_id,
            "api_key": new_key,
            "created_at": int(time.time())
        })
        await interaction.response.send_message(f"New API key created: {new_key}", ephemeral=True)

@bot.slash_command(description="Regenerate your API key")
async def regen_key(interaction: Interaction):
    user_id = str(interaction.user.id)
    key_doc = await keys_collection.find_one({"user_id": user_id})
    
    if key_doc:
        new_key = str(uuid.uuid4())
        await keys_collection.update_one(
            {"user_id": user_id},
            {"$set": {"api_key": new_key}}
        )
        await interaction.response.send_message(f"API key regenerated: {new_key}", ephemeral=True)
    else:
        await interaction.response.send_message("No API key found. Use /key to create one.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    global latest_text, latest_timestamp
    print(message)
    # if message.author.bot:
    #     return
    # Target channel ID
    if message.channel.id == 1316677449928544318:
        print('new message received!')
        latest_text = message.content
        print(f"Text: {latest_text}")
        latest_timestamp = int(time.time())
    await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
    await keys_collection.delete_one({"user_id": str(member.id)})

def run_bot():
    bot.run(os.environ["MTMxMzk5NTQ0MjYyMjU2NjQ1MA.GW9HxL.VEEgemw-SxHEeVXPbD_ey-yOBFV626tjbzXFUw"])

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=6969)
