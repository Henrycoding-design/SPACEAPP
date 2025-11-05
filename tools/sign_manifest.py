import json, base64, sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def canonical_bytes(obj):
    return json.dumps(obj, separators=(',', ':'), sort_keys=True).encode('utf-8')

if __name__ == "__main__":
    manifest_path = sys.argv[1]  # update.json
    private_pem_path = sys.argv[2]  # private.pem
    sig_out = sys.argv[3]  # update.json.sig

    with open(manifest_path, "rb") as f:
        manifest = json.load(f)
    with open(private_pem_path, "rb") as f:
        priv = load_pem_private_key(f.read(), password=None)

    data = canonical_bytes(manifest)
    sig = priv.sign(data, padding.PKCS1v15(), hashes.SHA256())
    with open(sig_out, "wb") as f:
        f.write(sig)
    print("Signed:", sig_out)