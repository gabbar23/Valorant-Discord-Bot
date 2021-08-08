import discord
import os
from discord import embeds
from discord.utils import find
import requests
from messages import *
from dotenv import load_dotenv
load_dotenv()



color=0xF44656
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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Valorant'))
    
    



# @client.event
# async def on_guild_join(guild):
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             join_message=join()
#             await channel.send(embed=join_message)
#         break


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == guild.system_channel.name,  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        join_message=join()
        await general.send(embed=join_message)



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
        player_tag=message.content.replace(player_stats_prefix,'').split("#")
        try:
            message_player_data_response=player_stats(player_tag)
            await message.channel.send(embed=message_player_data_response)
        except(KeyError):
            await message.channel.send("No user Found ")

#Live Game Stats-------> using live game endpoint to generate data
    if message.content.startswith(live_match_prefix):
        player_tag_live=message.content.replace(live_match_prefix,'').split('#')
        message_player_data_response=live_match(player_tag_live)
        await message.channel.send(embed=message_player_data_response)

#Top Players------> using leaderboard eendpoint to generate data with region provided
    if message.content.startswith(leaderboard_prefix):
        region=message.content.replace(leaderboard_prefix,'')
        message_player_data_response=leaderboard(region)
        await message.channel.send(embed=message_player_data_response)        
                 

    if message.content.startswith(help_prefix):
        message_player_data_response=help()
        await message.channel.send(embed=message_player_data_response)    

    



client.run(bot_token)