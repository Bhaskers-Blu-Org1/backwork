"""Handle the life cycle and events of notifiers.

This module is responsible for initializing the notification handlers that are
enabled and routing incoming messages.
"""
import os
from lib import utils

current_path = os.path.dirname(os.path.realpath(__file__))
engines = utils.load_engines("monsoon.notifiers")
active_engines = []

def parse_args(parser):
    """Add command line arguments regarding notifiers."""
    parser.add_argument("-n", "--notify", action="append", dest="notifiers",
        help="enable a notifier, it can be used multiple times")

    for _, klass in engines.iteritems():
        klass.parse_args(parser)

def initialize(args, extra):
    """Enable notifiers that were activted via command line."""
    if args.notifiers is None:
        return

    for notifier in args.notifiers:
        if notifier in engines:
            engine = engines[notifier](args, extra)
            active_engines.append(engine)
        else:
            raise Exception("Invalid notifier '%s'.", notifier)

def notify(msg=""):
    """Route incoming messages to all active notifiers."""
    for engine in active_engines:
        engine.notify(msg)