from instagrapi import Client
from faker import Faker
from helper.image import search_image
import requests
import tempfile
import os

def boarding(client:Client, gender:str):
    faker = Faker('id_ID')
    try:
        discover = client.get_suggest_follows()
        
        suggestions = discover['categories'][0]['suggestions']['groups'][0]['items']
        total_suggestions = len(suggestions)
        
        indexes = faker.random_elements(elements=range(total_suggestions), length=faker.random_int(min=3, max=5), unique=True)
        
        for index in indexes:
            user = suggestions[index]
            client.user_follow(user['user']['pk'])
        
        client.account_edit(**{
            'biography': faker.administrative_unit(),
            'email': f'{client.username}@inboxkitten.com',
        })
        image_url = search_image(f"indonesia {gender}")
        response = requests.get(image_url)
        if response.status_code == 200:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name

                # Upload the image
                client.account_change_picture(temp_file_path)

                # Optionally, you can remove the temporary file after upload
                os.remove(temp_file_path)
        else:
            print("Failed to download image")
    
    except Exception as e:
        print(f"Failed to update profile: {e}")