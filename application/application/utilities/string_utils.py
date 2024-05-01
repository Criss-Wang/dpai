import json
import re

from unidecode import unidecode

import nltk

try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("tokenizers/punkt")

except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")

from nltk import word_tokenize
from nltk.corpus import stopwords

english_stopwords = stopwords.words("english")


def clean_text(text):
    return " ".join(
        [t for t in word_tokenize(text.lower()) if t not in english_stopwords]
    )


def clean_commas_in_quotes(match_obj):
    cleaned_text = match_obj.group(0).replace(",", "")
    return cleaned_text


def clean_json_string(json_str):
    data = json.loads(json_str)
    if "inputs" in data:
        data["inputs"] = re.sub(
            r'(?<=")[^"]*(?=")', clean_commas_in_quotes, data["inputs"]
        )
    return json.dumps(data)


def remove_stopwords(input_string):
    # TODO: don't find the unique in each call of this method
    stop_words = set(english_stopwords)

    word_tokens = word_tokenize(input_string)

    filtered_string = " ".join([w for w in word_tokens if not w.lower() in stop_words])

    return filtered_string


def parse_rate_limit_openai_message(message):
    return re.search(
        r".*[retry after|try again in] (\d+)\s*(\w+).*",
        message,
    )


def str2bool(txt):
    if not isinstance(txt, str):
        return bool(txt)
    if txt in ["yes", "Yes", "YES", "true", "True", "TRUE"]:
        return True
    else:
        return False


def entity_replacer(query, entities):
    if any(["locs" not in ent or "name" not in ent for ent in entities]):
        return query
    offset = 0
    for ent in sorted(entities, key=lambda x: x["locs"][0]):
        start = ent["locs"][0]
        end = ent["locs"][-1]
        normalized_ent = ent["name"]

        query = query[: start + offset] + normalized_ent + query[end + offset + 1 :]
        offset += len(normalized_ent) - (end + 1 - start)
    return query


def remove_repeating_dots(s):
    return re.sub(r"(\s?\.\s?)+", " . ", s)


def remove_repeating_spaces(s):
    return re.sub(r" +", " ", s)


# Test
def text_preprocess(content):
    content = unidecode(content)
    content = remove_repeating_dots(content)
    content = content.replace(" . ", ".")
    content = content.replace(".=", " ")
    return content


def word_count(txt):
    return len(txt.replace("\n", " ").split())


def expand_string_section(text: str, string_section: str, size: int) -> str:
    """
    Given a string text and a string section, expand the string section
    by size words.
    In more detail, it expands the string section by size/2 words to the
    left and size/2 words to the right.
    If the string section is not found in the text, it returns an empty string.

    :param text: The text to expand the string section in.
    :param string_section: The string section to expand.
    :param size: The total size of words to expand.
    :return: The expanded text.
    """

    if len(text) <= len(string_section):
        return string_section

    index = text.find(string_section)
    if index == -1:
        return ""

    left_size = size // 2
    right_size = size - left_size
    left_substring = text[:index]
    right_substring = text[index + len(string_section) :]
    left_words = re.findall(r"\b\w+\b", left_substring)
    right_words = re.findall(r"\b\w+\b", right_substring)
    left_extra_words = left_words[-left_size:]
    right_extra_words = right_words[:right_size]

    augmented_text = " ".join(left_extra_words + [string_section] + right_extra_words)
    return augmented_text
