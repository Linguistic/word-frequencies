import json

from os import path
from langdetect import DetectorFactory, PROFILES_DIRECTORY
from langdetect.detector_factory import LangProfile


def create_detector(languages: set[str]):
    factory = DetectorFactory()
    langsize, index = len(languages), 0

    for language in languages:
        profile_path = path.join(PROFILES_DIRECTORY, language.replace("_", "-"))
        f = open(profile_path, "r", encoding="utf-8")
        json_data = json.load(f)
        profile = LangProfile(**json_data)
        factory.add_profile(profile, index, langsize)
        index += 1

    return factory
