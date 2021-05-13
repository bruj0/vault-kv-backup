import argparse
from argparse import ArgumentParser
from textwrap import dedent

from pkg_resources import get_distribution


class ArgParser(ArgumentParser):
    def __init__(self):

        __version__ = get_distribution('vmb').version
        description = f"Version {__version__}\nBackup KV backend and other configuration and encrypt it via the transit secret engine"

        super(ArgParser, self).__init__(
            description=dedent(description),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        self.add_argument("out_file",
                          help="Output file where data will be written")

        self.add_argument(
            "--log-to-file",
            help="Log output to a file (vmb.log if no argument is given)",
            nargs="?",
            const="vmb.log",
        )

        self.add_argument(
            "--stdout",
            help="Log output stdout",
            action="store_true",
            default=False
        )

        self.add_argument(
            "--debug",
            help="Log debug information (only relevant if --stdout or --log-to-file is passed)",
            action="store_true",
            default=False,
        )

        self.add_argument(
            "--version",
            help="Version of vmb",
            action="version",
            version=f"{__version__}"
        )
        self.add_argument(
            "--dry-run",
            help="Dont make any outbound requests",
            action="store_true",
            default=False
        )
