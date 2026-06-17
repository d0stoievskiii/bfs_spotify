import sys
import os

from collections import Counter, defaultdict

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from spotify_data.artist_genres_lookup import con


GENRE_FAMILIES = {

    "hip hop": [
        "hip hop",
        "rap",
        "trap",
        "drill",
        "grime",
        "phonk",
        "boom bap",
        "crunk",
        "memphis",
        "gangster",
        "rage rap"
    ],

    "rock": [
        "rock",
        "grunge",
        "shoegaze",
        "new wave",
        "post-grunge",
        "garage"
    ],

    "metal": [
        "metal",
        "djent",
        "deathcore",
        "grindcore"
    ],

    "punk": [
        "punk",
        "ska",
        "psychobilly",
        "riot grrrl"
    ],

    "emo": [
        "emo",
        "screamo"
    ],

    "pop": [
        "pop",
        "ballad"
    ],

    "indie": [
        "indie"
    ],

    "electronic": [

        "electronic",
        "edm",
        "house",
        "techno",
        "trance",
        "dubstep",
        "dance",
        "ambient",
        "bass",
        "drum and bass",
        "breakbeat",
        "breakcore",
        "hardstyle",
        "gabber",
        "nightcore",
        "synthwave",
        "vaporwave",
        "idm",
        "downtempo",
        "electro",
        "disco"
    ],

    "funk": [
        "funk"
    ],

    "r&b": [
        "r&b"
    ],

    "soul": [
        "soul",
        "motown"
    ],

    "jazz": [
        "jazz",
        "bebop",
        "hard bop",
        "swing"
    ],

    "blues": [
        "blues"
    ],

    "folk": [
        "folk"
    ],

    "country": [
        "country",
        "americana",
        "bluegrass",
        "honky tonk"
    ],

    "classical": [
        "classical",
        "opera",
        "orchestra",
        "orchestral",
        "requiem",
        "choral",
        "medieval",
        "chamber",
        "gregorian chant"
    ],

    "latin": [
        "latin",
        "salsa",
        "bachata",
        "cumbia",
        "reggaeton",
        "mariachi",
        "merengue",
        "vallenato",
        "tango",
        "bolero",
        "ranchera"
    ],

    "brazilian": [

        "mpb",
        "samba",
        "pagode",
        "sertanejo",
        "forró",
        "bossa nova",
        "axé",
        "arrocha",
        "brega",
        "piseiro",
        "funk carioca",
        "brazilian",
        "tecnobrega",
        "agronejo"
    ],

    "reggae": [
        "reggae",
        "dancehall",
        "dub",
        "ragga"
    ],

    "gospel": [
        "gospel",
        "christian",
        "worship",
        "pentecostal",
        "ccm"
    ],

    "african": [
        "afro",
        "amapiano",
        "gqom",
        "highlife",
        "fújì"
    ],

    "asian pop": [
        "k-pop",
        "j-pop",
        "c-pop",
        "mandopop",
        "cantopop"
    ],

    "soundtrack": [
        "soundtrack",
        "anime",
        "musical",
        "vocaloid"
    ]
}

def reduce_genre(genre):
    genre = genre.lower()

    for family, keywords in GENRE_FAMILIES.items():
        for keyword in keywords:
            if keyword in genre:
                return family

    return "outros"


def analyze_mapping():

    df = con.execute("""
        SELECT DISTINCT genre
        FROM artist_genres
        ORDER BY genre
    """).df()

    genres = df["genre"].tolist()
    family_count = Counter()
    mapping = defaultdict(list)
    others = []

    for genre in genres:
        family = reduce_genre(genre)
        mapping[family].append(genre)
        family_count[family] += 1

        if family == "outros":
            others.append(genre)

    total = len(genres)
    mapped = total - len(others)
    coverage = 100 * mapped / total
    print("="*70)
    print(f"Total: {total}")
    print(f"Mapeados: {mapped}")
    print(f"Outros: {len(others)}")
    print(f"Cobertura: {coverage:.2f}%")
    print("="*70)
    print("\nDistribuição:\n")

    for family, count in family_count.most_common():
        print(f"{family:15} -> {count}")

    with open(
        "genre_mapping_report.txt",
        "w",
        encoding="utf-8"

    ) as f:
        f.write(f"Total: {total}\n")
        f.write(f"Cobertura: {coverage:.2f}%\n\n")

        for family in sorted(mapping.keys()):
            f.write(f"\n[{family.upper()}]\n")

            for genre in sorted(mapping[family]):
                f.write(f"{genre}\n")

    with open(
        "unmapped_genres.txt",
        "w",
        encoding="utf-8"

    ) as f:
        for genre in others:
            f.write(f"{genre}\n")

    print("\nArquivos gerados:")

    print("genre_mapping_report.txt")
    print("unmapped_genres.txt")


if __name__ == "__main__":

    analyze_mapping()