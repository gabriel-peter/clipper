TOKEN = 'r8_SJVNd1ley9aCsrcfGn7E014EmAmxylT0wWLwf'
import os
os.environ['REPLICATE_API_TOKEN'] = TOKEN
import replicate
output = replicate.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    input={"prompt": "What is the hardest part of using LLMs in dialogue systems?"},
)
# The meta/llama-2-70b-chat model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
    print(item, end="")


if __name__ == "__main__":
    pass