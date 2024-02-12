# Nama : Atqiya Haydar Luqman
# NIM : 13522163
# Kelas : K3

import random

def randomize_matrix(matrix_width, matrix_height):
    matrix = []
    for _ in range(matrix_height):
        row = [random.choice(['7A', '55', 'E9', '1C', 'BD']) for _ in range(matrix_width)]
        matrix.append(row)
    return matrix

def randomize_sequences_and_rewards(number_of_sequences):
    sequences_and_rewards = {}
    for _ in range(number_of_sequences):
        sequence_length = random.randint(1, 5)
        sequence = ' '.join(random.choices(['7A', '55', 'E9', '1C', 'BD'], k=sequence_length))
        reward = random.randint(10, 50)
        sequences_and_rewards[sequence] = reward
    return sequences_and_rewards

def randomize():
    buffer_size = random.randint(5, 10)
    matrix_width = random.randint(4, 8)
    matrix_height = random.randint(4, 8)
    number_of_sequences = random.randint(1, 5)

    matrix = randomize_matrix(matrix_width, matrix_height)

    sequences_and_rewards = randomize_sequences_and_rewards(number_of_sequences)

    return buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards