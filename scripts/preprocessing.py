import os
import json
import re
import string
from typing import Dict

with open(os.path.join(os.path.dirname(__file__), "..", "kamus", "kata-gaul.json")) as f:
    SLANG_DICT = json.load(f)


def remove_noise(text: str) -> str:
    """Remove noise feature on text

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    emoji_pattern = re.compile(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    html_pattern = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    url_pattern = re.compile(
        r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
    )

    text = text.lower()  # case folding
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE)  # remove whitespace
    text = emoji_pattern.sub("", text)  # remove emoji
    text = html_pattern.sub("", text)  # remove html tags
    text = url_pattern.sub("", text)  # remove url
    text = text.translate(str.maketrans("", "", string.digits))  # remove numbers
    text = text.translate(
        str.maketrans(string.punctuation, " " * len(string.punctuation))
    )  # remove punctuation
    text = " ".join(text.split())  # remove multiple whitespace
    return text


def replace_slang(text: str, dictionary: Dict[str, str] = SLANG_DICT) -> str:
    """Replace slang words in sentence based on dictionary
    source : https://stackoverflow.com/a/15175239

    Args:
        text (str): text/sentence
        dictionary (Dict[str, str]): Dictionary of words [slang, formal]

    Returns:
        str: text after
    """
    pattern = re.compile("(%s)" % "|".join(map(lambda x: rf"\b{x}\b", dictionary.keys())))
    return pattern.sub(lambda mo: dictionary[mo.string[mo.start() : mo.end()]], text)


def replace_word_elongation(text: str) -> str:
    """Replace word elongation inside text

    Args:
        text (str): text/sentence

    Returns:
        str: text after
    """
    pattern = re.compile(r"\b\w*([a-z])(\1{1,})\w*\b")
    return pattern.sub(
        lambda mo: re.sub(r"(?i)([a-z])(\1{1,})", r"\1", mo.string[mo.start() : mo.end()]), text
    )


class TweetPreprocessing:
    def __init__(self, slang_words_dict: Dict[str, str] = SLANG_DICT) -> None:
        self._emoji_pattern = re.compile(
            pattern="["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+",
            flags=re.UNICODE,
        )
        self._html_pattern = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        self._url_pattern = re.compile(
            r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"
        )
        self._slang_dict = slang_words_dict
        self._slang_pattern = re.compile(
            "(%s)" % "|".join(map(lambda x: rf"\b{x}\b", slang_words_dict.keys()))
        )
        self._we_pattern = re.compile(r"\b\w*([a-z])(\1{1,})\w*\b")
