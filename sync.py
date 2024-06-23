import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
import os

load_dotenv()
response = requests.get(os.getenv('URL'), auth=(os.getenv('AUTH_USERNAME'), os.getenv('AUTH_PASSWORD')))
if response.ok:
    response_text = response.text
else:
    response.raise_for_status()
    quit()
soup = BeautifulSoup(response_text, 'html.parser')
remote = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.jpg')]

dirname = os.path.dirname(__file__)
photos_dir = os.path.join(dirname, 'photos')

local = os.listdir(photos_dir)

for file in local:
    if file not in remote:
        os.remove(os.path.join(photos_dir, file))
        # remove from status.json
        with open('photos.json', 'r') as f:
            status = json.load(f)
        status = [image for image in status if image['image'] != file]
        with open('photos.json', 'w') as f:
            json.dump(status, f)
        print(f'{file} removed')

for file in remote:
    if file not in local:
        response = requests.get(f'{os.getenv("URL")}/{file}', auth=(os.getenv('AUTH_USERNAME'), os.getenv('AUTH_PASSWORD')))
        with open(os.path.join(photos_dir, file), 'wb') as f:
            f.write(response.content)
        # add to status.json
        with open('photos.json', 'r') as f:
            status = json.load(f)
        status.append({'image': file, 'shown': False})
        with open('photos.json', 'w') as f:
            json.dump(status, f)
        print(f'{file} added')