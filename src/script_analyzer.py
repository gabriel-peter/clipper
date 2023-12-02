from typing import List
import pandas as pd
import os
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from src.constants import APPROVED_TRANSCRIPT_PATH, CACHE_DIRECTORY, DATA_DIRECTORY
import en_core_web_lg
import en_core_web_sm

nlp = en_core_web_sm.load()

accuracy_threshold = 0.4

def get_sentence_similarity(sentences: list[str], target: str):
    target_nlp = nlp(target)
    similarities = [target_nlp.similarity(nlp(sentence)) for sentence in sentences]
    similarities_filtered = list(filter(lambda x: x > accuracy_threshold, similarities))
    if len(similarities_filtered) == 0:
        return None
    max_similarity = max(similarities_filtered)
    max_index = similarities_filtered.index(max_similarity)
    return (sentences[max_index], max_index, max_similarity)


def intersect_script_worker(args):
    transcript, expected_segment, progress_ref, i = args
    sentence_list = get_sentence_similarity(transcript, expected_segment)
    progress_ref.update(1)
    return expected_segment, sentence_list


def intersect_scripts(transcript: pd.DataFrame, num_threads=4) -> pd.DataFrame:
    expected_segments = load_original_script()
    transcript.reset_index(inplace=True)
    actual_segments = [sentence.strip() for sentence in transcript["text"].tolist()]

    total_segments = len(expected_segments)
    progress_ref = tqdm(total=total_segments)

    args_list = [
        (actual_segments, expected_segment, progress_ref, i)
        for i, expected_segment in enumerate(expected_segments)
    ]
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        result = executor.map(intersect_script_worker, args_list)

    matches = {
        expected_segment: list(matches) for expected_segment, matches in list(result) if matches is not None
    }
    index_to_segment = {}
    for expected_segment, matches in matches.items():
        index_to_segment[matches[1]] = expected_segment
        print(f"Expected: {expected_segment}")
    print(index_to_segment)
    transcript['script_match'] = transcript.index.map(
        lambda x: index_to_segment[x] if x in index_to_segment else None)

    script_intersection = transcript[transcript['script_match'].notnull()]
    script_intersection.to_csv(APPROVED_TRANSCRIPT_PATH, index=False)

    return script_intersection

def load_original_script() -> list[str]:
    with open(
        os.path.join(DATA_DIRECTORY, "original_script.txt"), "r", encoding="utf-8"
    ) as f:
        original_script = f.read()

        sentence_endings_regex = re.compile(r"[.!?\n]")
        segmented_scripts: list[str] = sentence_endings_regex.split(original_script)
        sentences = [
            sentence.strip() for sentence in segmented_scripts if sentence.strip()
        ]

        return sentences

if __name__ == "__main__":
    intersect_scripts(pd.read_csv(os.path.join(CACHE_DIRECTORY, "transcript.csv")))
