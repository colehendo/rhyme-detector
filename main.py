from arguments import Arguments
from lyrics_parser import LyricsParser
from lyrics_getter import Genius
from printer import Printer
from rhyme_builder import RhymeBuilder


def main():
    args = Arguments.parse_args()

    song_name = args.song
    artist = args.artist

    lyrics = Genius().get_song_lyrics(song_name, artist)
    file_lines = LyricsParser().parse_lyrics(lyrics)
    matched_word_placements = RhymeBuilder().get_matched_word_placements(file_lines)
    Printer().print_rhyme_handler(file_lines, matched_word_placements)


if __name__ == "__main__":
    main()
