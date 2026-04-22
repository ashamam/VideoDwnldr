import re

link_pattern = r"https?://\S+"


def is_valid_link(link):
    return re.match(link_pattern, link) is not None
