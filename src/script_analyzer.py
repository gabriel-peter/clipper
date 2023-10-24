from typing import List
import pandas as pd
import os
import re
import spacy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from torch import Tensor
from tqdm import tqdm


from src.constants import CACHE_DIRECTORY, DATA_DIRECTORY
import en_core_web_sm
nlp = en_core_web_sm.load()

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('distilbert-base-nli-mean-tokens')


def get_sentence_similarity(sentences: list[str], target: str):
    target_nlp = nlp(target)
    
    similarities = [target_nlp.similarity(nlp(sentence)) for sentence in sentences]
    max_similarity = max(similarities)
    max_index = similarities.index(max_similarity)

    # print("Target sentence:", target)
    # print("Most similar sentence:", sentences[max_index])
    # print("Similarity score:", max_similarity)
    return (sentences[max_index], max_index, max_similarity)


def intersect_scripts(transcript: pd.DataFrame) -> pd.DataFrame:
    expected_segments = load_original_script()
    actual_segments = [sentence.strip() for sentence in transcript['text'].tolist()]
    # print(actual_segments, len(actual_segments))
    matches = {}
    for i, expected_segment in tqdm(enumerate(expected_segments[:20])):
        result = get_sentence_similarity(actual_segments, expected_segment)
        matches[expected_segment] = result
    print(json.dumps(matches, indent=4, sort_keys=True))

    return transcript

def load_original_script() -> list[str]:
    with open(os.path.join(DATA_DIRECTORY, "original_script.txt"), "r", encoding="utf-8") as f:
        original_script = f.read()

        sentence_endings_regex = re.compile(r'[.!?\n]')
        segmented_scripts: list[str] = sentence_endings_regex.split(original_script)
        sentences = [sentence.strip() for sentence in segmented_scripts if sentence.strip()]

        # print(sentences, len(sentences))
        return sentences
    
def find_matching_quote(sentences: list[str], target_sentence: str):
    model = 'sentence-transformers/all-MiniLM-L6-v2'


    # Print the most similar sentence and its similarity score
    print("Target sentence:", target_sentence)
    print("Most similar sentence:", sentences[most_similar_index])
    print("Similarity score:", similarity_scores[most_similar_index])
    

if __name__ == "__main__":
    intersect_scripts(pd.read_csv(os.path.join(CACHE_DIRECTORY, "transcript.csv")))