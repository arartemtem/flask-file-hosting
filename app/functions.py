import os
import hashlib
import random
import string
from app.models import User, File

def md5(filename, path):
    hash_md5 = hashlib.md5()
    with open(os.path.join(path, filename), "rb") as f:
        for chunk in iter(lambda: f.read(128), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def random_string_generator(size=12, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_sharelink():
    share_link = ''
    while not share_link:
        share_link = random_string_generator()
        link = User.query.filter_by(sharelink=share_link).first()
        if link is not None:
            share_link = ''
    return share_link
