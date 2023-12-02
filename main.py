import os
import re
from src.constants import DATA_DIRECTORY
from src.script_analyzer import intersect_scripts
from src.video_chunker import split_video_into_chunks
from src.text_extraction import extract_audio
from src.ai_engines.nlp_engine import remove_outtakes
from src.ai_engines.chatgpt_engine import llm_filter
from src.video_stitcher import stitch_video
import logging
from moviepy.editor import VideoFileClip
import graphviz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PipelineNode:
    def __init__(self, fn, name, parent):
        # for node in pipeline:

        self.fn = fn
        self.name = name
        self.parent = parent
        self.children: list[PipelineNode] = []

    def add_child(self, child):
        ## Assumes children are added in order
        if self.name == child.name:
            return
        if self.name == child.parent:
            print("Adding child to self", self.name, child.name)
            self.children.append(child)
        else:
            children = self.children
            for c in children:
                c.add_child(child)

    def run(self, *args, **kwargs):
        logging.info("Running %s", self.name)
        output = self.fn(*args, **kwargs)
        for child in self.children:
            child.run(output)

    def visualize(self, dot):
        dot.node(self.name, self.name)
        for c in self.children:
            dot.edge(self.name, c.name, constraint='false')
            c.visualize(dot)
        return dot

pipeline = {
    'extract_audio': {
        'parent': None,
        'fn': extract_audio,
    },
    'llm_engine': {
        'parent': 'extract_audio',
        'fn': llm_filter,
    },
    'split_video_into_chunks': {
        'parent': 'llm_engine',
        'fn': split_video_into_chunks,
    },
    # 'find_outtakes': {
    #     'fn': find_outtakes,
    # },
    'stitch_video': {
        'parent': 'split_video_into_chunks',
        'fn': stitch_video
    }
}

if __name__ == "__main__":
    # WITH NO SCRIPT REF
    # root = PipelineNode(fn=extract_audio, name='extract_audio', parent=None)
    # root.add_child(PipelineNode(fn=remove_outtakes, name='remove_outtakes', parent='extract_audio'))
    # root.add_child(PipelineNode(fn=llm_filter, name='llm_engine', parent='remove_outtakes'))
    # root.add_child(PipelineNode(fn=split_video_into_chunks, name='split_video_into_chunks', parent='llm_engine'))
    # root.add_child(PipelineNode(fn=stitch_video, name='stitch_video', parent='split_video_into_chunks'))
    # root.run(video_clip = VideoFileClip(os.path.join(DATA_DIRECTORY, 'unedited_hank_green.mp4')))
    # root.visualize(graphviz.Digraph('round-table', comment='The Round Table')).render(directory='output_chunks', view=True)

    
    root = PipelineNode(fn=extract_audio, name='extract_audio', parent=None)
    # root.add_child(PipelineNode(fn=remove_outtakes, name='remove_outtakes', parent='extract_audio'))
    root.add_child(PipelineNode(fn=intersect_scripts, name='script_matcher', parent='extract_audio'))
    root.add_child(PipelineNode(fn=split_video_into_chunks, name='split_video_into_chunks', parent='script_matcher'))
    root.add_child(PipelineNode(fn=stitch_video, name='stitch_video', parent='split_video_into_chunks'))
    root.run(video_clip = VideoFileClip(os.path.join(DATA_DIRECTORY, 'unedited_hank_green.mp4')))
    root.visualize(graphviz.Digraph('round-table', comment='The Round Table')).render(directory='output_chunks', view=True)