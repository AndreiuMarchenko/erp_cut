import random
import string

def generate_random_string(length=8):
    # Генерує випадковий рядок з букв і цифр
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

