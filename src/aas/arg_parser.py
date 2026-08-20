from argparse import (
    ArgumentParser,
    RawDescriptionHelpFormatter,
)
from importlib.metadata import PackageMetadata, metadata
from typing import Any

class AASArgParser(ArgumentParser):
    """Parse command-line arguments for AAS."""

    def __init__(self) -> None:
        """Initialize the AAS argument parser."""

        project_metadata = metadata("aas")

        super().__init__(
            **self._usage_info(project_metadata)
        )

        self._add_version_argument(project_metadata)

    @staticmethod
    def _usage_info(
        project_metadata: PackageMetadata,
    ) -> dict[str, Any]:
        """Build and return parser configuration."""

        prog = project_metadata["Name"]
        description = f"CLI {project_metadata['Summary']}"

        epilog = """
commands:
  load PATH  load an image
  render     render a loaded image
  info       print information about the image file
  quit       exit the program
"""

        formatter_class = RawDescriptionHelpFormatter
        color = False

        usage_info = {
            "prog": prog,
            "description": description,
            "epilog": epilog,
            "formatter_class": formatter_class,
            "color": color,
        }

        return usage_info

    def _add_version_argument(
        self,
        project_metadata: PackageMetadata,
    ) -> None:
        """Add the version argument."""

        self.add_argument(
            "-v",
            "--version",
            action="version",
            version=(
                f"ASCII Art Studio "
                f"{project_metadata['Version']}"
            ),
        )

