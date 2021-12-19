
from . import Kinds


@property
def _media_info(self) -> dict[str, str, str, str]:
    # currenly playing media info
    return {
        'name': None,
        'kind': None,
        'season': None,
        'episode': None,
    }

@property
def _media_name(self) -> str:
    return self._media_info['name']

@_media_name.setter
def _media_name(self, name: str) -> None:
    self._media_info['name'] = name

@property
def _media_kind(self) -> Kinds:
    return self._media_info['kind']

@_media_kind.setter
def _media_kind(self, kind: Kinds) -> None:
    self._media_info['kind'] = kind

@property
def _media_season(self) -> int:
    return self._media_info['season']

@_media_season.setter
def _media_season(self, season: int) -> None:
    self._media_info['season'] = season

@property
def _media_episode(self) -> int:
    return self._media_info['episode']

@_media_episode.setter
def _media_episode(self, episode: int) -> None:
    self._media_info['episode'] = episode

def _clear_media_info(self):
    for key in self._media_info.keys():
        self._media_info[key] = None
