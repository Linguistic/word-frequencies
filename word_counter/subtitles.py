import gzip

from os import path, mkdir
from alive_progress import alive_bar
from urllib.request import urlretrieve


class SubtitleDownloader:
    url: str

    language: str

    def __init__(self, language: str):
        self.url = f"http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/mono/OpenSubtitles.{language}.gz"
        self.language = language

    def _get_archive(self, output_dir: str):
        if not path.exists(output_dir):
            mkdir(output_dir)

        subtitle_archive = path.join(output_dir, f"{self.language}.tok.gz")

        if not path.exists(subtitle_archive):
            with alive_bar(title="[SubtitleDownloader]", manual=True) as bar:
                bar.text("Downloading pre-tokenized subtitle data...")

                def report_hook(count, block_size, total_size):
                    bar(count * block_size / total_size)

                urlretrieve(self.url, subtitle_archive, reporthook=report_hook)

        return subtitle_archive

    def get_subtitles(self, output_dir: str):
        subtitle_archive = self._get_archive(output_dir)

        with alive_bar(title="[SubtitleDownloader]", monitor=False, stats=False) as bar:
            subtitle_file = path.join(output_dir, f"{self.language}.tok")

            if not path.exists(subtitle_file):
                bar.text("Extracting archive...")
                with gzip.open(subtitle_archive, "rb") as f:
                    subtitles = f.read().decode("utf-8")
                with open(subtitle_file, "w") as f:
                    f.write(subtitles)
            else:
                bar.text("Reading cached data...")
                with open(subtitle_file, "r", encoding="utf-8") as f:
                    subtitles = f.read()

            return subtitles
