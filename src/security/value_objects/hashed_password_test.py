import pytest
from unittest.mock import Mock
from src.domain.value_objects.password import Password
from src.security.value_objects.hashed_password import HashedPassword
from src.security.cryptography.interface.i_cryptography import ICryptography
from src.security.cryptography.interface.i_salt import ISalt

@pytest.fixture
def valid_password():
    return Password('ValidPass1')

@pytest.fixture
def mock_salt():
    salt = Mock(spec=ISalt)
    salt.salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    return salt

@pytest.fixture
def mock_cryptography():
    crypto = Mock(spec=ICryptography)
    crypto.hash.return_value = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY9xcqKMHXHxqy6'
    return crypto

def test_hashed_password_creation(valid_password, mock_cryptography, mock_salt):
    hashed_pass = HashedPassword(valid_password, mock_cryptography, mock_salt)
    assert isinstance(hashed_pass, HashedPassword)
    mock_cryptography.hash.assert_called_once_with(valid_password, mock_salt)

def test_hashed_password_property(valid_password, mock_cryptography, mock_salt):
    expected_hash = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY9xcqKMHXHxqy6'
    hashed_pass = HashedPassword(valid_password, mock_cryptography, mock_salt)
    assert hashed_pass.hashed_password == expected_hash

def test_str_representation(valid_password, mock_cryptography, mock_salt):
    hashed_pass = HashedPassword(valid_password, mock_cryptography, mock_salt)
    expected_str = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY9xcqKMHXHxqy6'
    assert str(hashed_pass) == expected_str

def test_repr_representation(valid_password, mock_cryptography, mock_salt):
    hashed_pass = HashedPassword(valid_password, mock_cryptography, mock_salt)
    expected_repr = 'HashedPassword($2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY9xcqKMHXHxqy6)'
    assert repr(hashed_pass) == expected_repr

def test_return_property_salt():
    salt = Mock(spec=ISalt)
    salt.salt = b'$2b$12$LQv3c1yqBWVHxkd0LHAkCO'
    hashed_pass = HashedPassword(Password('ValidPass1'), Mock(spec=ICryptography), salt)
    assert hashed_pass.salt == salt.salt

def test_return_property_cryptography():
    cryptography = Mock(spec=ICryptography)
    hashed_pass = HashedPassword(Password('ValidPass1'), cryptography, Mock(spec=ISalt))
    assert hashed_pass.cryptography == cryptography