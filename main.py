from typing import Dict, List, Tuple
from string import punctuation
from pprint import pprint
import pronouncing



def read_rhyme_file(file_name: str) -> str:
    with open(file_name, mode="r") as file:
        file_contents = file.read()
        return file_contents
    

def parse_file_contents(file_contents: str):
    file_lines = file_contents.split("\n")
    return file_lines


def clean_file_line(line: str):
    for punctuation_mark in punctuation:
        line = line.replace(punctuation_mark, '')

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
    syllable_count_dict = {}

    for line_number, line in enumerate(file_lines):
        total_syllables = 0

        for word in reversed(line):
            syllable_count = count_word_syllables(word)
            syllable_count_dict[(line_number, total_syllables, total_syllables + syllable_count)] = word
            total_syllables += syllable_count

    return syllable_count_dict


def iterate_over_dict(syllable_count_dict: Dict[Tuple[int], str], all_matched_word_placements: List[Tuple[int]]):
    matched_word_placements = []
    main_word_placement = next(iter(syllable_count_dict))

    # TODO: utilize the search part of this package to make this looser
    # could probably make a second reference doc of all pronunciations to use here
    main_word = syllable_count_dict[main_word_placement]
    rhymes = pronouncing.rhymes(main_word)
    
    del syllable_count_dict[main_word_placement]

    # TODO: only check nearby syllable entries
    for word_placement, word in syllable_count_dict.items():
        if word in rhymes or word == main_word:
            matched_word_placements.append(word_placement)

    if matched_word_placements:
        for word_placement in matched_word_placements:
            del syllable_count_dict[word_placement]

        matched_word_placements.append(main_word_placement)
        all_matched_word_placements.append(matched_word_placements)
        

    if syllable_count_dict:
        iterate_over_dict(syllable_count_dict, all_matched_word_placements)


def main():
    file_name = "cat_in_the_hat.txt"
    file_contents = read_rhyme_file(file_name)
    file_lines = parse_file_contents(file_contents)
    file_lines = clean_file_lines(file_lines)
    syllable_count_dict = create_syllable_count_dict(file_lines)
    # pprint(syllable_count_dicts)


    all_matched_word_placements = []
    iterate_over_dict(syllable_count_dict, all_matched_word_placements)
    pprint(all_matched_word_placements)



if __name__ == "__main__":
    main()