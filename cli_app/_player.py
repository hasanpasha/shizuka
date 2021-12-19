
from . import List, MPVVideoPlayer, Kinds, os
from ._defaults import Defaults

# MPV Video Player
def _video_player(self, slug: str, verbose: bool = False) -> None:
    """The video player method uses mpv as default. """

    chosed_quality_url: str = self._choose_quality(slug)
    trans_files: List = self._get_trans_files(slug)

    cmd_args = ['mpv', ]

    if chosed_quality_url == None:
        return False

    cmd_args.append(f"{chosed_quality_url}")

    if len(trans_files) >= 1:
        for t in trans_files:
            cmd_args.append(f"--sub-file={t}")

    # no terminal output
    cmd_args.append("--no-terminal")

    if verbose:
        print('$ ' + ' '.join(cmd_args))

    # Save screenshots to data folder, with seperating medias
    # First make sure the data folder exist, if not make one
    if not os.path.exists(Defaults.DATA_FOLDER):
        os.mkdir(Defaults.DATA_FOLDER)

    # check for screenshots folder existance, or make one
    if not os.path.exists(Defaults.SCREENSHOTS_FOLDER):
        os.mkdir(Defaults.SCREENSHOTS_FOLDER)

    media_screenshots_path = os.path.join(
        Defaults.SCREENSHOTS_FOLDER,
        self._media_name
    )
    # check if the playing media have already folder, if not make one
    if not os.path.exists(media_screenshots_path):
        os.mkdir(media_screenshots_path)

    # Set directory, and quality for screenshots
    cmd_args.extend([
        # The path screenshots saved to
        f"--screenshot-directory={media_screenshots_path}",
        f"--screenshot-jpeg-quality={100}",
    ])

    # change screenshot filename template, and set media title
    if self._media_kind == Kinds.MOVIES:
        cmd_args.extend([
            f"--screenshot-template=%P",    # %p: Current playback time
            f"--force-media-title={self._media_name}"
        ])

    elif self._media_kind == Kinds.SERIES:
        cmd_args.extend([
            f"--screenshot-template=s{self._media_season}-e{self._media_episode}-%P",
            f"--force-media-title={self._media_name} s{self._media_season} e{self._media_episode}",
        ])

    # start playing the video
    video_player = MPVVideoPlayer()
    while True:
        video_process: bool = video_player.play_video(cmd_args)
        if video_process:   # if process returned True
            break   # end the loop

        # On error, Ask to retry playing the video
        elif self._continue(msg="Error on playing the videos, Retry? "):
            continue

        else:   # Else end the loop and return to the main loop
            break
