from src.security.hashedpassword_factory import hashedpassword_factory
from src.security.hashedpassword_factory_chk import hashedpassword_factory_chk
from src.security.value_objects.hashed_password import HashedPassword
from src.domain.value_objects.password import Password

def test_hashedpassword_factory():

    password = Password('Teste@123')

    hashedpassword_obj = hashedpassword_factory(password)
    salt = hashedpassword_obj.salt
    hashedpassword = hashedpassword_obj.hashed_password

    assert isinstance(hashedpassword_obj, HashedPassword)
    assert isinstance(salt, bytes)
    assert isinstance(hashedpassword, bytes)

    hashedpassword_chk = hashedpassword_factory_chk(hashedpassword, salt, password)

    assert hashedpassword_chk

    password_w = Password('NewPassword@123')

    hashedpassword_chk2 = hashedpassword_factory_chk(hashedpassword, salt, password_w)

    assert not hashedpassword_chk2