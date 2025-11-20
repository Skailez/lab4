import timeit
start = timeit.default_timer()

def escape_xml(text):

    if text is None:
        return ""
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def dict_to_xml(data, root_tag="schedule"):

    xml_parts = []

    xml_parts.append(f'<?xml version="1.0" encoding="UTF-8"?>')
    xml_parts.append(f'<{root_tag}>')

    for key, value in data.items():
        if key != "lessons":
            xml_parts.append(f'  <{key}>{escape_xml(value)}</{key}>')

    if "lessons" in data and data["lessons"]:
        xml_parts.append('  <lessons>')
        for lesson in data["lessons"]:
            xml_parts.append('    <lesson>')
            for key, value in lesson.items():
                xml_parts.append(f'      <{key}>{escape_xml(value)}</{key}>')
            xml_parts.append('    </lesson>')
        xml_parts.append('  </lessons>')

    xml_parts.append(f'</{root_tag}>')

    return '\n'.join(xml_parts)


def save_xml(data, filename):

    xml_content = dict_to_xml(data)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"XML файл сохранен как {filename}")


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
        save_xml(data_dict, "output4.xml")


    except FileNotFoundError:
        print("Ошибка: Файл input.json не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()

end = timeit.default_timer()
print(f"Время выполнения: {(end - start)*100} секунд*100")
