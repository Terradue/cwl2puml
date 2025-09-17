"""
CWL2PlantUML aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PantUM diagrams](https://plantuml.com/).


CWL2PlantUML (c) 2025

CWL2PlantUML is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from . import (
    DiagramType,
    to_puml
)
from cwl_loader import load_cwl_from_location
from datetime import datetime
from loguru import logger
from pathlib import Path
from typing import Optional

import click
import sys
import time

@click.command()
@click.argument(
    'workflow',
    required=True)
@click.option(
    '--puml',
    type=click.Choice(
        DiagramType,
        case_sensitive=False
    ),
    required=True,
    help="The PlantUML diagram type."
)
@click.option(
    '--output',
    type=click.Path(
        path_type=Path
    ),
    required=False,
    help="Output file path"
)
def main(
    workflow: str,
    puml: DiagramType,
    output: Optional[Path] = None,
):
    '''
    Converts a CWL,m given its document model, to a PlantUML diagram.

    Args:
        `workflow` (`str`): The CWL workflow file (it can be an URL or a file on the File System)
        `puml` (`DiagramType`): The PlantUML diagram type to render
        `output` (`Path`): The output file where streaming the PlantUML diagram

    Returns:
        `None`: none
    '''
    start_time = time.time()

    cwl_document = load_cwl_from_location(path=workflow)

    logger.info('------------------------------------------------------------------------')

    if output:
        logger.info(f"Saving the new PlantUML Workflow diagram to {output}...")

        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w") as f:
            to_puml(
                cwl_document=cwl_document,
                diagram_type=puml,
                output_stream=f
            )

        logger.info(f"PlantUML Workflow {puml.name.lower()} diagram successfully rendered to {output}!")
    else:
        to_puml(
            cwl_document=cwl_document,
            diagram_type=puml,
            output_stream=sys.stdout
        )

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")
