

from typing import List
import json
import requests
from urllib.parse import urlencode

from api.servers import Server
from api.servers import Status
from api.constants import Kinds

def KindEQ(kind: Kinds) -> str:
    opt = {Kinds.MOVIES: "movies", 
    Kinds.SERIES: "series"}
    return opt[kind]

class Cinemana(Server):
    id = 'cinemana'
    name = 'shabakaty cinemana'
    status = Status.ENABLED

    base_url = 'https://cinemana.shabakaty.com'
    base_api = base_url + '/api'
    search_url = base_api + '/android/AdvancedSearch?'
    videos = base_api + '/android/transcoddedFiles/id/{0}'
    episodes = base_api + '/android/videoSeason/id/{0}'
    translations = base_api + '/android/translationFiles/id/{0}'

    def __init__(self):
        # print(f"{self.id}: initializing...")
        if self.session is None:
            self.session = requests.Session()

    def get_data(self, *args, **kwargs):
        resp = self.session_get(*args, **kwargs)

        if resp.status_code != 200:
            return 

        return json.loads(resp.text)
    
    def search(self, keyword: str, **kwargs) -> List[dict[str, str, str]]:
        """Search for the media."""
        
        def buildURL(keyword, **kwargs):
            expected_params = {
                "kind": {
                    "site_eq": 'type',
                    "opt": lambda o: KindEQ(o),
                }
            }
            params = dict(videoTitle=keyword)
            for ex in kwargs.keys():
                if ex in expected_params:
                    kweq = expected_params[ex]
                    params.update({kweq["site_eq"]: kweq["opt"](kwargs[ex])})
            
            return self.search_url + urlencode(params) # URL to search result

        result_url = buildURL(keyword, **kwargs)

        # getting data
        json_data = self.get_data(result_url)
        
        if json_data == None:
            return

        return [
            dict(name=item['en_title'], year=item['year'], slug=item['nb'])
             for item in json_data ]


    def getVideos(self, slug) -> List[dict[str, str]]:
        """Get videos with different qualities for item"""
        videos_url = self.videos.format(slug)

        json_data = self.get_data(videos_url)

        if json_data == None:
            return

        return [
            dict(reso=video['resolution'], videoURL=video['videoUrl'])
            for video in json_data
        ]


    def getEpisodes(self, slug: str) -> List[dict[str, str, str]]:
        episodes_url = self.episodes.format(slug)

        json_data = self.get_data(episodes_url)

        if json_data == None:
            return

        return [
            dict(season=episode['season'], episode=episode['episodeNummer'], slug=episode['nb'])
            for episode in json_data
        ]


    def getTranslations(self, slug: str) -> List[dict[str, str, str]]:
        translation_url = self.translations.format(slug)

        json_data  = self.get_data(translation_url)

        if json_data == None:
            return

        return [
            dict(
                lang=trans['name'],
                extension=trans['extention'],
                fileURL=trans['file']
            )
            for trans in json_data['translations']
        ]
