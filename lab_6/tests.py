import os
import json
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from symmetrical import SymmetricCryptography
from asymmetrical import AsymmetricCryptography
from serialize import Serialization
from crypto_system import HybridCryptoSystem
from work_file import read_bytes, write_bytes, read_txt, write_txt, read_json


@pytest.mark.parametrize("key_size", [16, 24, 32])
def test_symmetric_encrypt_decrypt_roundtrip(key_size):
    data = b"test symmetric data"
    key = SymmetricCryptography.generate_key(key_size)
    c = SymmetricCryptography.encrypt(data, key)
    assert isinstance(c, bytes)
    assert len(c) > len(data)

    d = SymmetricCryptography.decrypt(c, key)
    assert d == data


@pytest.mark.parametrize("bad_size", [1, 15, 17, 23, 25, 31, 33])
def test_symmetric_encrypt_invalid_key_size_raises(bad_size):
    data = b"aaa"
    key = b"\x00" * bad_size
    with pytest.raises(ValueError):
        SymmetricCryptography.encrypt(data, key)


def test_symmetric_decrypt_invalid_key_size_raises():
    data = b"\x00" * 32
    key = b"\x01" * 10
    with pytest.raises(ValueError):
        SymmetricCryptography.decrypt(data, key)


def test_asymmetric_generate_encrypt_decrypt():
    a = AsymmetricCryptography("priv.pem", "pub.pem")
    private_key, public_key = a.generate_key()
    msg = b"hello rsa"
    c = a.encrypt(msg, public_key)
    assert isinstance(c, bytes)
    d = a.decrypt(c, private_key)
    assert d == msg


def test_save_and_load_symmetric_key(tmp_path):
    key = b"secret_key_bytes"
    path = tmp_path / "sym_key.bin"
    Serialization.save_symmetric_key(str(path), key)
    loaded = Serialization.load_symmetric_key(str(path))
    assert loaded == key


def test_save_and_load_rsa_keys(tmp_path):
    a = AsymmetricCryptography("priv.pem", "pub.pem")
    private_key, public_key = a.generate_key()

    priv_path = tmp_path / "private.pem"
    pub_path = tmp_path / "public.pem"

    Serialization.save_private_key(str(priv_path), private_key)
    Serialization.save_public_key(str(pub_path), public_key)

    loaded_priv = Serialization.load_private_key(str(priv_path))
    loaded_pub = Serialization.load_public_key(str(pub_path))

    # типы такие же
    from cryptography.hazmat.primitives.asymmetric import rsa

    assert isinstance(loaded_priv, rsa.RSAPrivateKey)
    assert isinstance(loaded_pub, rsa.RSAPublicKey)

    assert loaded_pub.public_numbers() == public_key.public_numbers()


def test_work_file_text_and_json(tmp_path):
    txt_path = tmp_path / "text.txt"
    json_path = tmp_path / "settings.json"

    write_txt(" hello ", str(txt_path))
    assert read_txt(str(txt_path)) == "hello"

    data = {"a": 1, "b": "test"}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    loaded = read_json(str(json_path))
    assert loaded == data


def test_work_file_bytes(tmp_path):
    bin_path = tmp_path / "data.bin"
    payload = b"\x01\x02\x03"
    write_bytes(payload, str(bin_path))
    assert read_bytes(str(bin_path)) == payload


def test_hybrid_generate_keys_calls_dependencies(tmp_path):
    sym_key_path = tmp_path / "sym_key.bin"
    priv_path = tmp_path / "priv.pem"
    pub_path = tmp_path / "pub.pem"

    h = HybridCryptoSystem(str(sym_key_path), str(priv_path), str(pub_path))

    fake_sym_key = b"A" * 16
    h.symmetric.generate_key = MagicMock(return_value=fake_sym_key)

    fake_public_key = MagicMock()
    fake_public_key.encrypt.return_value = b"encrypted_key"
    fake_private_key = MagicMock()

    h.asymmetric.generate_key = MagicMock(return_value=(fake_private_key, fake_public_key))

    with patch("crypto_system.Serialization.save_private_key") as m_save_priv, \
         patch("crypto_system.Serialization.save_public_key") as m_save_pub, \
         patch("crypto_system.write_bytes") as m_write_bytes, \
         patch("crypto_system.padding.OAEP") as m_oaep, \
         patch("crypto_system.padding.MGF1") as m_mgf1, \
         patch("crypto_system.hashes.SHA256") as m_sha:

        h.generate_keys(16)

        h.symmetric.generate_key.assert_called_once_with(16)
        h.asymmetric.generate_key.assert_called_once()

        m_save_priv.assert_called_once_with(h.asymmetric.private_key_path, fake_private_key)
        m_save_pub.assert_called_once_with(h.asymmetric.public_key_path, fake_public_key)

        fake_public_key.encrypt.assert_called_once()
        m_write_bytes.assert_called_once()


def test_hybrid_encrypt_decrypt_integration(tmp_path):
    sym_key_path = tmp_path / "sym_key.bin"
    priv_path = tmp_path / "priv.pem"
    pub_path = tmp_path / "pub.pem"
    in_path = tmp_path / "plain.txt"
    enc_path = tmp_path / "enc.bin"
    dec_path = tmp_path / "dec.txt"

    text = "Привет, мир!"
    write_txt(text, str(in_path))

    h = HybridCryptoSystem(str(sym_key_path), str(priv_path), str(pub_path))
    h.generate_keys(16)
    h.encrypt(str(in_path), str(enc_path))
    h.decrypt(str(enc_path), str(dec_path))

    res = read_txt(str(dec_path))
    assert res == text
