"""
MIT License

Copyright (c) 2024-2026 Jman

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

import importlib.util
import os

from typing import Any


class Loader(object):
    """ Subclass of ghost.core module.

    This subclass of ghost.core module is intended for providing
    Ghost Framework loader.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def import_modules(path: str, device: Any) -> dict:
        """ Import modules for the specified device.

        :param str path: path to import modules from
        :param Any device: device to import modules for
        :return dict: dict of modules
        """

        modules = {}

        for mod in os.listdir(path):
            if mod == '__init__.py' or not mod.endswith('.py'):
                continue
            else:
                try:
                    module_path = os.path.join(path, mod)
                    spec = importlib.util.spec_from_file_location(module_path, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    module_instance = module.GhostModule()

                    if not hasattr(module_instance, 'details') or not hasattr(module_instance, 'run'):
                        raise ImportError(f"Module {mod} is missing required attributes 'details' or 'run'.")

                    module_instance.device = device
                    modules[module_instance.details['Name']] = module_instance
                except Exception as e:
                    print(f"Error importing module {mod}: {e}")

        return modules

    def load_modules(self, device) -> dict:
        """ Load modules for the specified device and get their commands.

        :param Device device: device to load modules for
        :return dict: dict of modules commands
        """

        modules_path = os.path.join(os.path.dirname(__file__), '..', 'modules')
        return self.import_modules(modules_path, device)
