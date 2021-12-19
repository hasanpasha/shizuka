
from . import List, prompt

def _get_episode_slug(self, episodes: List) -> str:
    seasons = {}
    for s in episodes:
        if s['season'] not in seasons.keys():
            seasons[s['season']] = {}

        this_season = seasons[s['season']]

        if s['episode'] in this_season.keys():
            continue

        this_season[s['episode']] = s['slug']

    season_number = self._media_season = self._get_season_number(seasons)
    episode_number = self._media_episode = self._get_episode_number(
        seasons, season_number)

    return seasons[season_number][episode_number]

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
