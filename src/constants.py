import os
CACHE_DIRECTORY = os.path.abspath('output_chunks')
DATA_DIRECTORY = os.path.abspath('data')
AUDIO_CACHE_DIRECTORY = os.path.join(CACHE_DIRECTORY, 'audio')
APPROVED_TRANSCRIPT_PATH = os.path.join(CACHE_DIRECTORY, 'approved_transcript.csv')
OPEN_AI_API_KEY = "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"

def get_input_video_paths() -> list[str]:
    return os.listdir(DATA_DIRECTORY)