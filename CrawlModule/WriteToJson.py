import json
def write_to_json(links):


    # 构造一个列表，其中每个元素是 {"link": url}
    data = [{"link": url} for url in links]

    # 写入 JSON 文件
    i=0
    with open("../resources/json_input_path.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


    print("每个链接已作为单独字典写入 json_input_path.json")
