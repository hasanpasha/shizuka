
from . import prompt, Kinds

@property
def _get_search_options(self) -> dict[str, str, str]:
    return prompt([
        {
            'name': 'search_key',
            'type': 'input',
            'message': 'Enter a name to search',
        },
        {
            'name': 'media_type',
            'type': 'list',
            'message': 'select a media type: ',
            'choices': [dict(name=type) for type in [Kinds.MOVIES, Kinds.SERIES]],
            'when': lambda search_choices: search_choices['search_key'],
        },
        {
            'name': 'perform_search',
            'type': 'confirm',
            'message': 'Press any key to perform search or n to reset',
            'default': True,
            'when': lambda search_choices: search_choices['search_key'],
        }
    ])
