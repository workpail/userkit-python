import random
import string


def rand_str(n=8):
    """Return a random string of length n"""
    return ''.join(random.SystemRandom().choice(string.letters)
                   for _ in range(n))

def rand_email():
    return 'test.email.{}@userkit.co'.format(rand_str())
