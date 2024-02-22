#!/usr/bun/env/python3
import hashlib

with open('public_key.pem', 'rb') as public_key_file:
    public_key = public_key_file.read()


def generate_key_identifier(public_key):
    sha256_hash = hashlib.sha256(public_key)
    key_id = sha256_hash.hexdigest()
    return key_id

print(generate_key_identifier(public_key))
