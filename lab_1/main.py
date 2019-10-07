"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    if not isinstance(text, str):
        return {}
    formated_text = ''
    for letter in str(text):
        if letter.isalpha() or letter == ' ' or letter == '\n':
            formated_text += letter.lower()
    line_text = formated_text.split()
    dictionary_with_frequences = {}
    for word in line_text:
        if word not in dictionary_with_frequences:
            dictionary_with_frequences[word] = 1
        else:
            dictionary_with_frequences[word] += 1
    return dictionary_with_frequences


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
    line_sorted_items = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    line_with_top_n = []
    for word in line_sorted_items:
        line_with_top_n.append(word[0])
    tuple_with_top_n = tuple(line_with_top_n[0:top_n])
    return tuple_with_top_n


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
