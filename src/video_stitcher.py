import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import re

from src.constants import CACHE_DIRECTORY


# List of video files (change this to match your file names)
def stitch_video(video_files):

    # Load each video clip
    video_files.sort(key=sort_by_video_number)
    video_clips = [VideoFileClip(file) for file in video_files]

    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # Write the final concatenated video to a file
    final_clip.write_videofile(os.path.join(CACHE_DIRECTORY,'final_edit.mp4'), codec='libx264', audio_codec='aac')

    # Close the video clips
    for clip in video_clips:
        clip.close()

def sort_by_video_number(file):
    pattern = r'chunk_(\d+)\.mp4'
    match = re.search(pattern, file).group(1)
    return int(match)

if __name__ == "__main__":
    all_files = os.listdir(CACHE_DIRECTORY)
    # Filter MP4 files containing the word "chunk"
    mp4_files = [os.path.join(CACHE_DIRECTORY, file) for file in all_files if file.endswith('.mp4') and 'chunk' in file]
    stitch_video(mp4_files[:15])