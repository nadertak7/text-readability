# Import modules
import random
import math
import string
import spacy
import syllables

# Define TextReadability class 
class TextReadability:
    def __init__(self, source) -> None:
        ## TODO : Error handling for source goes here

        self.source = source

        # Load the English language model
        nlp = spacy.load("en_core_web_sm")

        # Process text with spacy
        processed_text = nlp(source)

        # Calculate the total number of (alphabetical) words
        self.num_tokens = sum(1 for token in processed_text if token.is_alpha)

        # Calculate the total number of sentences
        self.sentences = list(processed_text.sents)
        self.num_sentences = len(self.sentences)

        # Calculate the average sentence length
        self.average_sentence_length = (
            self.num_tokens
            / self.num_sentences
            if self.num_sentences > 0 else 0
        )

        # Calculate total number of syllables
        self.num_syllables = syllables.estimate(source)

        # Calculates the number of bisyllabic words
        self.num_bisyllabic_tokens = sum(1 for word in self.source.split() if syllables.estimate(word) >= 2)

        # Calculates the number of monosyllabic words
        self.num_monosyllabic_tokens = sum(1 for word in self.source.split() if syllables.estimate(word) == 1)

    # Prints stats
    def print_stats(self) -> None:
        # Add which stats to print in dict
        stats_to_print = {
            '# Words': self.num_tokens,
            '# Sentences': self.num_sentences,
            'Avg Sentence Length': self.average_sentence_length,
            '# Syllables': self.num_syllables,
            '# Monosyllabic Words': self.num_monosyllabic_tokens,
            '# Bisyllabic Words': self.num_bisyllabic_tokens
        }

        # Prints dict keys and values
        for title, stat in stats_to_print.items():
            print(f"{title}: {stat}")

    # Flesch reading ease (original)
    def flesch_reading_ease_original(self) -> float:
        # Perform calculation
        flesch_reading_ease_original_score = (
            206.835
            - (1.015 * self.average_sentence_length)
            - (84.6 * (self.num_syllables / self.num_tokens))
        )
        return flesch_reading_ease_original_score

    # Flesch reading ease (revised)
    def flesch_reading_ease_revised(self) -> float:
        # Perform calculation
        flesch_reading_ease_revised_score = (
            (1.599 * self.num_monosyllabic_tokens)
            - (1.015 * self.average_sentence_length)
            - 31.517
        )
        return flesch_reading_ease_revised_score

    # Flesch-Kincaid grade level
    def flesch_kincaid_grade_level(self) -> float:
        # Perform Calculation
        flesch_kincaid_grade_level = (
            (0.39 * (self.num_tokens / self.num_sentences))
            + (11.8 * (self.num_syllables / self.num_tokens))
            - 15.59
        )
        return flesch_kincaid_grade_level
   
    # Dale-Chall formula
    def dale_chall_formula(self) -> float:
        # Open file
        with open("./resources/dale-chall/dale-chall-wordlist.txt", encoding="utf8") as dale_chall_words:
            dale_chall_wordlist = dale_chall_words.read().splitlines()
       
        # Convert source string to a lowercase list
        source_lower_list = self.source.translate(str.maketrans('', '', string.punctuation))
       
        # Convert string and list to sets which will allow us to identify co-occurences
        source_lower_list_set = set(source_lower_list.lower().split())
        dale_chall_wordlist_set = set(dale_chall_wordlist)

        # Generate list of co-occurences (intersections)
        intersecting_tokens = source_lower_list_set.intersection(dale_chall_wordlist_set)

        # Count intersections
        dale_chall_intersection_count = len(intersecting_tokens)

        # Perform caluclation
        dale_chall_formula_score = (
            64
            - (0.95 * (self.num_tokens - dale_chall_intersection_count))
            - (0.69 * self.average_sentence_length)
        )
        return dale_chall_formula_score

    # Gunning Fog formula
    def gunning_fog_formula(self) -> float:
        # Perform calculation
        gunning_fog_index = (
            0.4
            * ((self.average_sentence_length + self.num_bisyllabic_tokens))
        )
        return gunning_fog_index

    def mclaughlin_smog_formula(self) -> float:
        # Picks random sample of 30 sentences (or all sentences if < 30) in source text
        random_sample_30_sentences_list = random.sample(self.sentences, min(30, self.num_sentences))
        random_sample_30_sentences_string = ' '.join(str(element) for element in random_sample_30_sentences_list)
    
        # Calculates the number of words with more than two syllables
        num_tokens_2plus_syllables = sum(1 for word in random_sample_30_sentences_string.split() if syllables.estimate(word) >= 2)

        # Perform calculation
        mclaughlin_smog_score = (
            3
            + math.sqrt(num_tokens_2plus_syllables)
        )
        return mclaughlin_smog_score

    def forcast_formula(self) -> float:
        # Picks random sample of 150 words (or all words if < 150) in source text
        random_sample_150_words_list = random.sample(self.source.split(), min(150, self.num_tokens))
        
        # Calculates number of monosyllabic words in sample
        num_monosyllablic_tokens_sample = sum(1 for word in random_sample_150_words_list if syllables.estimate(word) == 1)

        # Perform calculation
        forcast_score = (
            20
            - (num_monosyllablic_tokens_sample / 10)
        )
        return forcast_score
