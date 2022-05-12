import feedparser
import json
import pandas as pd

def parse_feed(ti, **kwargs):
    """Task que faz a chamada para um feed 
    e retorna via XCom as informações obtidas. 

    É esperado que um parâmetro 
    chamado feed_url seja passado via op_kwargs. 
    """
    parser = feedparser.parse(kwargs["feed_url"])
    ti.xcom_push(key='title', value=parser.feed.title)
    ti.xcom_push(key='subtitle', value=parser.feed.subtitle)
    ti.xcom_push(key='total_entries', value=len(parser.entries))
    ti.xcom_push(key='entries', value=json.dumps(parser.entries))


def compile_data(ti, **kwargs):
    """Task que a partir de uma lista de nome de taks 
    faz o pull das entradas delas e retorna um valor compilado. 

    É esperado que um parâmetro 
    chamado task_list seja passado via op_kwargs. 
    """
    compiled_data = []
    for task_name in kwargs["task_list"]:
        entries = ti.xcom_pull(key='entries', task_ids=[task_name])
        entries = json.loads(entries[0])
        for entry in entries:
            print(entry)
            item = {
                "title": entry.get("title"),
                "link": entry.get("link")
            }

            compiled_data.append(item)

    ti.xcom_push(key='compiled_entries', value=json.dumps(compiled_data))


def create_report(**kwargs):
    """
    Cria um relatório com base nas entradas compiladas.
    """
    entries = json.loads(kwargs["entries"])
    df = pd.DataFrame(entries)
    print(df.head(100))

