def load_text(file_path: str):
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line)

    text = ''.join(lines)
    validate_text(text)

    return text


def validate_text(text: str):
    for bit in text:
        if bit not in ('0', '1'):
            return False
            # raise Exception('Illegal char!')
    return True
