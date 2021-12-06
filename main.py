#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from sys import argv
# from _typeshed import Self
# import argparse
from api.utils.server_utils import ServerUtils
from api.constants import Kinds
from PyInquirer import prompt
from typing import List
import os
import subprocess

class Defaults:
    SERVER = 'cinemana'
    KIND = Kinds.MOVIES



def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


class Main:
    """ main app that run servers and get user commands """
    def __init__(self) -> None:
        
        # properties
        self.server = None

        clear_console()  # Clear cmd when start
        self.choose_server()    # Run one time on start to select the server
        

        # To add args...
         
    def choose_server(self):
        if self.server != None:
            return

        su = ServerUtils()
        servers = su.servers_list
        servers_ids = [ dict(name=server['id']) for server in servers ]

        answers = prompt([
            {   
                'name': 'server_name',
                'type': 'list',
                'message': 'choose server: ',
                'choices': servers_ids,
                'when': lambda _: len(servers) > 1
            }
        ])

        try:
            cls = su.get_class_by_id(answers['server_name'])
        except KeyError:
            print(
                f"Selected {servers_ids[0]['name']}, 'cause there is only one server... ")
            cls = su.get_class_by_id(servers_ids[0]['name'])

        if cls == None:
            print("Error on getting a class... ")
            exit(1)

        self.server = cls


    def run(self, first_run: bool = True) -> None:
        while True:
            # get user commands

            if not first_run:
                clear_console()
                if not self._continue("Continue: "):
                    break
            
            first_run = False

            search_options = self._get_search_options
            if not search_options['search_key'] or not search_options['perform_search']:
                continue
            
            search_result = self.server.search(
                search_options['search_key'], kind=search_options['media_type'])
            chosed_media_slug = self._choose_media(search_result)

            if search_options['media_type'] == Kinds.MOVIES:
                player = self._video_player(chosed_media_slug)
                if player:
                    continue

            elif search_options['media_type'] == Kinds.SERIES:
                episodes = self.server.getEpisodes(chosed_media_slug)

                while True:
                    chosed_episode_slug = self._get_episode_slug(episodes)
                    player = self._video_player(chosed_episode_slug)
                    if player and self._continue(msg="do you wnat to play another episode: "):
                        clear_console()
                        continue
                    break
                
    
    # MPV Video Player
    def _video_player(self, slug: str, active: bool = True) -> bool:
        chosed_quality_url: str = self._choose_quality(slug)
        trans_files: List = self._get_trans_files(slug)

        cmd_args = ['mpv', ]

        if chosed_quality_url == None:
            return False
        
        cmd_args.append(f"{chosed_quality_url}")

        if len(trans_files) >= 1:
            for t in trans_files:
                cmd_args.append(f"--sub-file={t}")

        # execute command line command
        player_process = subprocess.Popen(cmd_args)

        print('$ ' + ' '.join(cmd_args))
        while active:
            if player_process.poll() != None:
                break

        player_process.terminate()
        return True

    def _continue(self, default: bool = True, msg: str = "do you wanna to continue") -> bool:
        choice =  prompt([
            {
                'name': 'continue',
                'type': 'confirm',
                'message': msg,
                'default': default
            }
        ])
        return choice['continue']

    def _get_episode_slug(self, episodes: List) -> str:
        seasons = {}
        for s in episodes:
            if s['season'] not in seasons.keys():
                seasons[s['season']] = {}

            this_season = seasons[s['season']]

            if s['episode'] in this_season.keys():
                continue

            this_season[s['episode']] = s['slug']

        season_number = self._get_season_number(seasons)
        episode_number = self._get_episode_number(seasons, season_number)

        return seasons[season_number][episode_number]

    def _get_trans_files(self, slug: str) -> List:
        trans_list = self.server.getTranslations(slug)

        _list = [ dict(
                name=f"{tran['lang'].strip()} ({tran['extension'].strip()})",
                fileURL=tran['fileURL'])
            for tran in trans_list ]

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

    def _get_season_number(self, seasons: dict) -> str:

        # get the first season number
        def default_season() -> str:
            s_l_o_s = sorted([int(v) for v in seasons.keys()])[0]
            return str(s_l_o_s)

        while True:
        
            chosed_season = prompt([
                {
                    'name': 'season',
                    'type': 'input',
                    'message': f'choose season [{default_season()} - {len(seasons)}]',
                    'when': lambda _: (len(seasons) > 1),
                },
            ])
            

            try:
                s_n = chosed_season['season']
                
                # if choesn bigger >= first season number, and <= number of seasons
                if int(s_n) >= int(default_season()) and int(s_n) <= len(seasons):
                    return s_n

            except KeyError:
                return default_season()

            except ValueError:
                print("Pleas Enter a number :(")


    def _get_episode_number(self, seasons: dict, season_number) -> str:

        # get the first episode number
        def default_episode() -> str:
            e_l_o_s = sorted([int(v)
                             for v in seasons[season_number].keys()])[0]
            return str(e_l_o_s)

        while True:
            chosed_episode = prompt([
                {
                    'name': 'episode',
                    'type': 'input',
                    'message': 'enter number',
                    'message': f"choose episode [1 - {len(seasons[season_number])}]",
                    'when': lambda _: (len(seasons[season_number]) > 1),
                },
            ])

            
            try:
                e_n = chosed_episode['episode']
                
                # if choesn bigger >= first episode number, and <= number of episodes
                if (int(e_n) >= int(default_episode()) and 
                int(e_n) <= len((seasons[season_number]))):
                    return e_n

            # if the user input is not number  
            except ValueError:
                print("Pleas Enter a number :(")

            # if there is just one episode
            except KeyError:
                return default_episode()
            

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
        


    def _choose_media(self, media_list: List) -> str:
        _list = [ dict(name=f"{media['name']} ({media['year']})", slug=media['slug']) 
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
                return i['slug']
        

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


if __name__ == '__main__':
    main_app = Main()
    main_app.run()