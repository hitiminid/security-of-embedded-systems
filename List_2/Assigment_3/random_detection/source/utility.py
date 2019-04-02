def load_text(file_path: str):
    lines = []

    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line)

    text = ''.join(lines)
    if not validate_text(text):
        raise Exception("Invalid character!")

    return text


def validate_text(text: str):
    for bit in text:
        if bit not in ('0', '1'):
            return False
    return True

def get_text(file_path: str):
    lines = []
    number_of_lines = 1000
    current_line = 0

    with open(file_path, 'r') as file:
        for line in file:
            if current_line != 0:
                lines.append(line.strip())
            if current_line == number_of_lines:
                break
            current_line = current_line + 1

    text = ''.join(lines)
    return text


# file_path = '/home/pietrek/UCZELNIA/sem1/LABS/embedded-security/List_2/Assigment_3/output'

# text = get_text(file_path)
# print(text)
