import pickle

from concurrent.futures import ThreadPoolExecutor
from os import path
import tarfile
from pandas import Series, DataFrame
from alive_progress import alive_bar
from langdetect import DetectorFactory
from word_counter.langdetect import create_detector
from word_counter.subtitles import SubtitleDownloader
from word_counter.utils import get_out_dir, get_temp_dir, is_alpha


class WordCounter:
    detector_factory: DetectorFactory

    subtitle_downloader: SubtitleDownloader

    language: str

    def __init__(self, language: str):
        self.detector_factory = create_detector(languages=set(["en", language]))
        self.subtitle_downloader = SubtitleDownloader(language=language)
        self.language = language

    def _is_valid(self, word: str):
        try:
            detector = self.detector_factory.create()
            detector.append(word)
            detected = detector.detect().replace("-", "_")
            return detected == self.language and is_alpha(word)
        except:
            return is_alpha(word)

    def _count_frequencies(self, subtitles: str):
        subtitle_words = Series(subtitles.split())
        word_counts = subtitle_words.value_counts()
        return DataFrame({"Word": word_counts.index, "Frequency": word_counts.values})

    def _filter_df(
        self,
        df: DataFrame,
        cb: lambda _: bool,
    ):
        return df[df["Word"].apply(cb)]

    def _write_to_pkl(self, df: DataFrame, output_dir: str):
        p = path.join(output_dir, f"{self.language}.pkl")
        word_dict = Series(df["Index"].values, index=df["Word"]).to_dict()

        with open(p, "wb") as f:
            pickle.dump(word_dict, f)

        return p

    def _write_to_txt(self, df: DataFrame, output_dir: str):
        p = path.join(output_dir, f"{self.language}.txt")

        with open(p, "w") as f:
            f.write("\n".join(df["Word"]))

        return p

    def _write_to_csv(self, df: DataFrame, output_dir: str):
        p = path.join(output_dir, f"{self.language}.csv")

        with open(p, "w") as f:
            df.to_csv(f, index=False)

        return p

    def run(self):
        output_dir = get_out_dir()
        tmp_dir = get_temp_dir()
        subtitles = self.subtitle_downloader.get_subtitles(output_dir=tmp_dir)

        with alive_bar(title="[WordCounter]", monitor=False, stats=False) as bar:
            bar.text("Counting word frequencies...")

            df = self._count_frequencies(subtitles)

            bar.text("Filtering out invalid words...")

            df = self._filter_df(df, self._is_valid)

            bar.text("Sorting by frequency...")

            df = df.sort_values("Frequency", ascending=False)

            bar.text("Adding index...")

            df["Index"] = range(1, len(df) + 1)

            bar.text("Writing to .txt file...")

            txt = self._write_to_txt(df, tmp_dir)

            bar.text("Writing to .csv file...")

            csv = self._write_to_csv(df, tmp_dir)

            bar.text("Writing to .pkl file...")

            pkl = self._write_to_pkl(df, tmp_dir)

            bar.text("Compressing to archive...")

            archive = path.join(output_dir, f"{self.language}.tar.gz")

            with tarfile.open(archive, "w:gz") as tar:
                for file in [txt, csv, pkl]:
                    tar.add(file, arcname=path.basename(file))
