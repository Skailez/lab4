import timeit
start = timeit.default_timer()
def value_to_toml(value):

    if isinstance(value, str):
        escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
        return f'"{escaped}"'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, (int, float)):
        return str(value)
    elif value is None:
        return 'null'
    else:
        return f'"{str(value)}"'


def dict_to_toml(data):

    lines = []

    for key, value in data.items():
        if key != "lessons":
            lines.append(f"{key} = {value_to_toml(value)}")

    if "lessons" in data and data["lessons"]:
        lines.append("")

    if "lessons" in data:
        for lesson in data["lessons"]:
            lines.append("[[lessons]]")
            for key, value in lesson.items():
                lines.append(f"{key} = {value_to_toml(value)}")
            lines.append("")

    if lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def parse_json_string(s):

    s = s.strip()

    if s.startswith('{') and s.endswith('}'):
        return parse_object(s[1:-1])
    else:
        raise ValueError("Неверный формат JSON объекта")


def parse_object(s):
    obj = {}
    i = 0
    s = s.strip()

    while i < len(s):
        if s[i] == '"':
            key_end = s.find('"', i + 1)
            key = s[i + 1:key_end]
            i = key_end + 1


            while i < len(s) and s[i] != ':':
                i += 1
            i += 1


            value, i = parse_value(s, i)
            obj[key] = value

            while i < len(s) and s[i] in [',', ' ', '\n', '\t']:
                i += 1
        else:
            i += 1

    return obj


def parse_value(s, i):
    while i < len(s) and s[i] in [' ', '\n', '\t']:
        i += 1

    if i >= len(s):
        return None, i

    if s[i] == '"':
        end = s.find('"', i + 1)
        value = s[i + 1:end]
        return value, end + 1

    elif s[i] == '{':
        depth = 1
        j = i + 1
        while j < len(s) and depth > 0:
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
            j += 1
        obj_str = s[i:j]
        return parse_json_string(obj_str), j

    elif s[i] == '[':
        depth = 1
        j = i + 1
        while j < len(s) and depth > 0:
            if s[j] == '[':
                depth += 1
            elif s[j] == ']':
                depth -= 1
            j += 1
        arr_str = s[i:j]
        return parse_array(arr_str), j

    else:
        j = i
        while j < len(s) and s[j] not in [',', '}', ']', ' ', '\n', '\t']:
            j += 1

        value_str = s[i:j]
        if value_str == 'true':
            return True, j
        elif value_str == 'false':
            return False, j
        elif value_str == 'null':
            return None, j
        else:
            try:
                if '.' in value_str:
                    return float(value_str), j
                else:
                    return int(value_str), j
            except ValueError:
                return value_str, j


def parse_array(s):
    s = s.strip()
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1].strip()

    if not s:
        return []

    arr = []
    i = 0

    while i < len(s):
        value, i = parse_value(s, i)
        arr.append(value)
        while i < len(s) and s[i] in [',', ' ', '\n', '\t']:
            i += 1
    return arr

def main():
    try:
        with open('text.json', 'r', encoding='utf-8') as file:
            json_string = file.read()
        data_dict = parse_json_string(json_string)
        toml_content = dict_to_toml(data_dict)
        with open('output3.toml', 'w', encoding='utf-8') as file:
            file.write(toml_content)

    except FileNotFoundError:
        print("Ошибка: Файл input.json не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")



if __name__ == "__main__":
    main()

end = timeit.default_timer()
print(f"Время выполнения: {end - start} секунд")