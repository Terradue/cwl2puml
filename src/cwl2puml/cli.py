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
    required=True
)
@click.option(
    '--workflow-id',
    required=True,
    help="ID of the main Workflow"
)
@click.option(
    '--output',
    type=click.Path(
        path_type=Path
    ),
    required=True,
    help="Output directory path"
)
def main(
    workflow: str,
    workflow_id: str,
    output: Path,
):
    '''
    Converts a CWL, given its document model, to a PlantUML diagram.

    Args:
        `workflow` (`str`): The CWL workflow file (it can be an URL or a file on the File System)
        `workflow-id` (`str`): The ID of the main Workflow to render
        `output` (`Path`): The output file where streaming the PlantUML diagram

    Returns:
        `None`: none
    '''
    start_time = time.time()

    cwl_document = load_cwl_from_location(path=workflow)

    logger.info('------------------------------------------------------------------------')

    output.mkdir(parents=True, exist_ok=True)

    for diagram_type in DiagramType:
        target = Path(output, f"{diagram_type.name.lower()}.puml")
        logger.info(f"Saving PlantUML {diagram_type.name.lower()} diagram to {target}...")

        try:
            with target.open("w") as f:
                to_puml(
                    cwl_document=cwl_document,
                    workflow_id=workflow_id,
                    diagram_type=diagram_type,
                    output_stream=f
                )

            logger.success(f"PlantUML {diagram_type.name.lower()} diagram successfully rendered to {target}!")
        except Exception as e:
            logger.error(f"An unexpected error occurred while rendering PlantUML {diagram_type.name.lower()} diagram to {target}: {e}")

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")
