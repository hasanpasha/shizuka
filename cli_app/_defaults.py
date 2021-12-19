
# filename: _defaults.py
# This will contain the default options

from . import Kinds, os

class Defaults:
    SERVER = 'cinemana'
    DATA_FOLDER = os.path.join(
        os.path.split(
            # get real path if the running file is link from this file
            os.path.realpath(__file__)  # This will return the file path not the directory
        )[0],   #+ so I split it and choose only the dir path
        'data'
        )
    SCREENSHOTS_FOLDER = os.path.join(DATA_FOLDER, 'screenshots')
    KIND = Kinds.MOVIES