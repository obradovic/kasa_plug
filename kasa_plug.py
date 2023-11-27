#
# Prints info about Kasa plug electrical usage
#
# USAGE:
#   First, make a handy bash alias:
#   > alias kasa-plug='python3.10 kasa_plug.py'
#
#   View all the plugs:
#   > kasa-plug
#
#   View only one of the plugs:
#   > kasa-plug --plug Veggie
#
# NOTES:
#   Python 3.11 prints a spurious error on exit, 3.10 works fine:
#   https://github.com/python/cpython/issues/109538
#
#   requirements.txt would be:
#   python-kasa
#

import argparse
import asyncio
from typing import Dict
from kasa import Discover

# from kasa import SmartStrip


def main():
    asyncio.run(main_async())


async def main_async():
    print("discovering...")
    found_devices = await Discover.discover()
    print("discovering complete\n")

    await print_info(found_devices, get_plug_name())


async def print_info(found_devices: Dict, plug_name: str):
    # device is an object: kasa.smartstrip.SmartStrip
    for ip, device in found_devices.items():
        await device.update()

        # device_type = device.device_type  # this is a: enum DeviceType
        mac = device.device_id
        print(f"    {device.alias} ip: {ip}, MAC: {mac}")

        for plug in device.children:
            if not plug_name or (plug_name and plug_name == plug.alias):
                await plug.update()
                emeter = plug.emeter_realtime

                state = "on"
                if not plug.is_on:
                    state = "off"

                print(f"    {plug.alias} {state}:")
                print(f"        voltage: {emeter.voltage}")
                print(f"        current: {emeter.current}")
                print(f"        power:   {emeter.power}")
                print(f"        total:   {emeter.total}")
                print()


def get_plug_name() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plug", help="The name of the plug")
    args, _ = parser.parse_known_args()
    return args.plug


if __name__ == "__main__":
    main()
