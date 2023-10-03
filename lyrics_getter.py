import json
from functools import cache

import boto3
from botocore.exceptions import ClientError

from lyricsgenius import Genius as genius_api


class Genius:
    @property
    @cache
    def genius_instance(self):
        genius_instance = genius_api(self.genius_api_token)
        genius_instance.verbose = False

        return genius_instance

    @property
    @cache
    def genius_api_token(self) -> str:
        secret_name = "rhyme-detector/genius-lyrics-api"
        region_name = "us-east-1"

        client = boto3.client(service_name="secretsmanager", region_name=region_name)

        try:
            raw_secret_value = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise e

        parsed_secret_value = json.loads(raw_secret_value["SecretString"])
        token = parsed_secret_value.get("token")

        return token

    def get_song_lyrics(self, song_name: str, artist: str = "") -> str:
        song_info = self.genius_instance.search_song(title=song_name, artist=artist)

        if not song_info:
            error_message = f"Could not find the song {song_name}"
            if artist:
                error_message += f" by {artist}"
            error_message += ". Please search again!"

            raise Exception(error_message)

        lyrics = song_info.lyrics

        if not lyrics:
            error_message = f"The request for the song {song_name}"
            if artist:
                error_message += f" by {artist}"
            error_message += " did not return lyrics. Please try a different song."

            raise Exception(error_message)

        print(f"\n\nHere is {song_info.title_with_featured} by {song_info.artist}:\n\n")
        return lyrics
