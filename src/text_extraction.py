from enum import Enum
import os
import whisper
from moviepy.editor import VideoFileClip
import pandas as pd
import logging

from src.constants import AUDIO_CACHE_DIRECTORY, CACHE_DIRECTORY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




# speed optimization: https://stackoverflow.com/questions/75908422/whisper-ai-error-fp16-is-not-supported-on-cpu-using-fp32-instead
class WhisperAiModelType(Enum):
    TINY = 'tiny'
    SMALL = 'small'
    BASE = 'base'
    MEDIUM = 'medium'
    LARGE = 'large'

def extract_audio(video_clip: VideoFileClip, 
                #   output_directory: str = CACHE_DIRECTORY,
                  model_type:  WhisperAiModelType = WhisperAiModelType.TINY) -> pd.DataFrame:
    model = whisper.load_model(model_type.value)
    if os.path.exists(os.path.join(CACHE_DIRECTORY, "transcript.csv")):
        df = pd.read_csv(os.path.join(CACHE_DIRECTORY, "transcript.csv"))
        logging.info("cached transcript found, skipping audio transcription")
    else:
        audio_path = os.path.join(AUDIO_CACHE_DIRECTORY, "audio.wav")
        video_clip.audio.write_audiofile(audio_path)
        logging.info("Starting file transcription, %s", audio_path)
        result = model.transcribe(audio_path, word_timestamps=True, fp16=False)
        logging.debug("File transcription complete, %s", audio_path)
        df = pd.DataFrame(result['segments'])
    df.to_csv(os.path.join(CACHE_DIRECTORY, "transcript.csv"))
    return df



if __name__ == "__main__":
    # Example usage
    video_path = 'data/unedited_hank_green.mp4'
    video = VideoFileClip(video_path)
    extract_audio(video, model_type=WhisperAiModelType.LARGE)