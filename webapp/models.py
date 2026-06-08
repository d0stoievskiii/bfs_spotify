from django.db import models

class Artist(models.Model):
    id = models.BigIntegerField(primary_key=True)

    #https://open.spotify.com/artist/<spotify_id>
    external_id = models.CharField(max_length=64, unique=True, db_index=True)

    name = models.CharField(max_length=512, db_index=True)
    name_normalized = models.CharField(max_length=512, db_index=True)

    followers_total = models.BigIntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["name_normalized"]),
            models.Index(fields=["popularity"]),
            models.Index(fields=["followers_total"]),
        ]

    def __str__(self):
        return self.name
