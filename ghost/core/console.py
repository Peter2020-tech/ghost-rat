"""
MIT License

Copyright (c) 2020-2024 Jman

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

import cmd
from ghost.core.device import Device
from ghost.core.loader import Loader


class Console(cmd.Cmd):
    """ Subclass of ghost.core module.

    This subclass of ghost.core modules is intended for providing
    main Ghost Framework console interface.
    """

    def __init__(self) -> None:
        super().__init__()
        cmd.Cmd.__init__(self)

        self.devices = {}
        self.banner = """%clear%end                                      .           :  .       : :
                              :  :   :  .            .  .         .  .   .       :    .     : :
                              :  :   :  .   .     :  .  .        :  :  .  .      : :    .   : : 
                       .  .   :  :   :  :  .   .  :  .  :      :   .    .  .     : :  .  .  . :
                       .  .   .  .   :  :     .      .  :     :   .      .  .    : :    .   . :
                       .    .    :   :  :     .      :  :    :   . .  .  .   .   : :      .   :
                        .   . .  .   :  :            :  :   :   .         .   .  : :        . :

--=[ %bold%whiteGhost Framework 8.0.0%end
--=[ Developed by Jman (%linehttps://encryton.com/%end)
"""

        self.prompt = '(ghost)> '
        self.loader = Loader()
        self.module_commands = self.load_modules()

    def load_modules(self) -> dict:
        """ Load modules and return a dictionary of available commands.

        :return dict: Dictionary containing module commands
        """
        loaded_modules = self.loader.load_modules()
        module_commands = {}

        for module_name, module_instance in loaded_modules.items():
            module_commands[module_name] = module_instance

        return module_commands

    def do_run_module(self, module_name: str) -> None:
        """ Run a loaded module.

        :param str module_name: Name of the module to run
        :return None: None
        """
        if module_name not in self.module_commands:
            print(f"Module '{module_name}' not found!")
            return

        module_instance = self.module_commands[module_name]
        module_instance.device = self.device  # Pass the device instance to the module

        module_instance.run(0, [])

    def do_exit(self, _) -> None:
        """ Exit Ghost Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].disconnect()
            del self.devices[device]

        raise EOFError

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        print('%clear', end='')

    def do_connect(self, address: str) -> None:
        """ Connect device.

        :param str address: device host:port or just host
        :return None: None
        """

        if not address:
            print("connect <host>:[port]")
            return

        address = address.split(':')

        if len(address) < 2:
            host, port = address[0], 5555
        else:
            host, port = address[0], int(address[1])

        device = Device(host=host, port=port)

        if device.connect():
            self.devices.update({
                len(self.devices): {
                    'host': host,
                    'port': str(port),
                    'device': device
                }
            })
            print("")

            print(
                f"Type %greendevices%end to list all connected devices.")
            print(
                f"Type %greeninteract {str(len(self.devices) - 1)}%end "
                "to interact with this device."
            )

    def do_devices(self, _) -> None:
        """ Show connected devices.

        :return None: None
        """

        if not self.devices:
            print("No devices connected.")
            return

        devices = []

        for device in self.devices:
            devices.append(
                (device, self.devices[device]['host'],
                 self.devices[device]['port']))

        print_table(
            "Connected Devices", ('ID', 'Host', 'Port'), *devices)

    def do_disconnect(self, device_id: int) -> None:
        """ Disconnect device.

        :param int device_id: device ID
        :return None: None
        """

        if not device_id:
            print("disconnect <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            print("Invalid device ID!")
            return

        self.devices[device_id]['device'].disconnect()
        self.devices.pop(device_id)

    def do_interact(self, device_id: int) -> None:
        """ Interact with device.

        :param int device_id: device ID
        """

        if not device_id:
            print("interact <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            print("Invalid device ID!")
            return

        print(f"Interacting with device {str(device_id)}...")
        self.devices[device_id]['device'].interact()

    def do_EOF(self, _):
        """ Catch EOF.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def default(self, line: str) -> None:
        """ Default unrecognized command handler.

        :param str line: line sent
        :return None: None
        """

        print(f"Unrecognized command: {line.split()[0]}!")

    def emptyline(self) -> None:
        """ Do something on an empty line.

        :return None: None
        """

        pass

    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """
        print(self.banner, translate=False)

        while True:
            try:
                cmd.Cmd.cmdloop(self)

            except (EOFError, KeyboardInterrupt):
                print(end='')
                break

            except Exception as e:
                print("An error occurred: " + str(e) + "!")
