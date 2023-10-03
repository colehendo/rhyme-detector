from argparse import ArgumentParser, Namespace


class Arguments:
    def parse_args() -> Namespace:
        parser = ArgumentParser()

        parser.add_argument(
            "--song",
            required=True,
            help="The name of the song to get the lyrics for",
        )
        parser.add_argument("--artist", help="The artist who wrote the provided song")

        return parser.parse_args()
