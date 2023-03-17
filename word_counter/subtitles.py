import dask.dataframe as dd
import dask.bag as db
import pandas as pd
import lxml.etree as ET

from pathlib import Path
from os import path, mkdir
from alive_progress import alive_bar
from urllib.request import urlretrieve
from pandas import Series
from zipfile import ZipFile

parser = ET.XMLParser(encoding="utf-8", recover=True)


class SubtitleDownloader:
    url: str

    language: str

    def __init__(self, language: str):
        self.url = f"https://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/xml/{language}.zip"
        self.language = language

    def _get_archive(self, output_dir: str):
        if not path.exists(output_dir):
            mkdir(output_dir)

        subtitle_archive = path.join(output_dir, path.basename(self.url))

        if not path.exists(subtitle_archive):
            with alive_bar(title="[SubtitleDownloader]", manual=True) as bar:
                bar.text("Downloading pre-tokenized subtitle data...")

                def report_hook(count, block_size, total_size):
                    bar(count * block_size / total_size)

                urlretrieve(self.url, subtitle_archive, reporthook=report_hook)

        return subtitle_archive

    def _get_words(self, path: str):
        root = ET.parse(path, parser)

        for w in root.findall(".//w"):
            if w.text == "3ch000000" or w.text == "fnmicrosoft":
                print(path)

        return [
            w.text.casefold()
            for w in root.findall(".//w")
            if w.text is not None and not w.text.isspace()
        ]

    def get_subtitles(self, output_dir: str):
        subtitle_archive = self._get_archive(output_dir)

        with alive_bar(title="[SubtitleDownloader]", monitor=False, stats=False) as bar:
            subtitle_dir = path.join(output_dir, self.language)

            if not path.exists(subtitle_dir):
                bar.text("Extracting archive...")

                with ZipFile(subtitle_archive, "r") as zip_ref:
                    zip_ref.extractall(subtitle_dir)

            bar.text("Reading data...")

            words_series = None

            b = (
                db.from_sequence(Path(subtitle_dir).rglob("*.xml"))
                .map(self._get_words)
                .flatten()
            )

            df = b.to_dataframe(columns=["Word"])

            words_series = (
                df
                if words_series is None
                else dd.concat(
                    [
                        words_series,
                        df,
                    ],
                    ignore_index=True,
                )
            )

            words_series.reset_index(drop=True)

            return words_series
