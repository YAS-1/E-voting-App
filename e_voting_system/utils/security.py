import hashlib
import random
import string

# The security based functions 

def generate_voter_card_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()