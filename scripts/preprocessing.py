import re 

def multiple_replace(dictionary: dict, text: str) -> str:
    """Replace multiple words in sentence based on dictionary
    source : https://stackoverflow.com/a/15175239

    Args:
        dictionary (dict): Dictionary of words
        text (str): text/sentence

    Returns:
        str: text after
    """
    pattern = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))
    return pattern.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text) 