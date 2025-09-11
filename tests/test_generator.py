import string

import pytest

from password_gen.generator.generator import generate_password


def test_password_length():
    """Пароль всегда должен быть указанной длины."""
    pw = generate_password(
        length=16, use_letters=True, use_digits=True, use_symbols=True
    )
    assert len(pw) == 16


def test_contains_all_selected_categories():
    """Пароль должен содержать хотя бы один символ из каждой выбранной категории."""
    pw = generate_password(
        length=12, use_letters=True, use_digits=True, use_symbols=True
    )

    assert any(c in string.ascii_letters for c in pw)  # буквы
    assert any(c in string.digits for c in pw)  # цифры
    assert any(c in "+-=_ " for c in pw)  # символы


def test_only_letters():
    """Если выбраны только буквы, пароль не должен содержать других символов."""
    pw = generate_password(
        length=10, use_letters=True, use_digits=False, use_symbols=False
    )
    assert all(c in string.ascii_letters for c in pw)


def test_only_digits():
    """Если выбраны только цифры, пароль не должен содержать других символов."""
    pw = generate_password(
        length=10, use_letters=False, use_digits=True, use_symbols=False
    )
    assert all(c in string.digits for c in pw)


def test_error_on_no_categories():
    """Если не выбрана ни одна категория — должна быть ошибка."""
    with pytest.raises(ValueError):
        generate_password(
            length=10, use_letters=False, use_digits=False, use_symbols=False
        )


def test_error_if_length_too_short():
    """Длина пароля меньше числа выбранных категорий → ошибка."""
    with pytest.raises(ValueError):
        generate_password(length=2, use_letters=True, use_digits=True, use_symbols=True)
