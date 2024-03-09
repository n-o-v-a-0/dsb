import requests
import time
import random
import ctypes
import websocket

def error(title, message):
    MB_OK = 0x0
    MB_ICONERROR = 0x10
    ctypes.windll.user32.MessageBoxW(0, message, title, MB_OK | MB_ICONERROR)

def read_token():
    try:
        with open('discord.token', 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        error('error', 'discord.token file was not found')


token = read_token()

def typing(channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/typing"
    headers = {
        "Authorization": token
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 204:
        print("Typing signal sent.")
    else:
        print("Typing signal failed. Status code:", response.status_code)

def message(channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token
    }
    payload = {
        "content": message
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Message sent.")
    else:
        print("Message wasn't sent. Status code:", response.status_code)


def changeChannelName(channel_id, name):

    url = f"https://discord.com/api/v9/channels/{channel_id}"

    payload = {
        "name": name
    }

    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, json=payload, headers=headers)

    print('Channel named.')

def createChannel(guild_id, category_id, name, type):
    
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    headers = {
        "Authorization": token
    }
    
    payload = {
        "type": type,
        "name": name,
        "permission_overwrites": [],
        "parent_id": category_id
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Channel created")
    else:
        print("Channel wasn't created. Status code:", response.status_code)

def list_servers():
    headers = {
        "Authorization": token
    }

    response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)

    if response.status_code == 200:
        guilds = response.json()
        for guild in guilds:
            print(f"Guild Name: {guild['name']}, Guild ID: {guild['id']}")
    else:
        print("Failed to fetch guilds:", response.text)
