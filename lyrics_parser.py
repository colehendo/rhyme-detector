from functools import cache
from itertools import takewhile
from string import punctuation
from typing import List, Optional


class LineCleaner:
    @staticmethod
    def remove_punctuation(line: str) -> str:
        for punctuation_mark in punctuation:
            line = line.replace(punctuation_mark, "")
        return line

    @staticmethod
    def remove_square_brackets(line: str) -> str:
        start = line.find("[")
        end = line.find("]")
        if start != -1 and end != -1:
            line = line[:start] + line[end + 1 :]

        return line

    @staticmethod
    def make_line_lowercase(line: str) -> str:
        line = line.lower()
        return line

    def clean_line(self, line: str) -> str:
        if not line:
            return line

        line = self.remove_square_brackets(line)
        line = self.remove_punctuation(line)
        line = self.make_line_lowercase(line)

        return line


class LyricsCleaner:
    def __init__(self, lyric_lines: List[str]) -> None:
        self.lyric_lines = lyric_lines
        self.line_cleaner = LineCleaner()

    @staticmethod
    def clean_final_word(words: List[str]) -> str:
        cleaned_final_word = "".join(takewhile(str.isalpha, words[-1]))
        words[-1] = cleaned_final_word

    @property
    @cache
    def contributors_line(self) -> Optional[int]:
        for line_number in range(3):
            if "Contributors" in self.lyric_lines[line_number]:
                return line_number
        return -1

    def clean_lyrics(self) -> List[str]:
        cleaned_lyric_lines = []
        lyrics_length = len(self.lyric_lines)

        for line_number, line in enumerate(self.lyric_lines):
            # Genius lyrics' API returns an initial line in the lyrics
            # noting the number of contributors to the song lyrics.
            # This removes that contributors line, and any preceding lines
            if line_number <= self.contributors_line:
                continue

            line = self.line_cleaner.clean_line(line)
            if not line:
                continue

            words = line.split(" ")

            # Genius lyrics' API returns the final word
            # with an embed code on the final word.
            # This removes that code
            if line_number == lyrics_length - 1:
                self.clean_final_word(words)

            cleaned_lyric_lines.append(words)

        return cleaned_lyric_lines


class LyricsParser:
    def parse_raw_lyrics(self, lyrics: str) -> List[str]:
        lyric_lines = lyrics.split("\n")
        return lyric_lines

    def parse_lyrics(self, lyrics: str) -> List[str]:
        lyric_lines = self.parse_raw_lyrics(lyrics)
        lyric_lines = LyricsCleaner(lyric_lines).clean_lyrics()

        return lyric_lines
