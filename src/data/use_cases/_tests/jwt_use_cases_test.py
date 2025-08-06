import pytest
from unittest.mock import MagicMock
from src.data.use_cases.encode_jwt import EncodeJwt
from src.data.use_cases.decode_jwt_token import DecodeJwtToken
from src.data.use_cases.valid_jwt import ValidJwt

@pytest.fixture
def mock_encrypt():
    return MagicMock()

def test_encode_jwt_success(mock_encrypt):
    payload = {'user_id': 123, 'role': 'admin'}
    expected_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    mock_encrypt.encode.return_value = expected_token
    
    use_case = EncodeJwt(mock_encrypt)
    result = use_case.encode(payload)
    
    mock_encrypt.encode.assert_called_once_with(payload=payload)
    assert result == expected_token

def test_encode_jwt_encryption_error(mock_encrypt):
    payload = {'user_id': 123}
    mock_encrypt.encode.side_effect = Exception("Encryption failed")
    
    use_case = EncodeJwt(mock_encrypt)
    
    with pytest.raises(Exception, match="Encryption failed"):
        use_case.encode(payload)

def test_decode_jwt_token_success(mock_encrypt):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    expected_payload = {'user_id': 123, 'role': 'admin'}
    mock_encrypt.decode.return_value = expected_payload
    
    use_case = DecodeJwtToken(mock_encrypt)
    result = use_case.decode(token)
    
    mock_encrypt.decode.assert_called_once_with(token=token, verify_exp=True)
    assert result == expected_payload

def test_decode_jwt_token_with_verify_exp_false(mock_encrypt):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    expected_payload = {'user_id': 123}
    mock_encrypt.decode.return_value = expected_payload
    
    use_case = DecodeJwtToken(mock_encrypt)
    result = use_case.decode(token, verify_exp=False)
    
    mock_encrypt.decode.assert_called_once_with(token=token, verify_exp=False)
    assert result == expected_payload

def test_decode_jwt_token_decryption_error(mock_encrypt):
    token = 'invalid_token'
    mock_encrypt.decode.side_effect = Exception("Decryption failed")
    
    use_case = DecodeJwtToken(mock_encrypt)
    
    with pytest.raises(Exception, match="Decryption failed"):
        use_case.decode(token)

def test_valid_jwt_success(mock_encrypt):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    expected_result = {'invalid': False, 'expired': False}
    mock_encrypt.is_expired.return_value = expected_result
    
    use_case = ValidJwt(mock_encrypt)
    result = use_case.valid(token)
    
    mock_encrypt.is_expired.assert_called_once_with(token=token)
    assert result == expected_result

def test_valid_jwt_expired_token(mock_encrypt):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    expected_result = {'invalid': False, 'expired': True}
    mock_encrypt.is_expired.return_value = expected_result
    
    use_case = ValidJwt(mock_encrypt)
    result = use_case.valid(token)
    
    mock_encrypt.is_expired.assert_called_once_with(token=token)
    assert result == expected_result

def test_valid_jwt_validation_error(mock_encrypt):
    token = 'invalid_token'
    mock_encrypt.is_expired.side_effect = Exception("Validation failed")
    
    use_case = ValidJwt(mock_encrypt)
    
    with pytest.raises(Exception, match="Validation failed"):
        use_case.valid(token) 