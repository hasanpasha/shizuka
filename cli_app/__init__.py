#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.server_utils import ServerUtils
from utils.video_player import MPVVideoPlayer
from api.constants import Kinds
from PyInquirer import prompt
from typing import List
import os


class Main:
    """ main app that run servers and get user commands """
    
    # Imports
    from ._server import _choose_server
    from ._series_case import (_get_episode_number,
                               _get_episode_slug,
                               _get_season_number)
    from ._search import _get_search_options
    from ._player import _video_player
    from ._get_media import (_choose_media,
                             _choose_quality,
                             _get_trans_files)
    from ._data import (
        _media_info,
        _clear_media_info,
        _media_name,
        _media_kind,
        _media_season,
        _media_episode,
    )
    from ._utils import clear_console, _continue
    from ._defaults import Defaults
    
    def __init__(self) -> None:    
        # properties
        self.server = None

        self.clear_console()  # Clear cmd when start
        self._choose_server()    # Run one time on start to select the server
        
        # To add args...         

    def run(self, first_run: bool = True) -> None:
        while True:
            # get user commands
            if not first_run:
                self.clear_console()
                self._clear_media_info()
                if not self._continue("Continue: "):
                    break
            
            first_run = False

            search_options = self._get_search_options
            if not search_options['search_key'] or not search_options['perform_search']:
                continue

            # edit media info
            self._media_kind = search_options['media_type']
            
            search_result = self.server.search(
                search_options['search_key'], kind=self._media_kind)
            chosed_media_slug = self._choose_media(search_result)

            if self._media_kind == Kinds.MOVIES:
                self._video_player(chosed_media_slug)
                continue

            elif self._media_kind == Kinds.SERIES:
                episodes = self.server.getEpisodes(chosed_media_slug)

                while True:
                    chosed_episode_slug = self._get_episode_slug(episodes)
                    self._video_player(chosed_episode_slug)
                    if self._continue(msg="do you wnat to play another episode: "):
                        self.clear_console()
                        continue
                    break
            # since this is the end it will return to 
            #+ the beginning of the main loop, just like using continue