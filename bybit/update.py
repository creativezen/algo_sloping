import requests
import os
import json
import time

endpoints_filename = "endpoints.py"
max_chars = 99
cache = False

if cache and not os.path.exists("cache"):
    os.mkdir("cache")


def load_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Ошибка: {response.status_code} {response.text}")


def load_json_from_github(repo_owner, repo_name, path):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка: {response.status_code} {response.text}")


def camel_to_snake(value):
    result = []
    for i, char in enumerate(value):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)


json_filename = "cache/endpoints.json"
if cache and os.path.exists(json_filename):
    endpoints = json.load(open(json_filename, encoding="utf-8"))
else:
    endpoints = {}
    files = load_json_from_github("bybit-exchange", "pybit", "pybit")
    for file in files:
        if not file["name"].startswith("_") and file["name"].endswith(".py"):
            print(f"Загружаю endpoints из {file['name'].split('.')[0]}")
            data = load_from_url(file["download_url"])
            time.sleep(1)
            if "(str, Enum)" in data:
                rows = data.split("\n")
                for row in rows:
                    if "\"/v5" in row and "=" in row:
                        name, value = row.split("=")
                        name = name.strip().lower()
                        value = value.strip().strip("\"")
                        if name in endpoints.values():
                            add_suffix = value.split("/v5/")[-1].split("-")[0]
                            name += f"_{add_suffix}"
                        endpoints[value] = name
    if cache:
        json.dump(endpoints, open(json_filename, "w", encoding="utf-8"))

json_filename = "cache/folders.json"
print("Загружаю папки из github")
if cache and os.path.exists(json_filename):
    folders = json.load(open(json_filename, encoding="utf-8"))
else:
    folders = load_json_from_github("bybit-exchange", "docs", "docs/v5")
    if cache:
        json.dump(folders, open(json_filename, "w", encoding="utf-8"))


with open(endpoints_filename, "w") as res_file:
    res_file.write("class Endpoints:\n\n    def request(self, *_, **__):\n        pass\n")
    for folder in folders:
        if "." not in folder['name']:
            folder_name = folder['name']
            json_filename = f"cache/folder-{folder_name}.json"
            if cache and os.path.exists(json_filename):
                files = json.load(open(json_filename, encoding="utf-8"))
            else:
                files = {}
                data = load_json_from_github("bybit-exchange", "docs", f"docs/v5/{folder_name}")
                print(f"Загружаю папку {folder_name}")
                for d in data:
                    if d["type"] == "dir":
                        data2 = load_json_from_github("bybit-exchange", "docs",
                                                      f"docs/v5/{folder_name}/{d["name"]}")
                        for d2 in data2:
                            files[f"{d["name"]}-{d2["name"]}"] = d2["download_url"]
                    else:
                        files[d["name"]] = d["download_url"]
                if cache:
                    json.dump(files, open(json_filename, "w", encoding="utf-8"))
            for file_name, file_url in files.items():
                if not file_name.endswith(".mdx"):
                    continue
                file_name_2 = f"cache/{folder_name}-{file_name}"
                print(f"Загружаю endpoint {folder_name}-{file_name}")
                if cache and os.path.exists(file_name_2):
                    with open(file_name_2, "r", encoding="utf-8") as f:
                        data = f.read()
                else:
                    data = load_from_url(file_url)
                    if cache:
                        with open(file_name_2, "w", encoding="utf-8") as f:
                            f.write(data)
                    time.sleep(1)
                req = data.split("### HTTP Request\n")
                if len(req) == 1:
                    continue
                else:
                    req = req[1].split("###")
                    if len(req) == 1:
                        raise Exception(f"Ошибка {file_name_2}, не найден конец HTTP Request")
                    for row in req[0].split("\n"):
                        row = row.split(' ')
                        if len(row) > 1:
                            method = row[0].upper()
                            if method not in ("GET", "POST"):
                                raise Exception(f"Неверный метод {method}")
                            url = row[1].strip("`")
                            break
                    else:
                        raise Exception(f"Ошибка {file_name_2}, не найдены method и url")
                params_mandatory = []
                params_optional = []
                d = data.split("### Request Parameters\n")
                if len(d) == 1:
                    raise Exception(f"Ошибка {file_name_2}, не найдены Request Parameters")
                else:
                    d = d[1].split("### Response Parameters\n")
                    if len(d) == 1:
                        raise Exception(f"Ошибка {file_name_2}, не найдены Response Parameters")
                    else:
                        d = d[0].split("|:-")
                        if len(d) != 1:
                            d = d[-1].split("\n")
                            for row in d:
                                if row and row.startswith("|"):
                                    values = row.split('|')
                                    name = values[1].strip()
                                    if ">" in name:
                                        continue
                                    if "]" in name:
                                        name = name.split("]")[0].strip("[")
                                    if name == 'category':
                                        params_optional.insert(0, name)
                                    elif "true" in values[2] or "ture" in values[2]:
                                        params_mandatory.append(name)
                                    elif "false" in values[2]:
                                        params_optional.append(name)
                                    else:
                                        raise Exception(f"Ошибка {file_name_2}, неверное значение параметра {row}")
                        elif d[0].startswith("None"):
                            pass
                        else:
                            raise Exception(f"Ошибка {file_name_2}, не найдены параметры, {d}")
                if func_name := endpoints.get(url):
                    sign = "X-BAPI-SIGN" in data
                    text = f"\n    def {func_name}(self"
                    for param in params_mandatory:
                        add_text = f", {camel_to_snake(param)}"
                        if len(text) - text.rfind("\n") + len(add_text) >= max_chars:
                            text += f",\n        {' ' * (len(func_name) + 1)}{camel_to_snake(param)}"
                        else:
                            text += add_text
                    for param in params_optional:
                        add_text = f", {camel_to_snake(param)}=None"
                        if len(text) - text.rfind("\n") + len(add_text) >= max_chars:
                            text += f",\n        {' ' * (len(func_name) + 1)}{camel_to_snake(param)}=None"
                        else:
                            text += add_text
                    text += f"):\n        return self.request({method == 'POST'}, \"{url}\", {sign}"
                    for param in params_mandatory:
                        add_text = f", {param}={camel_to_snake(param)}"
                        if len(text) - text.rfind("\n") + len(add_text) >= max_chars:
                            text += f",\n                            {param}={camel_to_snake(param)}"
                        else:
                            text += add_text
                    for param in params_optional:
                        add_text = f", {param}={camel_to_snake(param)}"
                        if len(text) - text.rfind("\n") + len(add_text) >= max_chars:
                            text += f",\n                            {param}={camel_to_snake(param)}"
                        else:
                            text += add_text
                    text += ")\n"
                    res_file.write(text)