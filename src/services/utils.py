from typing import Union

FIELD_MAPPING = {'imdb_rating': 'rating'}  # поля входной и выходной модели отличаются


def get_sort_body(sort: str):
    order = 'desc' if sort.startswith('-') else 'asc'
    field = sort.removeprefix('-')
    if field in FIELD_MAPPING.keys():
        field = FIELD_MAPPING[field]
    return get_sort_query(field, order)


def get_nested_term_query(field: str, request: Union[str, list]):
    term_value = "term"
    if type(request) == list:
        term_value += "s"
    query = {"query": {
        "nested": {
            "path": field,
            "query": {
                "bool": {
                    "must": [
                        {term_value: {
                            f"{field}.id": request}}
                    ]
                }
            }
        }
    }}
    return query


def get_base_match_query(search_field: str, request: str):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {search_field: request}}
                ]
            }
        }
    }
    return query


def get_base_multimatch_query(search_fields: list[str], request: str):
    query = {
        "query": {
            "multi_match": {
                "query": request,
                "fields": search_fields
            }
        }
    }
    return query


def get_films_by_person_query(uuid: str):
    query = {
        "query": {
            "term": {
                "person_ids": uuid
            }
        }
    }
    return query


def get_pagination_query(page_number: int, page_size: int):
    return {"from": page_number * page_size, "size": page_size}


def get_sort_query(field: str = 'rating', order: str = 'desc'):
    return {"sort": {field: order}}
