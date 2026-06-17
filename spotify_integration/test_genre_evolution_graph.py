import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import matplotlib.pyplot as plt
import pandas as pd

from collections import Counter, defaultdict

from spotify_data.collab_search import (
    get_artist_rowid_by_name,
    explore_levels
)

from spotify_data.artist_genres_lookup import (
    con
)

from genre_mapping import (
    reduce_genre
)


def plot_genre_evolution(
    artist_name,
    max_depth=6
):

    start_id = int(
        get_artist_rowid_by_name(
            artist_name
        )
    )

    levels = explore_levels(
        start_id,
        max_depth
    )

    distributions = {}

    for depth, artists in levels.items():

        print("\n" + "="*70)

        print(
            f"Nível {depth}"
        )

        print(
            f"Artistas: {len(artists)}"
        )

        if len(artists) == 0:
            continue

        artist_ids = [
            int(a)
            for a in artists
        ]

        print("Consultando gêneros...")

        df = con.execute("""
            SELECT
                artist_rowid,
                genre
            FROM artist_genres
            WHERE artist_rowid = ANY(?)
        """,
        [artist_ids]
        ).df()

        print(
            f"Linhas retornadas: {len(df)}"
        )

        if df.empty:
            continue

        artist_families = defaultdict(set)

        for _, row in df.iterrows():

            artist = row["artist_rowid"]

            family = reduce_genre(
                row["genre"]
            )

            if family == "outros":
                continue

            artist_families[
                artist
            ].add(
                family
            )

        artists_with_genres = len(
            artist_families
        )

        print(
            f"Artistas com gêneros válidos: "
            f"{artists_with_genres}"
        )

        if artists_with_genres == 0:
            continue

        counter = Counter()

        for families in artist_families.values():
            for family in families:
                counter[
                    family
                ] += 1

        distributions[depth] = {
            family:
            100 * count /
            artists_with_genres
            for family, count
            in counter.items()

        }
        print("\nTop famílias:")

        for family, pct in sorted(
            distributions[depth].items(),
            key=lambda x: x[1],
            reverse=True

        )[:8]:

            print(
                f"{family:12}"
                f"{pct:6.1f}%"
            )

    if not distributions:
        return

    df = pd.DataFrame(distributions).fillna(0)
    df = df.sort_index()
    df = df.div(df.sum(axis=0), axis=1) * 100
    df = df.sort_index()

    top = (
        df.mean(axis=1)
        .sort_values(
            ascending=False
        )
        .head(8)
        .index
    )
    df = df.loc[top]

    plt.figure(
        figsize=(10,4)
    )

    plt.stackplot(
        df.columns,
        df.values,
        labels=df.index,
        alpha=0.85

    )

    plt.xticks(
        range(
            min(df.columns),
            max(df.columns) + 1
        )
    )

    plt.xlabel(
        "Nível da Rede",
        fontsize=11, fontweight="bold"
    )

    plt.ylabel(
        "% dos artistas",
        fontsize=11, fontweight="bold"
    )

    plt.title(
        f"Evolução das famílias musicais\n({artist_name})",
        fontsize=12, fontweight="bold"
    )

    plt.legend(
        loc="upper left",
        bbox_to_anchor=(1.02,1)
    )

    plt.grid(
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(
        "genre_evolution.png",
        dpi=300
    )

    plt.show()


plot_genre_evolution(
    "MOZART",
    max_depth=4
)