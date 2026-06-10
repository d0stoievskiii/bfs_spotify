import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from webapp.services.bfs_lastfm import bfs_via_api

print("Testando busca via Last.fm...")
resultado = bfs_via_api("BTS", "Foo Fighters", max_depth=2)

print(f"Caminho encontrado: {resultado}")