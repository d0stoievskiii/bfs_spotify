from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import time
import threading

# limitador pra api...
class RateLimiter:
    def __init__(self, max_per_minute: int):
        self.interval = 60.0 / max_per_minute
        self.lock = threading.Lock()
        self.last_time = 0

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time

            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)

            self.last_time = time.time()

limiter = RateLimiter(max_per_minute=20)

def safe_get(url, headers, retries=5):
    for attempt in range(retries):

        limiter.wait()

        response = get(url, headers=headers)

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 2))
            retry_after = max(retry_after, 2)

            print(f"429 hit. Backing off {retry_after}s...")
            time.sleep(retry_after)
            continue

        if response.status_code in (500, 502, 503):
            time.sleep(2 ** attempt)
            continue

        response.raise_for_status()

    raise Exception("Max retries exceeded")

load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# adquire o token a partir do client_id e client_secret
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    return json.loads(result.content)["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Busca por um artista a partir de uma string
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    result = safe_get(url + query, headers=headers)
    items = json.loads(result.content)["artists"]["items"]
    if len(items) == 0:
        print("Nenhum artista com esse nome encontrado...")
        return None
    return items[0]

# retorna todos os álbuns de um artista dado seu id
def get_all_albums(token, artist_id):
    albums = []
    offset = 0
    while True:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&market=BR&limit=10&offset={offset}"
        result = safe_get(url, headers=get_auth_header(token))
        data = json.loads(result.content)
        items = data.get("items", [])
        albums.extend(items)
        offset += 10
        if len(items) < 10:
            break
    return albums

# busca colaboradores de um artista em todos seus álbums
def get_collabs(token, artist_id):
    collabs = {}

    albums = get_all_albums(token, artist_id)

    print(f"Found {len(albums)} albums/singles, scanning tracks...")

    for album in albums:
        url = f"https://api.spotify.com/v1/albums/{album['id']}/tracks?market=BR"

        result = safe_get(url, headers=get_auth_header(token))

        tracks = json.loads(result.content).get("items", [])

        for track in tracks:
            for artist in track["artists"]:
                collab_id = artist["id"]
                collab_name = artist["name"]

                if collab_id != artist_id:

                    if collab_name not in collabs:
                        collabs[collab_name] = 0

                    collabs[collab_name] += 1

    return collabs

# imagem do artista p/ exibir
def get_artist_image(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"

    response = safe_get(url, headers=get_auth_header(token))

    data = response.json()

    images = data.get("images", [])

    if not images:
        print("No images found.")
        return

    print(f"\nFound {len(images)} images")

    for img in images:
        print(f"{img['width']}x{img['height']}")
        print(img["url"])
        print()

    return images

# artistas similares via api do last.fm
def get_similar_artists(artist, limit=10):
    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "artist.getSimilar",
        "artist": artist,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }

    response = get(url, params=params)
    time.sleep(0.2)

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(data["message"])

    return data["similarartists"]["artist"]