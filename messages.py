import discord
import requests
import os
from dotenv import load_dotenv
load_dotenv()


color=0x848587
valorant_endpoint=os.environ.get("VALORANT_ENDPOINT")


def player_stats(player_tag):

    
    data_base=requests.get(f"{valorant_endpoint}/valorant/v1/account/{player_tag[0]}/{player_tag[1]}").json()
    player_region=data_base["data"]["region"]
    data_stats=requests.get(f"{valorant_endpoint}/valorant/v2/mmr/{player_region}/{player_tag[0]}/{player_tag[1]}").json()
    fields_dict={"Account Level" : data_base["data"]["account_level"], "Account Region" : data_base["data"]["region"] ,"Current Elo ": data_stats["data"]["current_data"]["elo"], "Elo change in Last Game" :data_stats["data"]["current_data"]["mmr_change_to_last_game"], "Current Rank" : data_stats["data"]["current_data"]["currenttierpatched"]}
    message_player_data_response=discord.Embed(title="Player Stats",color=color,
    description=f'Here are {data_stats["data"]["name"]} stats')
    for key in fields_dict:
        message_player_data_response.add_field(
            name=key,
            value=fields_dict[key],
            inline=False
        )
    return message_player_data_response


def live_match(player_tag):


     data_base=requests.get(f"{valorant_endpoint}/valorant/v1/live-match/{player_tag[0]}/{player_tag[1]}").json()
     if (data_base["status"]=="200") & (data_base["data"]["current_state"]=="INGAME"):
          fields_dict={"Game Mode":data_base["data"]["gamemode"], "Current State":data_base["data"]["current_state"],"Map":data_base["data"]["map"],"Ally Team Score":str(data_base["data"]["score_ally_team"]),"Enemy Team Score":str(data_base["data"]["score_enemy_team"])}     
          message_player_data_response=discord.Embed(title="Player Stats",color=color,
          description=f'Here are Live Game Stats of {player_tag[0]}')
          for key in fields_dict:
            print(key,fields_dict[key])
            message_player_data_response.add_field(
                name=key,
                value=fields_dict[key],
                inline=False
            )
          return message_player_data_response




     if (data_base["status"]=="200") & (data_base["data"]["current_state"]=="MENUS"):

          fields_dict={"Game Mode Selected":data_base["data"]["current_selected_gamemode"], "Current State":data_base["data"]["current_state"],"Party Size":data_base["data"]["party_size"]}     
          message_player_data_response=discord.Embed(title="Player Stats",color=color,
          description=f'Here are Live Game Stats of {player_tag[0]}')
          for key in fields_dict:
            print(key,fields_dict[key])
            message_player_data_response.add_field(
                name=key,
                value=fields_dict[key],
                inline=False
            )
          return message_player_data_response