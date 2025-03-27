# Chatter Blocker for Linux
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Python implementation of a chatter blocker (e.g. for mechanical keyboard chatter) for Linux.**

This project is inspired by [Keyboard Chattering Fix for Linux](https://github.com/finkrer/KeyboardChatteringFix-Linux).

## Installation

Either download or clone this repository. After that, run the command below to automatically create a virtual Python environment and download the required packages.

```bash
make all
```

## Configuration

Execute the following command to perform an initial setup, which will then place a `chatterblocker.conf` at `/etc/chatterblocker.conf`. The setup will guide you through available options.

```bash
$ dist/chatterblocker/chatterblocker
```

In the resulting file you can also add **excluded keys** with the `exclude=` option. There you will need to insert the specific input event codes, as they can be found in [linux/input-event-codes.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h).

## Usage

To use the software simply run the binary file located at `dist/chatterblocker/chatterblocker`.

## Automate

You can create a systemd-service simply by running the command below.

```bash
make service
```

This will create a `chatter-blocker-py.service` file located at `/usr/lib/systemd/system/chatter-blocker-py.service` that points to the binary located here. The command simultaneously enables the service, to make it automatically start up on boot.

## License

Distributed under the MIT License. See `LICENSE` for more information.
