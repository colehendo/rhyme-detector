from string import punctuation
from typing import List


class FileParser:
    def __init__(self) -> None:
        pass

    def read_rhyme_file(self, file_name: str) -> str:
        with open(file_name, mode="r") as file:
            file_contents = file.read()
            return file_contents

    def parse_file_contents(self, file_contents: str) -> List[str]:
        file_lines = file_contents.split("\n")
        return file_lines

    def clean_file_line(self, line: str) -> str:
        for punctuation_mark in punctuation:
            line = line.replace(punctuation_mark, "")

        return line.lower()

    def clean_file_lines(self, file_lines: List[str]) -> List[str]:
        cleaned_file_lines = []
        for line in file_lines:
            if not line:
                continue

            line = self.clean_file_line(line)
            words = line.split(" ")
            cleaned_file_lines.append(words)

        return cleaned_file_lines

    def parse_file_lines(self) -> List[str]:
        file_name = "lifes_a_bitch.txt"
        file_contents = self.read_rhyme_file(file_name)
        file_lines = self.parse_file_contents(file_contents)
        file_lines = self.clean_file_lines(file_lines)

        return file_lines
