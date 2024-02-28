"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ghost.core.console import Console


def cli() -> None:
    """ Ghost Framework command-line interface.

    :return None: None
    """

    console = Console()
    console.shell()

def start_command_line_interface() -> None:
    """Start the Ghost Framework command-line interface.

    This function initializes the Ghost Framework command-line interface by creating
    a Console instance and launching the interactive shell.

    :return: None
    """
    try:
        # Create an instance of the Console class
        ghost_console = Console()

        # Launch the interactive shell
        ghost_console.shell()

    except Exception as e:
        print(f"Error starting the command-line interface: {e}")