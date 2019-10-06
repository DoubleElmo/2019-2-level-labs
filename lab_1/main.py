"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    if not isinstance(text, str):
        return {}
    form_text = ''
    for letter in str(text):
        if letter.isalpha() or letter == ' ' or letter == '\n':
            form_text += letter.lower()
    line_text = form_text.split()
    new_dick = {}
    for word in line_text:
        if word not in new_dick:
            new_dick[word] = 1
        else:
            new_dick[word] += 1
    return new_dick


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    newlywed = {}
    if not isinstance(frequencies, dict):
        return {}
    elif not isinstance(stop_words, tuple):
        return frequencies
    for word in frequencies:
        if word in stop_words or not isinstance(word, str):
            pass
        else:
            newlywed[word] = frequencies[word]
    return newlywed


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    if top_n < 0:
        return ()
    animedeaths = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    isthatanime = []
    for turd in animedeaths:
        isthatanime.append(turd[0])
    top10 = tuple(isthatanime[0:top_n])
    return top10


def read_from_file(path_to_file: str, lines_limit: int) -> str:
    textile = open(path_to_file, 'r')
    n = 0
    all_lines = ''
    for line in textile:
        if n < lines_limit:
            all_lines += str(line)
            n += 1
    textile.close()
    return all_lines


def write_to_file(path_to_file: str, content: tuple):
    textice = open(path_to_file, 'w')
    for word in content:
        textice.write(word + '\n')
    textice.close()
