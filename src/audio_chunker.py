import os
from re import split
from pydub import AudioSegment
from src.constants import CACHE_DIRECTORY

def split_audio(audio, silence_threshold=0, silence_duration=1000):
    # TODO this function may cut off mid-sentence
    chunks = 3
    return audio[::len(audio) // chunks]

if __name__ == "__main__":
    # Example usage
    audio = AudioSegment.from_file('output_chunks/audio.wav', 'wav')
    chunks = split_audio(audio)
    for i, chunk in enumerate(chunks):
        chunk.export(f"output_chunks/audio/chunk_{i}.wav", format='wav')