# Copyright (c) 2026 Durim Miziraj.
"""Provide the command-line interface for AAS."""

# from aas.arg_parser import AASArgParser
from aas.controller.cli_controller import CLIController
from aas.model.domain_model import AASModel
from aas.view.view import CLIView


def main() -> int:
    """Initiate the CLI version of AAS.

    Returns:
        An exit success code.

    """
    # args = AASArgParser().parse_args()

    controller = CLIController()
    model = AASModel()
    view = CLIView()

    controller.add_observer(model)
    model.add_observer(view)

    controller.start()

    return 0
