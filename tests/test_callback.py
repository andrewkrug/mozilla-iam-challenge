#!/usr/bin/python
import pytest

import callback

def test_callback_lib_instation():
    c = callback.OIDCCallbackHandler(
        'myfakeclient_id',
        'myfakeclient_secretSUCHSECRETSOMG',
        'MOZILLATEST.example.cm'
    )
    assert c is not None
    assert c.client_id == 'myfakeclient_id'
    assert c.client_secret == 'myfakeclient_secretSUCHSECRETSOMG'
    assert c.auth_0_domain == 'MOZILLATEST.example.cm'


def test_token_payload_generation():
    c = callback.OIDCCallbackHandler(
        'myfakeclient_id',
        'myfakeclient_secretSUCHSECRETSOMG',
        'MOZILLATEST.example.cm'
    )
    code = 'how do I get to sesame street?'
    payload = c.generate_token_payload(code)
    assert payload['code'] == code

def test_bad_token_info_parser():
    c = callback.OIDCCallbackHandler(
        'myfakeclient_id',
        'myfakeclient_secretSUCHSECRETSOMG',
        'foo.bar.nonexistant'
    )
    code = 'how do I get to sesame street?'
    payload = c.generate_token_payload(code)
    with pytest.raises(Exception) as error:
        token_info = c.token_info(payload)
