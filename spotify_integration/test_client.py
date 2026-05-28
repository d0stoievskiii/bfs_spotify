from client import (
    get_token,
    search_for_artist,
    get_artist_image,
    get_similar_artists,
    get_collabs
)

token = get_token()

artist = search_for_artist(token, "Susumu Yokota")

artist_name = artist["name"]
artist_id = artist["id"]

print(f"Artist: {artist_name} ({artist_id})")

collabs = get_collabs(token, artist_id)

print(f"\nCollaborators ({len(collabs)}):")

for name, count in sorted(
    collabs.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(f"  - {name}: {count}")

print("\nImages:")
get_artist_image(token, artist_id)

print("\nSimilar artists:")

artists = get_similar_artists(artist_name)

for a in artists:
    print(a["name"], a["match"])