"""
CWL2PlantUML aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PantUM diagrams](https://plantuml.com/).

CWL2PlantUML (c) 2025

CWL2PlantUML is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_loader.utils import (
    assert_process_contained,
    to_dict
)
from cwl_utils.parser import (
    Process,
    Workflow
)
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
from loguru import logger
from typing import (
    Any,
    List,
    Mapping,
    Union,
    TextIO,
    get_args,
    get_origin
)

import time

class DiagramType(Enum):
    '''The supported PlantUML diagram types'''
    ACTIVITY = auto()
    '''Represents the PlantUML `activity' diagram'''
    COMPONENT = auto()
    '''Represents the PlantUML `components' diagram'''
    CLASS = auto()
    '''Represents the PlantUML `class' diagram'''
    SEQUENCE = auto()
    '''Represents the PlantUML `sequence' diagram'''
    STATE = auto()
    '''Represents the PlantUML `state' diagram'''

# START custom built-in functions to simplify the CWL rendering

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

    if hasattr(typ, 'symbols'):
        return f"Enum: [ {', '.join([str(s.split('/')[-1]) for s in typ.symbols])} ]"

    if hasattr(typ, '__name__'):
        return type.__name__

    return str(type)

def _not_single_item_list(
    value : Any
) -> bool:
    return isinstance(value, list) and len(value) > 1

def _get_value_from_str_or_single_item_list(
    value : Any
) -> Any:
    return value[0] if isinstance(value, list) else value

def _get_version() -> str:
    try:
        return version("cwl2puml")
    except PackageNotFoundError:
        return 'N/A'

def _to_mapping(
    functions: List[Any]
) -> Mapping[str, Any]:
    mapping: Mapping[str, Any] = {}

    for function in functions:
        mapping[function.__name__[1:]] = function

    return mapping

_jinja_environment = Environment(
    loader=PackageLoader(
        package_name='cwl2puml'
    )
)
_jinja_environment.filters.update(
    _to_mapping(
        [
            _to_puml_name,
            _type_to_string,
            _get_value_from_str_or_single_item_list
        ]
    )
)
_jinja_environment.tests.update(
    _to_mapping(
        [ _not_single_item_list ]
    )
)

# END

# TODO maybe move this method in the loader
def _assert_connected_graph(index: Mapping[str, Process]):
    issues: List[str] = []
    for process in index.values():
        if any(isinstance(process, typ) for typ in get_args(Workflow)):
            for step in getattr(process, 'steps', []):
                if not index.get(step.run[1:]):
                    issues .append(f"- {process.id}.steps.{step.id}{step.run}")

    if issues:
        nl = '\n'
        raise ValueError(f"Detected unresolved links in the input $graph:\n{nl.join(issues)}")

def to_puml(
    cwl_document: Process | List[Process],
    diagram_type: DiagramType,
    output_stream: TextIO,
    workflow_id: str = 'main'
):
    '''
    Converts a CWL, given its document model, to a PlantUML diagram.

    Args:
        `cwl_document` (`Processes`): The Processes object model representing the CWL document
        `diagram_type` (`DiagramType`): The PlantUML diagram type to render
        `output_stream` (`Stream`): The output stream where serializing the PlantUML diagram

    Returns:
        `None`: none
    '''
    assert_process_contained(
        process=cwl_document,
        process_id=workflow_id
    )
    
    index = to_dict(cwl_document) if isinstance(cwl_document, list) else { workflow_id: cwl_document }

    _assert_connected_graph(index)

    template = _jinja_environment.get_template(f"{diagram_type.name.lower()}.puml")

    output_stream.write(
        template.render(
            version=_get_version(),
            timestamp=datetime.fromtimestamp(time.time()).isoformat(timespec='milliseconds'),
            workflows=index.values(),
            workflow_id=workflow_id,
            index=index
        )
    )
