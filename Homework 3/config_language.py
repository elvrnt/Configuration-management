import sys
import xml.etree.ElementTree as ET
import re


class ConfigSyntaxError(Exception):
    def __init__(self, message):
        super().__init__(message)


def is_valid_name(name):
    return re.match(r'^[A-Z_]+$', name) is not None


def array_to_string(array_elem):
    values = []
    for elem in array_elem:
        if elem.tag == 'value':
            values.append(elem.text.strip())
        elif elem.tag == 'array':
            values.append(array_to_string(elem))
    return '<< ' + ', '.join(values) + ' >>'


def convert_xml_to_custom_language(xml_root):
    result = []
    constants = {}

    for elem in xml_root:
        if elem.tag == 'variable':
            var_name = elem.get('name')
            var_value = elem.text.strip()
            if not is_valid_name(var_name):
                raise ConfigSyntaxError(f"Неверное имя переменной: {var_name}")
            result.append(f"var {var_name} := {var_value};")
        elif elem.tag == 'array':
            result.append(array_to_string(elem))
        elif elem.tag == 'constant':
            const_name = elem.get('name')
            const_value = elem.text.strip()
            if not is_valid_name(const_name):
                raise ConfigSyntaxError(f"Неверное имя константы: {const_name}")
            result.append(f"(define {const_name} {const_value})")
            constants[const_name] = const_value
        else:
            raise ConfigSyntaxError(f"Неизвестный элемент: {elem.tag}")

    for i, line in enumerate(result):
        for const_name, const_value in constants.items():
            line = re.sub(r'\$\(' + re.escape(const_name) + r'\)', const_value, line)
        result[i] = line

    return '\n'.join(result)


def main():
    if len(sys.argv) != 3:
        print("Использование: python task_3.py <input_file.xml> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        sys.exit(1)
    except ET.ParseError:
        print(f"Ошибка при разборе XML-файла {input_file}.")
        sys.exit(1)

    try:
        result = convert_xml_to_custom_language(root)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    except ConfigSyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()