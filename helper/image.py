from unsplash.api import Api
from unsplash.auth import Auth
from dotenv import load_dotenv
import random
import os

load_dotenv()

client_id = os.getenv('UNSPLASH_CLIENT_ID')
client_secret = os.getenv('UNSPLASH_CLIENT_SECRET')
redirect_uri = os.getenv('UNSPLASH_REDIRECT_URI')

auth = Auth(client_id, client_secret, redirect_uri)
api = Api(auth)

def search_image(query):
    response = api.search.photos(query=query, per_page=100)
    images = response['results']
    max = len(images) - 1
    index = random.randint(0, max)
    data = images[index]
    return data.urls.small