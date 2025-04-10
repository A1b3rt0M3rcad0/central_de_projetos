from src.security.cryptography.utils.salt import Salt


def test_salt_generation() -> None:
    # Arrange & Act
    salt = Salt()
    
    # Assert
    assert isinstance(salt.salt, bytes)
    assert len(salt.salt) > 0


def test_salt_initialization_with_existing_salt() -> None:
    # Arrange
    existing_salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    
    # Act
    salt = Salt(existing_salt)
    
    # Assert
    assert salt.salt == existing_salt


def test_salt_generation_uniqueness() -> None:
    # Arrange & Act
    salt1 = Salt()
    salt2 = Salt()
    
    # Assert
    assert salt1.salt != salt2.salt