from typing import Dict, List, Tuple
from string import punctuation
from pprint import pprint
import pronouncing
from collections import defaultdict
from random import randint


def read_rhyme_file(file_name: str) -> str:
    with open(file_name, mode="r") as file:
        file_contents = file.read()
        return file_contents


def parse_file_contents(file_contents: str):
    file_lines = file_contents.split("\n")
    return file_lines


def clean_file_line(line: str):
    for punctuation_mark in punctuation:
        line = line.replace(punctuation_mark, "")

    return line.lower()


def clean_file_lines(file_lines: List[str]) -> List[str]:
    cleaned_file_lines = []
    for line in file_lines:
        if not line:
            continue

        line = clean_file_line(line)
        words = line.split(" ")
        cleaned_file_lines.append(words)

    return cleaned_file_lines


def count_word_syllables(word: str) -> int:
    pronunciations = pronouncing.phones_for_word(word)

    if not pronunciations:
        return 1

    syllable_count = pronouncing.syllable_count(pronunciations[0])
    return syllable_count


def create_syllable_count_dict(file_lines: List[str]):
    syllable_count_dict = defaultdict(list)

    for line_number, line in enumerate(file_lines):
        total_syllables = 0
        word_index = len(line) - 1

        for word in reversed(line):
            syllable_count = count_word_syllables(word)

            # remove any small word not at the end

            syllable_count_dict[word].append(
                (
                    line_number,
                    word_index,
                    total_syllables,
                    total_syllables + syllable_count,
                )
            )

            total_syllables += syllable_count
            word_index -= 1

    return syllable_count_dict


def iterate_over_dict(
    syllable_count_dict: Dict[Tuple[int], str],
    all_matched_word_placements: List[Tuple[int]],
):
    main_word = next(iter(syllable_count_dict))
    main_word_placements = syllable_count_dict[main_word]
    words_to_delete = []
    combined_word_placements = []

    del syllable_count_dict[main_word]

    rhymes = pronouncing.rhymes(main_word)

    for word, word_placements in syllable_count_dict.items():
        if word in rhymes:
            combined_word_placements.extend(word_placements)
            words_to_delete.append(word)

    for word in words_to_delete:
        del syllable_count_dict[word]

    if combined_word_placements:
        combined_word_placements.extend(main_word_placements)
        all_matched_word_placements.append(combined_word_placements)

    if syllable_count_dict:
        iterate_over_dict(syllable_count_dict, all_matched_word_placements)


# def old_iterate_over_dict(
#     syllable_count_dict: Dict[Tuple[int], str],
#     all_matched_word_placements: List[Tuple[int]],
# ):
#     matched_word_placements = []
#     main_word = next(iter(syllable_count_dict))
#     main_word_placement = syllable_count_dict[main_word]

#     main_lower_bound_syllable = main_word_placement[2]
#     main_upper_bound_syllable = main_word_placement[3]

#     del syllable_count_dict[main_word]

#     # remove any small word not at the end
#     if (
#         main_lower_bound_syllable > 0
#         and main_upper_bound_syllable - main_lower_bound_syllable <= 1
#         and syllable_count_dict
#     ):
#         iterate_over_dict(syllable_count_dict, all_matched_word_placements)

#     # TODO: utilize the search part of this package to make this looser
#     # could probably make a second reference doc of all pronunciations to use here
#     rhymes = pronouncing.rhymes(main_word)

#     for word_placement, word in syllable_count_dict.items():
#         lower_bound_syllable = word_placement[2]
#         upper_bound_syllable = word_placement[3]

#         # check nearby syllable entries
#         # TODO: formalize!!
#         if lower_bound_syllable - main_upper_bound_syllable > 3:
#             continue

#         if main_lower_bound_syllable - upper_bound_syllable > 3:
#             continue

#         # localize rhymes
#         # TODO: formalize!!
#         # TODO: reorg recursion to make this work
#         # implement sliding window
#         # if word_placement[0] > main_word_placement[0] + 5:
#         #     continue

#         if word in rhymes or word == main_word:
#             matched_word_placements.append(word_placement)

#     if matched_word_placements:
#         for word_placement in matched_word_placements:
#             del syllable_count_dict[word_placement]

#         matched_word_placements.append(main_word_placement)
#         all_matched_word_placements.append(matched_word_placements)

#     if syllable_count_dict:
#         iterate_over_dict(syllable_count_dict, all_matched_word_placements)


def pick_color_code(selected_numbers: List[int]) -> int:
    number = randint(1, 231)

    if number == 15 or number in selected_numbers:
        pick_color_code(selected_numbers)

    selected_numbers.append(number)
    return number


def color_word_backgrounds(
    lines: List[str], matched_word_placements: List[List[Tuple[int]]]
):
    color_base = "\u001b[48;5;"
    clear = "\u001b[49m"

    selected_numbers = []

    for rhyme_scheme in matched_word_placements:
        color_code = pick_color_code(selected_numbers)

        for word_placement in rhyme_scheme:
            line = word_placement[0]
            word_index = word_placement[1]

            lines[line][
                word_index
            ] = f"{color_base}{str(color_code)}m{lines[line][word_index]}{clear}"


def print_rhyme(file_lines):
    for index, line in enumerate(file_lines):
        file_lines[index] = " ".join(line)
        print(file_lines[index])
        print()


def main():
    # file_name = "cat_in_the_hat.txt"
    file_name = "lifes_a_bitch.txt"
    file_contents = read_rhyme_file(file_name)
    file_lines = parse_file_contents(file_contents)
    file_lines = clean_file_lines(file_lines)
    syllable_count_dict = create_syllable_count_dict(file_lines)

    all_matched_word_placements = []
    iterate_over_dict(syllable_count_dict, all_matched_word_placements)
    color_word_backgrounds(file_lines, all_matched_word_placements)

    print_rhyme(file_lines)



if __name__ == "__main__":
    main()
