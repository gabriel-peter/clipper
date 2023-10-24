import os
import whisper
from moviepy.editor import VideoFileClip
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model = whisper.load_model("large")
output_directory = "output_chunks"

def transcribe_worker(args):
    audio_path = args
    logging.info("Starting file transcription, %s", audio_path)
    result = model.transcribe(audio_path, word_timestamps=True, fp16=False)
    logging.debug("File transcription complete, %s", audio_path)
    # print(result['segments'])
    return pd.DataFrame(result['segments'])

def transcribe(audio_file_paths: list, num_threads=4):
    args_list = [(audio_path)
                 for audio_path in audio_file_paths]
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        subframes = executor.map(transcribe_worker, args_list)

    return pd.concat(subframes)


if __name__ == "__main__":
    # Example usage
    # Multithreading attempt failed due to whisper k-v store shared resource
    # audio_dir = os.path.join("output_chunks", "audio")
    # chunks = [os.path.join(audio_dir, file) for file in os.listdir(audio_dir)]
    # print(chunks)
    # transcript = transcribe(chunks[:-1])
    transcript = transcribe(["output_chunks/audio.wav"])
    transcript.to_csv(os.path.join(output_directory, "transcript.csv"))