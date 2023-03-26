from os import path
import pickle
import pandas as pd

from requests import get

content = get(
    "https://raw.githubusercontent.com/Linguistic/FrequencyWords/master/content/2018/en/en_full.txt"
).text

df = pd.DataFrame(
    [s.split(" ") for s in content.splitlines()], columns=["Word", "Frequency"]
)

df["Index"] = df.reset_index(drop=False).index + 1

p = path.join("data", f"en.pkl")


word_dict = pd.Series(df["Index"].values, index=df["Word"]).to_dict()

with open(p, "wb") as f:
    pickle.dump(word_dict, f)
