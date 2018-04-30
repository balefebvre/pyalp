import argparse

from .handle import handle  # TODO clean line.


# Command-line parsing.
parser = argparse.ArgumentParser()
parser.add_argument("-umd", "--use-mock-dmd", action="store_true",
                    help="use a mock micromirror device (development purpose)")
parser.add_argument("-ni", "--no-interpreter", action="store_true",
                    help="don't start the interpreter (development purpose)")
args = parser.parse_args()


# Handle device.
dmd = handle(mock=args.use_mock_dmd)


# Start interpreter (if necessary).
if args.no_interpreter:
    pass
else:
    import IPython
    from traitlets.config import Config
    config = Config()
    config.InteractiveShell.colors = 'Neutral'
    config.InteractiveShell.confirm_exit = False
    config.InteractiveShell.separate_in = ''
    config.InteractiveShell.banner1 = ""
    config.InteractiveShell.banner2 = ""
    IPython.embed(config=config)
    # IPython.embed(display_banner=False)


# Release device.
dmd.release()
