import syllables
import spacy

class TextReadability:
    def __init__(self, source) -> None:
        # Load the English language model
        nlp = spacy.load("en_core_web_sm")

        # Process text with spacy
        processed_text = nlp(source)

        # Calculate the total number of (alphabetical) words
        self.total_words = sum(1 for token in processed_text if token.is_alpha)

        # Calculate the total number of sentences
        self.total_sentences = len(list(processed_text.sents))

        # Calculate the average sentence length
        self.average_sentence_length = (
            self.total_words 
            / self.total_sentences 
            if self.total_sentences > 0 else 0
        )

        # Calculate total number of syllables
        self.total_syllables = syllables.estimate(source)

        # Calculates the number of monosyllabic words
        self.total_monosyllabic_words = sum(1 for word in source.split() if syllables.estimate(word) == 1)

    # Prints stats
    def print_stats(self) -> None:
        print(f"Total Words: {self.total_words}")
        print(f"Total Sentences: {self.total_sentences}")
        print(f"Average Sentence Length: {self.average_sentence_length}")
        print(f"Total Syllables: {self.total_syllables}")
        print(f"Total Monosyllablic Words: {self.total_monosyllabic_words}")

    # Flesch reading ease (original)
    def flesch_reading_ease_original(self) -> float:
        flesch_reading_ease_original_score = (
            206.835
            - (1015 * self.average_sentence_length)
            - (84.6 * (self.total_syllables / self.total_words))
        )
        return flesch_reading_ease_original_score

    # Flesch reading ease (revised)
    def flesch_reading_ease_revised(self) -> float:
        flesch_reading_ease_revised_score = (
            (1.599 * self.total_monosyllabic_words)
            - (1.015 * self.average_sentence_length)
            - 31.517
        )
        return flesch_reading_ease_revised_score

    # Flesch-Kincaid grade level 
    def flesch_kincaid_grade_level(self) -> float:
        flesch_kincaid_grade_level = (
            (0.39 * (self.total_words / self.total_sentences))
            + (11.8 * (self.total_syllables / self.total_words))
            - 15.59
        )
        return flesch_kincaid_grade_level

instance = TextReadability("hello dog woof. my name is nadr.")

instance.print_stats()
