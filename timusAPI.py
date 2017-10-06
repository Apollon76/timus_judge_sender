import os
import urllib.request
import pyquery
import pickle

path_to_cache = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'task_names_cache.data')

try:
    with open(path_to_cache, 'rb') as f:
        cache = pickle.load(f)
except Exception:
    cache = {}

def get_task_name(task_id: int):
    global cache

    name_by_id = dict(map(lambda x: (int(cache[x]), x), cache))
    if task_id in name_by_id:
        return name_by_id[task_id]
    cache = make_cache()
    name_by_id = dict(map(lambda x: (int(cache[x]), x), cache))
    if task_id in name_by_id:
        return name_by_id[task_id]
    return None

def get_task_id(task_name: str):
    global cache

    if task_name in cache:
        return cache[task_name]
    cache = make_cache()
    if task_name not in id_by_name:
        return None
    return id_by_name[task_name]

def make_cache():
    task_list_url = 'http://acm.timus.ru/problemset.aspx?space=1&page=all&locale=ru'
    with urllib.request.urlopen(task_list_url) as page:
        page_content = page.read()
    page_content = list(pyquery.PyQuery(page_content).items('td'))
    temp = []
    for i, s in enumerate(page_content):
        if s.attr('class') == 'name':
            temp.append((page_content[i - 1], s))
    page_content = map(lambda x: (x[0].contents(), x[1].items('a')), temp)
    id_by_name = dict(map(lambda x: (list(x[1])[0].contents()[0], x[0][0]), page_content))
    with open(path_to_cache, 'wb') as f:
        pickle.dump(id_by_name, f)
    return id_by_name

