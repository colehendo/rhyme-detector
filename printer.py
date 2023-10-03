from functools import cache
from random import randint
from typing import List, Tuple


class Printer:
    @property
    @cache
    def color_codes_to_avoid(self) -> List[int]:
        black = 0
        white = 15
        gray = 8

        grayscale = list(range(232, 256))
        grayscale.extend([black, white, gray])

        return grayscale

    def pick_color_code(self, selected_numbers: List[int]) -> int:
        number = randint(1, 231)

        # The last condition checks if there are still unique ascii values
        if number in self.color_codes_to_avoid or (
            number in selected_numbers and len(selected_numbers) < 236
        ):
            self.pick_color_code(selected_numbers)

        selected_numbers.append(number)
        return number

    def highlight_words(
        self, lines: List[str], matched_word_placements: List[List[Tuple[int]]]
    ):
        color_base = "\u001b[48;5;"
        clear = "\u001b[49m"

        selected_numbers = []

        for rhyme_scheme in matched_word_placements:
            color_code = self.pick_color_code(selected_numbers)

            for word_placement in rhyme_scheme:
                line = word_placement[0]
                word_index = word_placement[1]

                lines[line][
                    word_index
                ] = f"{color_base}{str(color_code)}m{lines[line][word_index]}{clear}"

    @staticmethod
    def print_rhyme(file_lines: List[str]):
        for index, line in enumerate(file_lines):
            file_lines[index] = " ".join(line)
            print(file_lines[index])
            print()

    def print_rhyme_handler(
        self, file_lines: List[str], matched_word_placements: List[List[Tuple[int]]]
    ):
        self.highlight_words(file_lines, matched_word_placements)
        self.print_rhyme(file_lines)
