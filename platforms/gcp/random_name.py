import string
import random


# Function id_generator() generates random 6 digit lowercase alphanumeric string
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    random_id = id_generator()
    print('openebs-e2e-' + random_id)
