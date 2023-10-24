import json
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag
import pandas as pd

from src.constants import CACHE_DIRECTORY

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')

def detect_repeated_sentences(sentences):
    repeated_sentences = []
    sentence_freq = FreqDist(sentences)

    for sentence, count in sentence_freq.items():
        if count > 1:
            repeated_sentences.append(sentence)

    return repeated_sentences

def detect_stutters(transcript: pd.DataFrame):
    # stutters = []
    # stop_words = set(stopwords.words('english'))

    # sentences = transcript['text'].tolist()
    # for sentence in sentences:
    #     words = word_tokenize(sentence)
    #     words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    #     pos_tags = pos_tag(words)

    #     for i in range(len(pos_tags) - 1):
    #         if pos_tags[i][1] == pos_tags[i + 1][1]:
    #             stutters.append(sentence)
    #             break

    return transcript

if __name__ == "__main__":
    transcript_path = os.path.join(CACHE_DIRECTORY, "transcript.csv")
    transcript = pd.read_csv(transcript_path)
    stutters = detect_stutters(transcript)
    print("Stutters:", stutters)