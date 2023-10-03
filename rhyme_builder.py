from collections import defaultdict
from typing import Dict, List, Tuple

import pronouncing


class RhymeBuilder:
    @staticmethod
    def create_syllable_count_dict(file_lines: List[str]):
        syllable_count_dict = defaultdict(list)

        for line_number, line in enumerate(file_lines):
            word_index = len(line) - 1

            for reverse_word_index, word in enumerate(reversed(line)):
                syllable_count_dict[word].append(
                    (
                        line_number,
                        word_index,
                        reverse_word_index,
                    )
                )

                word_index -= 1

        return syllable_count_dict

    def iterate_over_dict(
        self,
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

        # Add duplicate words if they are one of the last two words in a line
        else:
            trailing_words = [
                word_placement
                for word_placement in main_word_placements
                if word_placement[2] in (0, 1)
            ]
            all_matched_word_placements.append(trailing_words)

        if syllable_count_dict:
            self.iterate_over_dict(syllable_count_dict, all_matched_word_placements)

    def get_matched_word_placements(
        self, file_lines: List[str]
    ) -> List[List[Tuple[int]]]:
        matched_word_placements = []

        syllable_count_dict = self.create_syllable_count_dict(file_lines)
        self.iterate_over_dict(syllable_count_dict, matched_word_placements)

        return matched_word_placements
