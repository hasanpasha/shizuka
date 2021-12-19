
from . import os, prompt

# Should be signed as static method
# method_name = staticmethod(function)

def clear_console(self) -> None:
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def _continue(self,
              default: bool = True,
              msg: str = "do you wanna to continue") -> bool:
    choice = prompt([
        {
            'name': 'continue',
            'type': 'confirm',
            'message': msg,
            'default': default
        }
    ])
    return choice['continue']
