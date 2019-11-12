"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if not isinstance(num_rows, int) or not isinstance(num_cols, int):
        return []
    new_list = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
    return new_list


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    list_matrix = list(edit_matrix)
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int):
        return list_matrix
    if len(list_matrix) is False or len(list_matrix[0]) is False:
        return list_matrix
    for ind1 in range(1, len(list_matrix)):
        list_matrix[ind1][0] = list_matrix[ind1-1][0] + remove_weight
    for ind2 in range(1, len(list_matrix[0])):
        list_matrix[0][ind2] = list_matrix[0][ind2-1] + add_weight
    return list_matrix


def minimum_value(numbers: tuple) -> int:
    minint = min(numbers)
    return minint


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str,) -> list:
    if not isinstance(edit_matrix, tuple) or not isinstance(add_weight, int) or not isinstance(remove_weight, int) \
            or not isinstance(substitute_weight, int) or not isinstance(original_word, str) \
            or not isinstance(target_word, str):
        return list(edit_matrix)
    list_matrix = list(edit_matrix)
    for index1, thing1 in enumerate(list_matrix):
        if index1 == 0:
            continue
        for index2, _ in enumerate(thing1):
            if index2 == 0:
                continue
            value1 = list_matrix[index1 - 1][index2] + remove_weight
            value2 = list_matrix[index1][index2 - 1] + add_weight
            if original_word[index1 - 1] == target_word[index2 - 1]:
                value3 = list_matrix[index1 - 1][index2 - 1] + 0
            else:
                value3 = list_matrix[index1 - 1][index2 - 1] + substitute_weight
            thing1[index2] = minimum_value(tuple([value1, value2, value3]))
    return list_matrix


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int) or not isinstance(substitute_weight, int)\
            or not isinstance(original_word, str) or not isinstance(target_word, str):
        return -1
    edit_matrix = tuple(generate_edit_matrix(len(original_word)+1, len(target_word)+1))
    edit_matrix = initialize_edit_matrix(edit_matrix, add_weight, remove_weight)
    edit_matrix = fill_edit_matrix(tuple(edit_matrix), add_weight, remove_weight, substitute_weight, original_word, 
                                   target_word)
    distance = edit_matrix[-1][-1]
    return distance


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    file = open(path_to_file, 'w')
    for line in edit_matrix:
        for ind1, val1 in enumerate(line):
            line[ind1] = str(val1)
        file.write(','.join(line) + '\n')
    file.close()


def load_from_csv(path_to_file: str) -> list:
    matrix = open(path_to_file)
    matrix = matrix.readlines()
    for ind1, val1 in enumerate(matrix):
        matrix[ind1] = val1.split(',')
        for ind2, val2 in enumerate(matrix[ind1]):
            matrix[ind1][ind2] = int(val2)
    return matrix
