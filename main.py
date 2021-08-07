import discord
import os
from discord import embeds
import requests
from messages import *
from dotenv import load_dotenv
load_dotenv()



color=0x848587
#Prefix 
greet_prefix="&hello"
help_prefix="&help"
player_stats_prefix="&player-"
live_match_prefix="&live-"
leaderboard_prefix="&top-"

#Bot tokens and Valorant API Endpoint
bot_token=os.environ.get("BOT_TOKEN")
valorant_endpoint=os.environ.get("VALORANT_ENDPOINT")

client=discord.Client()

@client.event
async def on_ready():
    print(f"Our Bot has been logged in {client.user}")
    


#main function----->Interaction with bot
@client.event
async def on_message(message):
    if message.author==client.user:
        return

        
# Simple Greeting---->Bot will respond with Hello if user inputs greeting prefix
    if message.content.startswith(greet_prefix):
        message_greet=discord.Embed(title="𝘉𝘰𝘯𝘫𝘰𝘶𝘳",color=color,description=f"Hello {message.author.mention}")
        await message.channel.send(embed=message_greet)



# Player Stats----->using player stats endpoint to generate data
    if message.content.startswith(player_stats_prefix):
        print("this running")
        player_tag=message.content.replace(player_stats_prefix,'').split("#")
        try:
            message_player_data_response=player_stats(player_tag)
            await message.channel.send(embed=message_player_data_response)
        except(KeyError):
            await message.channel.send("No user Found 1 ")


    if message.content.startswith("&live-"):
        print("this running 1")
        player_tag_live=message.content.replace(live_match_prefix,'').split('#')
        # try:
        print("inside try")
        message_player_data_response=live_match(player_tag_live)
        await message.channel.send(embed=message_player_data_response)
            
        # except(KeyError):
        #     await message.channel.send("No user Found 2")        

            

    



client.run(bot_token)