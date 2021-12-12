#
import concurrent.futures
import subprocess
from typing import List

class MPVVideoPlayer:
    """
        play video using mpv player from command line
        the process will be in another thread..
    """

    def _player(self, args: List) -> bool:
        try:
            process = subprocess.Popen(args)
            process.wait()

        except Exception as e:
            print(e)
            return False

        else:
            # get command return code
            if process.poll() != 0:
                return False
            return True

        finally:
            # free the process
            process.terminate()

    def play_video(self, args: List) -> bool:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            process_args = {executor.submit(self._player, args): args}
            try:
                for process_future in concurrent.futures.as_completed(process_args):
                    return process_future.result()

            # exit norammly on keyborad interrupt
            except KeyboardInterrupt:
                return True