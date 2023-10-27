#!/usr/bin/env python

import os
import sys
import json

from jwcrypto import jwk


def usage():
    program = os.path.basename(sys.argv[0])
    print(f"Usage: {program} KEY_ID...", file=sys.stderr)


def generate_keys(key_ids):
    keys = [jwk.JWK.generate(kid=key_id, kty="RSA", alg="RS256") for key_id in key_ids]

    private_keys = [json.loads(exported) for exported in [key.export() for key in keys]]
    public_keys = [
        json.loads(exported)
        for exported in [key.export(private_key=False) for key in keys]
    ]

    print("private.json:\n")
    json.dump({"keys": private_keys}, sys.stdout, indent=4)

    print("\n" * 2)

    print("public.json:\n")
    json.dump({"keys": public_keys}, sys.stdout, indent=4)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    generate_keys(sys.argv[1:])