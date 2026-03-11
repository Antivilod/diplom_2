import random
import string

def generate_random_string(length=10):
    """Генерирует случайную строку из букв и цифр."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    """Генерирует данные для нового пользователя."""
    email = f"test_{generate_random_string(8)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(8)
    return {
        "email": email,
        "password": password,
        "name": name
    }

def generate_invalid_ingredient_hash():
    """Генерирует заведомо невалидный хеш ингредиента."""
    return f"invalid_{generate_random_string(20)}"