from file_parser import FileParser
from printer import Printer
from rhyme_builder import RhymeBuilder


def main():
    file_lines = FileParser().parse_file_lines()
    matched_word_placements = RhymeBuilder().get_matched_word_placements(file_lines)
    Printer().print_rhyme_handler(file_lines, matched_word_placements)


if __name__ == "__main__":
    main()
