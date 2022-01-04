import random
import string

from AdvancedDevelopment.firebase import FirebaseClient


def gen_ran(size=16):
    """e.g. mqPssj5bbYDOSoy5"""
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])


def generate_id(client: FirebaseClient):
    """Generate ID using gen_ran and rotate it until it's unique in the client"""
    id_gen = gen_ran()
    while client.get_by_id(id_gen) is not False:  # if id is taken, find another until one is free
        id_gen = gen_ran()

    return id_gen
