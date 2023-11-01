#
import concurrent.futures
import subprocess
from typing import List
import signal


class PoliteExit(Exception):
    pass

def handle_signal(signum, frame):
    raise PoliteExit()

class MPVVideoPlayer:
    """
        play video using mpv player from command line
        the process will be in another thread..
    """

    def __init__(self) -> None:
        # Use signal handler to throw exception which can be 
        #+ caught to allow polite exit.
        end_signals = [
            signal.SIGTERM,  # 15
            signal.SIGABRT,  # 6
            signal.SIGQUIT,  # 3
        ]
        for sig in end_signals:
            signal.signal(sig, handle_signal)

    def _player(self, args: List) -> bool:
        try:
            process = self.player_process = subprocess.Popen(args)
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
            process = executor.submit(self._player, args)
            process_args = {process: args}
            try:
                for process_future in concurrent.futures.as_completed(process_args):
                    return process_future.result()

            # exit norammly on keyborad interrupt
            except KeyboardInterrupt:
                return True

            except PoliteExit:
                # On receiving SIG* signal
                self.player_process.terminate()

                # And cancel the process if still running
                process.cancel()

                # End the script running, with returning error code
                exit(3) # Quit