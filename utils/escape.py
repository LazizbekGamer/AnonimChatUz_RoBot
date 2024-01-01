import re



def escape_text(text):
    escaped_text = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
    return escaped_text
