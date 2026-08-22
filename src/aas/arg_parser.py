from argparse import (
    ArgumentParser,
    RawDescriptionHelpFormatter
)
from importlib.metadata import PackageMetadata, metadata
from typing import Any

class AASArgParser(ArgumentParser):
    """Parse command-line arguments for AAS."""

    def __init__(self) -> None:
        """Initialize the AAS argument parser."""

        project_metadata: PackageMetadata = metadata("aas")

        super().__init__(
            **self._usage_info(project_metadata)
        )

        self._add_version_argument(project_metadata)

    @staticmethod
    def _usage_info(
        project_metadata: PackageMetadata,
    ) -> dict[str, str | None]:
        """Build and return parser configuration."""

        command_spec = """
commands:
  load image PATH               load an image with PATH as ALIAS
  load image PATH as ALIAS      load an image with ALIAS
  render                        render the current image
  render ALIAS                  render an image with ALIAS
  render ALIAS to DESTINATION   render ascii to file at DESTINATION
  set ALIAS brightness FACTOR   set brightness to a multiple of FACTOR
  set ALIAS contrast FACTOR     set contrast to a multiple of FACTOR
  save session as SESSION_NAME  save the current session under SESSION_NAME
  load session as SESSION_NAME  load a session under SESSION_NAME
  info                          print session info
  quit                          exit the program

  (FACTOR >= 0; 1.0 = unchanged)
"""

        usage_info = {
            "prog": project_metadata["Name"],
            "description": f"CLI {project_metadata['Summary']}",
            "epilog": command_spec,
            "formatter_class": RawDescriptionHelpFormatter,
            "color": True
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

