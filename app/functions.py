import os
import hashlib

def md5(filename, path):
    hash_md5 = hashlib.md5()
    with open(os.path.join(path, filename), "rb") as f:
        for chunk in iter(lambda: f.read(128), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
