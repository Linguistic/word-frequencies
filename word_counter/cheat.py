from gzip import compress
from os import path
import sys
import pandas as pd

from requests import get

from proto.frequency_pb2 import FrequencyDictionary

lang = sys.argv[1]

content = get(
    f"https://raw.githubusercontent.com/Linguistic/FrequencyWords/master/content/2018/{lang}/{lang}_50k.txt"
).text

df = pd.DataFrame(
    [s.split(" ") for s in content.splitlines()], columns=["Word", "Frequency"]
)

df["Index"] = df.reset_index(drop=False).index + 1

p = path.join("data", f"{lang}.dat")

word_dict = pd.Series(df["Index"].values, index=df["Word"]).to_dict()

with open(p, "wb") as f:
    f.write(
        compress(
            FrequencyDictionary(language="en", frequency=word_dict).SerializeToString()
        )
    )
