# Import modules 
import syllables
import spacy
import string
import math

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

        # Calculates the number of bisyllabic words
        self.total_bisyllabic_words = sum(1 for word in self.source.split() if syllables.estimate(word) >= 2)

    # Prints stats
    def print_stats(self) -> None:
        print(f"Total Words: {self.total_words}")
        print(f"Total Sentences: {self.total_sentences}")
        print(f"Average Sentence Length: {self.average_sentence_length}")
        print(f"Total Syllables: {self.total_syllables}")
        print(f"Total Monosyllablic Words: {self.total_monosyllabic_words}")

    # Flesch reading ease (original)
    def flesch_reading_ease_original(self) -> float:
        # Perform calculation
        flesch_reading_ease_original_score = (
            206.835
            - (1015 * self.average_sentence_length)
            - (84.6 * (self.total_syllables / self.total_words))
        )
        return flesch_reading_ease_original_score

    # Flesch reading ease (revised)
    def flesch_reading_ease_revised(self) -> float:
        # Calculates the number of monosyllabic words
        total_monosyllabic_words = sum(1 for word in self.source.split() if syllables.estimate(word) == 1)
        
        # Perform calculation
        flesch_reading_ease_revised_score = (
            (1.599 * total_monosyllabic_words)
            - (1.015 * self.average_sentence_length)
            - 31.517
        )
        return flesch_reading_ease_revised_score

    # Flesch-Kincaid grade level
    def flesch_kincaid_grade_level(self) -> float:
        # Perform Calculation
        flesch_kincaid_grade_level = (
            (0.39 * (self.total_words / self.total_sentences))
            + (11.8 * (self.total_syllables / self.total_words))
            - 15.59
        )
        return flesch_kincaid_grade_level
   
    # Dale-Chall formula
    def dale_chall_formula(self) -> float():
        # Open file
        with open("./resources/dale-chall/dale-chall-wordlist.txt") as dale_chall_words:
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

        # Perform Caluclation
        dale_chall_formula_score = (
            64
            - (0.95 * (self.total_words - dale_chall_intersection_count))
            - (0.69 * self.average_sentence_length)
        )
        return dale_chall_formula_score

    # Gunning Fog formula
    def gunning_fog_formula(self) -> float:
        # Perform Calculation
        gunning_fog_index = (
            0.4
            * ((self.average_sentence_length + self.total_bisyllabic_words))
        )
        return gunning_fog_index

    def mclaughlin_smog_formula(self):
        # TODO : Calculate for only a sample of 30 sentences in string
        mclaughlin_smog_score = ( 
            3
            + math.sqrt(self.total_bisyllabic_words)
        )
        return mclaughlin_smog_score