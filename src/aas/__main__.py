# Copyright (c) 2026 Durim Miziraj.
"""The starting script of the program."""


from aas.cli import main as cli_main

try:
    exit(cli_main())

except KeyboardInterrupt:
    SIGINT = 130

    print("Received interrupt signal, exiting the program.")
    exit(SIGINT)

except SystemExit as _exit:
    exit(_exit.code)
