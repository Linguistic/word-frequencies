from gzip import compress
import pickle
import tarfile
from unicodedata import category
import dask.dataframe as dd

from os import path
from pandas import Series, DataFrame
from alive_progress import alive_bar
from langdetect import DetectorFactory
from proto.frequency_pb2 import FrequencyDictionary
from word_counter.langdetect import create_detector
from word_counter.subtitles import SubtitleDownloader
from word_counter.utils import get_out_dir, get_temp_dir, is_printable


class WordCounter:
    detector_factory: DetectorFactory

    subtitle_downloader: SubtitleDownloader

    language: str

    def __init__(self, language: str):
        self.detector_factory = create_detector(languages=set([language]))
        self.subtitle_downloader = SubtitleDownloader(language=language)
        self.language = language

    def _is_valid(self, word: str):
        """
        Checks if a given word is valid
        """

        try:
            detector = self.detector_factory.create()
            detector.append(word)
            detected = detector.detect().replace("-", "_")
            return detected == self.language and is_printable(word)
        except:
            return is_printable(word)

    def _count_frequencies(self, subtitles: dd.DataFrame):
        """
        Groups words by frequency and adds an additional Frequency column
        """
        grouped = subtitles.groupby(by="Word").size().reset_index()
        grouped = grouped.rename(columns={"Words": "Word", 0: "Frequency"})
        return grouped

    def _write_to_pkl(self, df: DataFrame, output_dir: str):
        """
        Writes the given DataFrame to a .pkl (Pickle) file in output_dir
        """
        p = path.join(output_dir, f"{self.language}.pkl")

        word_dict = Series(df["Index"].values, index=df["Word"]).to_dict()

        with open(p, "wb") as f:
            pickle.dump(word_dict, f)

        return p

    def _write_to_proto(self, df: DataFrame, output_dir: str):
        """
        Writes the given DataFrame to a .proto (Protobuf) file in output_dir using the frequency.proto schema
        """
        p = path.join(output_dir, f"{self.language}.bin")

        word_dict = Series(df["Index"].values, index=df["Word"]).to_dict()

        fd = FrequencyDictionary()
        fd.language = self.language
        fd.frequency.update(word_dict)

        with open(p, "wb") as f:
            f.write(compress(fd.SerializeToString()))

        return p

    def _write_to_txt(self, df: DataFrame, output_dir: str):
        """
        Writes the given DataFrame to a .txt file in output_dir
        """
        p = path.join(output_dir, f"{self.language}.txt")

        with open(p, "w") as f:
            f.write("\n".join(df["Word"]))

        return p

    def _write_to_csv(self, df: DataFrame, output_dir: str):
        """
        Writes the given DataFrame to a .csv file in output_dir
        """
        p = path.join(output_dir, f"{self.language}.csv")

        with open(p, "w") as f:
            df.to_csv(f, index=False)

        return p

    def _create_archive(self, output_dir: str, files: list[str]):
        """
        Creates an archive in output_dir containing the specified files
        """
        archive = path.join(output_dir, f"{self.language}.tar.gz")

        with tarfile.open(archive, "w:gz") as tar:
            for file in files:
                tar.add(file, arcname=path.basename(file))

    def run(self):
        output_dir = get_out_dir()
        tmp_dir = get_temp_dir()
        subtitles = self.subtitle_downloader.get_subtitles(output_dir=tmp_dir)

        with alive_bar(title="[WordCounter]", monitor=False, stats=False) as bar:
            # Group by word frequency
            ddf = self._count_frequencies(subtitles)

            # Filter out invalid words
            ddf = ddf[ddf["Word"].apply(self._is_valid, meta=("Word", "str"))]

            # Sort by frequency
            ddf = ddf.sort_values("Frequency", ascending=False)

            # Add sequential index column
            ddf["Index"] = ddf.reset_index(drop=False).index + 1

            # Compute frequencies
            df = ddf.compute().head(50000)

            # Write output files
            txt = self._write_to_txt(df, tmp_dir)
            csv = self._write_to_csv(df, tmp_dir)
            pkl = self._write_to_pkl(df, tmp_dir)
            bin = self._write_to_proto(df, tmp_dir)

            # Archive all the files
            self._create_archive(output_dir, [txt, bin, csv, pkl])
