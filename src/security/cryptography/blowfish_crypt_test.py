from unittest.mock import Mock
from src.security.cryptography.blowfish_crypt import BlowfishCrypt
from src.security.cryptography.interface.i_salt import ISalt
from src.domain.value_objects.password import Password


def test_hash_password() -> None:
    # Arrange
    password = Password("123@Alberto")
    mock_salt = Mock(spec=ISalt)
    mock_salt.salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    
    # Act
    hashed = BlowfishCrypt.hash(password, mock_salt)
    
    # Assert
    assert isinstance(hashed, bytes)
    assert len(hashed) > 0


def test_unhash_valid_password() -> None:
    # Arrange
    password = Password("123@Alberto")
    mock_salt = Mock(spec=ISalt)
    mock_salt.salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    hashed = BlowfishCrypt.hash(password, mock_salt)
    
    # Act
    result = BlowfishCrypt.check(password, hashed)
    
    # Assert
    assert result is True


def test_unhash_invalid_password() -> None:
    # Arrange
    password = Password("123@Alberto")
    wrong_password = Password("123@Alberto1")
    mock_salt = Mock(spec=ISalt)
    mock_salt.salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    hashed = BlowfishCrypt.hash(password, mock_salt)
    
    # Act
    result = BlowfishCrypt.check(wrong_password, hashed)
    
    # Assert
    assert result is False