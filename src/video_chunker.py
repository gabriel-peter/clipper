import os
from moviepy.editor import VideoFileClip
import cv2
from pydub import AudioSegment
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

video_path = 'data/unedited_hank_green.mp4'
output_directory = "output_chunks"

def split_video_chunk_worker(args):
    input_video_path, time_tuple, output_directory, chunk_number = args
    video = VideoFileClip(input_video_path)
    clip = video.subclip(time_tuple[0], time_tuple[1])
    clip_path = os.path.join(output_directory, f"chunk_{chunk_number + 1}.mp4")
    clip.write_videofile(clip_path, audio_codec='aac')
    return clip_path


def split_video_into_chunks(time_sheet, input_video_path='data/unedited_hank_green.mp4', output_director="output_chunks", num_threads=4):
    os.makedirs(output_directory, exist_ok=True)
    time_tuples = list(zip(time_sheet['start'], time_sheet['end']))

    args_list = [(input_video_path, time_tuple, output_directory, chunk_number)
                 for chunk_number, time_tuple in enumerate(time_tuples)]
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        paths = executor.map(split_video_chunk_worker, args_list)

    return list(paths)

def clean_old_run(output_directory):
    for file in os.listdir(output_directory):
        if file.endswith('.mp4') and 'chunk' in file:
            os.remove(os.path.join(output_directory, file))

if __name__ == "__main__":
    # Example usage
    time_sheet = pd.read_csv('output_chunks/approved_script.csv')
    # Convert the DataFrame to a list of tuples
    clean_old_run(output_directory)
    split_video_into_chunks(time_sheet)