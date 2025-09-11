import random
import secrets
import string


def generate_password(length=12, use_letters=True, use_digits=True, use_symbols=True):
    """
    Generates a cryptographically secure random password.

    Args:
        length (int): Length of the password. Default is 12.
        use_letters (bool): Include letters in the password.
        use_digits (bool): Include digits in the password.
        use_symbols (bool): Include special symbols in the password.

    Returns:
        str: A random password.

    Raises:
        ValueError: If no character categories are selected.
    """
    categories = []
    if use_letters:
        categories.append(string.ascii_letters)
    if use_digits:
        categories.append(string.digits)
    if use_symbols:
        categories.append("+-=_")

    if not categories:
        raise ValueError("Select at least one character category")

    if length < len(categories):
        raise ValueError("Password length is too short for the chosen categories")

    # Гарантируем попадание всех категорий
    password_chars = [secrets.choice(cat) for cat in categories]

    # Остальное — случайно из всех категорий вместе
    all_chars = "".join(categories)
    password_chars += [
        secrets.choice(all_chars) for _ in range(length - len(password_chars))
    ]

    # Перемешиваем, чтобы символы категорий не всегда были в начале
    random.shuffle(password_chars)

    return "".join(password_chars)
