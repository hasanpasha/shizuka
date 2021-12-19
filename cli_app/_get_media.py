
from . import List, prompt

def _choose_media(self, media_list: List) -> str:
    _list = [dict(name=f"{media['name']} ({media['year']})", slug=media['slug'])
            for media in media_list]

    select_media = prompt([
        {
            'name': 'media_choice',
            'message': 'select media: ',
            'type': 'list',
            'choices': _list
        }
    ])
    for i in _list:
        if i['name'] == select_media['media_choice']:
            # set_media_name
            self._media_name = i['name']
            return i['slug']

def _get_trans_files(self, slug: str) -> List:
    trans_list = self.server.getTranslations(slug)

    _list = [dict(
        name=f"{tran['lang'].strip()} ({tran['extension'].strip()})",
        fileURL=tran['fileURL'])
        for tran in trans_list]

    choose_tran = prompt([
        {
            'name': 'trans',
            'type': 'checkbox',
            'message': 'choose on or more translation file: ',
            'choices': [dict(name=tran['name'])
                        for tran in _list],
            # 'validate': lambda choose_tran: 'You must choose at least one topping.' if len(choose_tran) == 0 else True
        },
    ])

    return [
        i['fileURL'] for i in _list if i['name'] in choose_tran['trans']
    ]


def _choose_quality(self, slug: str) -> str:
    qualities = self.server.getVideos(slug)
    choose_quality = prompt([
        {
            'name': 'quality',
            'type': 'list',
            'message': 'select video quality',
            'choices': [dict(name=video['reso']) for video in qualities]
        }
    ])

    selected_quality = choose_quality['quality']
    for i in qualities:
        if i['reso'] == selected_quality:
            return i['videoURL']
