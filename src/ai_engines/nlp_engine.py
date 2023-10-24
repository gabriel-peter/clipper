from email.policy import default
import nltk
import os
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import json

nltk.download('punkt')
output_directory = 'output_chunks'

def remove_outtakes(transcript: pd.DataFrame) -> pd.DataFrame:
    # Tokenization and Text Cleaning
    tokenized_sentences = []
    sentences = transcript['text'].tolist()
    for sentence in sentences:
        try:
            tokenized_sentences.append(word_tokenize(str(sentence.lower())))
        except AttributeError:
            print(sentence) 

    # Vectorization using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_sentences])

    # Cosine Similarity
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Set a similarity threshold (adjust as needed)
    similarity_threshold = 0.2

    # Find outtakes
    outtakes = defaultdict(list)
    for i in range(len(cosine_similarities)):
        for j in range(i+1, len(cosine_similarities[i])):
            if cosine_similarities[i][j] > similarity_threshold:
                outtakes[sentences[j]].append(sentences[i])
                # outtakes.add(sentences[j])

    # TODO remove outtakes from transcript


    return transcript # TODO change this

if __name__ == "__main__":
    transcript_path = os.path.join(output_directory, "transcript.csv")
    transcript = pd.read_csv(transcript_path)
    outtakes = remove_outtakes(transcript)
    print("Outtakes:", json.dumps(outtakes, indent=4, sort_keys=True))