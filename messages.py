import discord
from discord import message
from discord.errors import HTTPException
import requests
import os
from dotenv import load_dotenv
load_dotenv()


color=0xF44656
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
    try:

        data_base=requests.get(f"{valorant_endpoint}/valorant/v1/live-match/{player_tag[0]}/{player_tag[1]}").json()

        #rasing exception manually  because of the bad api response :{   
        if not data_base["data"]["gamemode"]:
            raise Exception("Manual Exception")

    #Ingame
        fields_dict1={"Game Mode":data_base["data"]["gamemode"], "Current State":data_base["data"]["current_state"],"Map":data_base["data"]["map"],"Ally Team Score":str(data_base["data"]["score_ally_team"]),"Enemy Team Score":str(data_base["data"]["score_enemy_team"])}     
    except(KeyError):
        try:
        #Menu
            fields_dict2={"Game Mode Selected":data_base["data"]["current_selected_gamemode"], "Current State":data_base["data"]["current_state"],"Party Size":data_base["data"]["party_size"]}   
            #rasing exception manually  because of the bad api response :(  
            if not data_base["data"]["current_selected_gamemode"]:
                raise Exception("Manual Exception")

            if not data_base["data"]["gamemode"]:
                raise Exception("Manual Exception")

        except(KeyError):
            try:
            #User no added or User offline
                fields_dict3={"Error":data_base["message"]}

            except(KeyError):
                #this line of code will probably never be executed because even if user inputs wrong username then there is a message "user not found" in the API.
                message_player_data_response=discord.Embed(title="Live Game Stats",color=color,
                description=f'No Data Found for {player_tag[0]} ')
                return message_player_data_response

            else:
                message_player_data_response=discord.Embed(title="oooops!",color=color,
                description=f'{player_tag[0]} is having some error')
                for key in fields_dict3:
                    message_player_data_response.add_field(
                        name=key,
                        value=fields_dict3[key],
                        inline=False
                    )
                return message_player_data_response

        except: 
        #this block is explicitly created for custom game because api throws null value for custom game so we have to handle it by passing string value manually i.e "Game Mode Selected"
            fields_dict_custom={"Game Mode Selected":"Custom", "Current State":data_base["data"]["current_state"],"Party Size":data_base["data"]["party_size"]}
            
            message_player_data_response=discord.Embed(title="Live Game Stats!",color=color,
            description=f' Here are Live Game Stats of {player_tag[0]}')
            for key in fields_dict_custom:
                message_player_data_response.add_field(
                    name=key,
                    value=fields_dict_custom[key],
                    inline=False
                )
            return message_player_data_response


        else:
            print("inside here in menus")
            message_player_data_response=discord.Embed(title="Live Game Stats",color=color,
            description=f'Here are Live Game Stats of {player_tag[0]}')
            for key in fields_dict2:
                message_player_data_response.add_field(
                    name=key,
                    value=fields_dict2[key],
                    inline=False
                )
            return message_player_data_response
            
    except:
        #this block is explicitly created for custom game because api throws null value for custom game so we have to handle it by passing string value manually i.e "Game Mode Selected"
        fields_dict_custom_ingame={"Game Mode Selected":"Custom", "Current State":data_base["data"]["current_state"],"Map":data_base["data"]["map"],"Ally Team Score":str(data_base["data"]["score_ally_team"]),"Enemy Team Score":str(data_base["data"]["score_enemy_team"])}
        message_player_data_response=discord.Embed(title="Live Game Stats!",color=color,
        description=f'Here are Live Game Stats of {player_tag[0]}')
        for key in fields_dict_custom_ingame:
            message_player_data_response.add_field(
                name=key,
                value=fields_dict_custom_ingame[key],
                inline=False
            )
        return message_player_data_response

    else:
        message_player_data_response=discord.Embed(title="Live Game Stats",color=color,
        description=f'Here are Live Game Stats of {player_tag[0]}')
        for key in fields_dict1:
            print(key,fields_dict1[key])
            message_player_data_response.add_field(
                name=key,
                value=fields_dict1[key],
                inline=False
            )
        return message_player_data_response



def leaderboard(region):
    try:
        data_base=requests.get(f"{valorant_endpoint}/valorant/v1/leaderboard/{region}").json()
        message_player_data_response=discord.Embed(title=f"Top Players of {region}",color=color)
        
        for key in range(10):
            message_player_data_response.add_field(
                name=f"{key+1}",
                value=data_base[key]["gameName"],
                inline=False
            )
        return message_player_data_response
    except:
        message_player_data_response=discord.Embed(title=f"ooops!",description=f"{data_base['message']}",color=color)
        return message_player_data_response



def help():
    message_player_data_response=discord.Embed(title=f"𝐇𝐨𝐰 𝐭𝐨 𝐮𝐬𝐞 𝐦𝐞~",color=color)
    help_field={"Player Profile Stats":"Prefix : '&player-' |Example : &player-Scream#1tapss ","Live Match Stats (Bot need to be added as friend)":"Prefix : '&live-' |Example : &live-Scream#1tapss ","Top 10 Players of a Region (Available regions: eu, ap, na, kr)":"Prefix : '&top-' |Example : &top-ap ","Bonus Command":"Prefix : '&hello-' |Example : &hello ",}
    for key in help_field:
        message_player_data_response.add_field(
            name=key,
            value=help_field[key],
            inline=False
        )
    return message_player_data_response

def join():
    message_player_data_response=discord.Embed(title=f"Thanks for adding me!",color=color)
    intro_field={"Hi there! I am Coop , a Valorant Stats Bot":"use prefix &help to know how to use me","Created By":"Aman Saini","My Github Repository":"https://github.com/gabbar23/Valorant-Discord-Bot","Invite me ":"https://discord.com/api/oauth2/authorize?client_id=873252963282452561&permissions=211968&scope=bot"}
    for key in intro_field:
        message_player_data_response.add_field(
            name=key,
            value=intro_field[key],
            inline=False
        )
    return message_player_data_response