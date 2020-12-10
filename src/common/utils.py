import ast
import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def extract_name(full_name):
    return full_name.strip('.yaml').strip('.yml')


def extract_templates_list(text):
    return ast.literal_eval(text.decode("utf-8"))['templates']
