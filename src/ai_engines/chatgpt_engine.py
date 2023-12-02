from time import sleep
from cv2 import log
import openai
from openai.error import RateLimitError
import pandas as pd
import logging
import os

from src.constants import OPEN_AI_API_KEY # TODO make this an environment variable
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your API key from an environment variable or secret management service
openai.api_key = OPEN_AI_API_KEY

def llm_filter(transcript: pd.DataFrame):
    if os.path.exists("output_chunks/approved_script.csv"):
        logging.info("cached approved script found, skipping llm filter")
        return pd.read_csv("output_chunks/approved_script.csv")
    
    context_role = {
        "role": "system",
        "content": "You are my video editor and will see transcript of my recording. We want to remove anything seems like an outtake or mess-up. The criteria for each snippet is that: 1. It make sense based on what was previously said. 2. It is not a mess-up or outtake. 3. It was not said previously. 4. It is a concise thought. Determine whether it stays in the final edit or not with 'YES' or 'NO'.",
    }

    approved_script = pd.DataFrame()
    for index, row in transcript.iterrows():
        text = row["text"]
        start = row["start"]
        end = row["end"]
        messages = [
            context_role,
            {"role": "system", "content": "The content of the video is about mean comments and cyberbullying."}
        ]
        if approved_script.shape[0] > 0:
            previous_texts = ' '.join(approved_script['text'].tolist()[max(-5, -approved_script.shape[0]):])
            messages.append(
                {
                    "role": "system",
                    "content": f"What was previously said: '{previous_texts}'"
                }
            )
        messages.append({"role": "user", "content": f"Here is the current snippet: '{text}'. Should this be in the edit based on the instructions and context provided?"})
        logging.info("Prompt %s", messages)
        try:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
            )
        except RateLimitError as e:
            logging.error("Rate limit exceeded, waiting 10 seconds: %s", e)
            sleep(10)
            chat_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
            )

        response = chat_completion.choices[0].message.content
        print(text, response)
        if response == "YES":
            approved_script = pd.concat([approved_script, row.to_frame().T])

    print(approved_script)
    approved_script.to_csv("output_chunks/approved_script.csv")
    return approved_script

if __name__ == "__main__":
    transcript = pd.read_csv("output_chunks/transcript.csv")
    approved_script = llm_filter(transcript.head(5))
    approved_script.to_csv("output_chunks/approved_script.csv", index=False)
