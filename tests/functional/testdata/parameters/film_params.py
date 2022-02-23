from functional.testdata.parameters.genre_params import NONEXISTENT_GENRE_ID, \
    EXISTENT_GENRE_ID

NONEXISTENT_FILM_ID = '135c3882-129a-472d-8f3a-bf84014b6537'

SORT_PARAMS_VALID = [{'sort': 'imdb_rating'},
                     {'sort': '-imdb_rating'}, ]

SORT_PARAMS_INVALID = [{'sort': 'anyfield'},
                       {'sort': '-anyfield'}, ]

PAGE_PARAMS_VALID = [
    {'page_size': 5, 'page_number': 20},
    {'page_size': 5, 'page_number': 10},
    {'page_size': 5, 'page_number': 0},
]

PAGE_PARAMS_INVALID = [
    {'page_size': -5, 'page_number': 20},
    {'page_size': 5, 'page_number': -10},
    {'page_size': 5, 'page_number': 30},
]

FILTER_PARAMS_VALID = [{'filter_genre': EXISTENT_GENRE_ID}, ]

FILTER_PARAMS_INVALID = [{'filter_genre': NONEXISTENT_GENRE_ID}, ]

LIST_PARAMETERS_VALID = [
    {'sort': '-imdb_rating', 'filter_genre': EXISTENT_GENRE_ID,
     'page_size': 5, 'page_number': 20}
]

FILM_BASE_PARAMS = [
    {},
    {'sort': 'imdb_rating'},
    {'sort': '-imdb_rating'},
    {'page_size': 5, 'page_number': 20},
    {'sort': '-imdb_rating', 'filter_genre': NONEXISTENT_GENRE_ID,
     'page_size': 5, 'page_number': 20},
]

FILM_PARAMS = FILM_BASE_PARAMS + [{'filter_genre': NONEXISTENT_GENRE_ID}, {}]
