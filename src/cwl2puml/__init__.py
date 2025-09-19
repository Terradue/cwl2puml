"""
CWL2PlantUML aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PantUM diagrams](https://plantuml.com/).


CWL2PlantUML (c) 2025

CWL2PlantUML is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser import Process
from datetime import datetime
from enum import (
    auto,
    Enum
)
from importlib.metadata import (
    version,
    PackageNotFoundError
)
from jinja2 import (
    Environment,
    PackageLoader
)
from typing import (
    Any,
    List,
    Union,
    TextIO,
    get_args,
    get_origin
)

import time

class DiagramType(Enum):
    '''The supported PlantUML diagram types'''
    COMPONENTS = auto()
    '''Represents the PlantUML `components' diagram'''
    CLASS = auto()
    '''Represents the PlantUML `class' diagram'''
    SEQUENCE = auto()
    '''Represents the PlantUML `sequence' diagram'''
    STATE = auto()
    '''Represents the PlantUML `state' diagram'''

def _to_puml_name(identifier: str) -> str:
    return identifier.replace('-', '_').replace('/', '_')

def _type_to_string(typ: Any) -> str:
    if get_origin(typ) is Union:
        return " or ".join([_type_to_string(inner_type) for inner_type in get_args(typ)])

    if isinstance(typ, list):
        return f"[ {', '.join([_type_to_string(t) for t in typ])} ]"

    if hasattr(typ, "items"):
        return f"{_type_to_string(typ.items)}[]"

    if isinstance(typ, str):
        return typ

    return typ.__name__

def _get_version() -> str:
    try:
        return version("cwl2puml")
    except PackageNotFoundError:
        return 'N/A'

_jinja_environment = Environment(
    loader=PackageLoader(
        package_name='cwl2puml'
    )
)
_jinja_environment.filters['to_puml_name'] = _to_puml_name
_jinja_environment.filters['type_to_string'] = _type_to_string

def to_puml(
    cwl_document: Process | List[Process],
    diagram_type: DiagramType,
    output_stream: TextIO
):
    '''
    Converts a CWL,m given its document model, to a PlantUML diagram.

    Args:
        `cwl_document` (`Processes`): The Processes object model representing the CWL document
        `diagram_type` (`DiagramType`): The PlantUML diagram type to render
        `output_stream` (`Stream`): The output stream where serializing the PlantUML diagram

    Returns:
        `None`: none
    '''
    template = _jinja_environment.get_template(f"{diagram_type.name.lower()}.puml")

    workflows = cwl_document if isinstance(cwl_document, list) else [cwl_document]

    output_stream.write(
        template.render(
            version=_get_version(),
            timestamp=datetime.fromtimestamp(time.time()).isoformat(timespec='milliseconds'),
            workflows=workflows
        )
    )
