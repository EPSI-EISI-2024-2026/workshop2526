import os
import requests
from PIL import Image
import json

# Harry Potter API for characters
api_url = 'https://hp-api.herokuapp.com/api/characters'

# Get character data
response = requests.get(api_url)
characters = response.json()

# Filter main characters
main_characters = [
    'Harry Potter',
    'Hermione Granger',
    'Ron Weasley',
    'Albus Dumbledore',
    'Severus Snape',
    'Lord Voldemort',
    'Draco Malfoy',
    'Neville Longbottom',
    'Luna Lovegood',
    'Ginny Weasley'
]

# Create images directory
images_dir = '../datasets/images'
os.makedirs(images_dir, exist_ok=True)

for char in characters:
    name = char['name']
    if name in main_characters and char['image']:
        # Create subfolder
        char_dir = os.path.join(images_dir, name.replace(' ', '_'))
        os.makedirs(char_dir, exist_ok=True)
        
        # Download image
        img_response = requests.get(char['image'])
        if img_response.status_code == 200:
            img_path = os.path.join(char_dir, f"{name.replace(' ', '_')}.jpg")
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded {name}")
        else:
            print(f"Failed to download {name}")

# Note: This downloads one image per character. For training, you may need more images.
# Consider data augmentation in the notebook.
