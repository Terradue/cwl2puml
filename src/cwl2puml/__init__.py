"""
CWL2PlantUML aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PantUM diagrams](https://plantuml.com/).


CWL2PlantUML (c) 2025

CWL2PlantUML is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_loader import (
    load_cwl_from_location,
    Processes,
    Stream
)
from cwl_utils.parser import Process
from datetime import datetime
from io import TextIOBase
from jinja2 import Environment
from loguru import logger
from pathlib import Path
from typing import (
    Any,
    Union,
    get_args,
    get_origin
)
import click
import enum
import sys
import time

_COMPONENTS_TEMPLATE = """@startuml
skinparam linetype ortho

{% for workflow in workflows %}
node "{{ workflow.class_ }} '{{ workflow.id }}'" {
    component "{{ workflow.id }}" as {{ workflow.id | to_puml_name }} {
    {% for input in workflow.inputs %}
        portin "{{ input.id }}" as {{ workflow.id | to_puml_name }}_{{ input.id | to_puml_name }}
    {% endfor %}
    {% for output in workflow.outputs %}
        portout "{{ output.id }}" as {{ workflow.id | to_puml_name }}_{{ output.id | to_puml_name }}
    {% endfor %}
    }

{% for step in workflow.steps %}
    component "{{ step.id }}" as {{ workflow.id | to_puml_name }}_{{ step.id | to_puml_name }} {
    {% for input in step.in_ %}
        portin "{{ input.id }}" as {{ workflow.id | to_puml_name }}_{{ step.id | to_puml_name }}_{{ input.id | to_puml_name }}
        {{ workflow.id | to_puml_name }}_{{ input.source | replace('/', '_') | to_puml_name }} .down.> {{ workflow.id | to_puml_name }}_{{ step.id | to_puml_name }}_{{ input.id | to_puml_name }}
    {% endfor %}

    {% for output in step.out %}
        portout "{{ output }}" as {{ workflow.id | to_puml_name }}_{{ step.id | to_puml_name }}_{{ output | to_puml_name }}
    {% endfor %}
    }
{% endfor %}
}
{% endfor %}

{% for workflow in workflows %}
    {% for output in workflow.outputs %}
        {% for outputSource in output.outputSource %}
{{ workflow.id | to_puml_name }}_{{ outputSource | replace('/', '_') | to_puml_name }} .up.> {{ workflow.id | to_puml_name }}_{{ output.id | to_puml_name }}
        {% endfor %}
    {% endfor %}

    {% for step in workflow.steps %}
{{ workflow.id | to_puml_name }}_{{ step.id | to_puml_name }} .right.> {{ step.run[1:] | to_puml_name }}
    {% endfor %}
{% endfor %}
@enduml
"""

_CLASS_TEMPLATE = '''@startuml

{% for workflow in workflows %}
class "{{ workflow.id }}" as {{ workflow.id | to_puml_name }} extends {{ workflow.class_ }} {
    __ Inputs __
    {% for input in workflow.inputs %}
    + {{ input.id }}: {{ input.type_ | type_to_string }}{% if input.default %} = {{ input.default }}{% endif %}
    {% endfor %}

    __ Outputs __
    {% for output in workflow.outputs %}
    + {{ output.id }}: {{ output.type_ | type_to_string }}
    {% endfor %}

    {% if workflow.steps is defined %}
    __ Steps __
        {% for step in workflow.steps %}
    - {{ step.id }}: {{ step.run[1:] | to_puml_name }}
        {% endfor %}
    {% endif %}
}

    {% if workflow.requirements %}
    package "Requirements" {
    {% for requirement in workflow.requirements %}
        {% if requirement.class_ %}
{{ workflow.id | to_puml_name }} --> {{ requirement.class_ }}
        {% endif %}
    {% endfor %}
    }
    {% endif %}

    {% if workflow.hints %}
    package "Hints" {
    {% for hint in workflow.hints %}
        {% if hint.class_ %}
{{ workflow.id | to_puml_name }} --> {{ hint.class_ }}
        {% endif %}
    {% endfor %}
    }
    {% endif %}
{% endfor %}

{% for workflow in workflows %}
    {% for step in workflow.steps %}
{{ workflow.id | to_puml_name }} --> {{ step.run[1:] | to_puml_name }}
    {% endfor %}

    {% for input in workflow.inputs %}
        {% if input.doc or input.label %}
note left of {{ workflow.id | to_puml_name }}::{{ input.id }}
    {% if input.doc %}{{ input.doc }}{% else %}{{ input.label }}{% endif %}
end note
        {% endif %}
    {% endfor %}
{% endfor %}
@enduml
'''

class DiagramType(enum.Enum):
    '''The supported PlantUML diagram types'''
    COMPONENTS = _COMPONENTS_TEMPLATE
    '''Represents the PlantUML `components' diagram'''
    CLASS = _CLASS_TEMPLATE
    '''Represents the PlantUML `class' diagram'''

def _to_puml_name(identifier: str) -> str:
    return identifier.replace('-', '_')

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

def to_puml(
    cwl_document: Processes,
    diagram_type: DiagramType,
    output_stream: Stream
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
    env = Environment()
    env.filters['to_puml_name'] = _to_puml_name
    env.filters['type_to_string'] = _type_to_string

    string_template = diagram_type.value
    template = env.from_string(string_template)

    workflows = cwl_document if isinstance(cwl_document, list) else [cwl_document]

    output_stream.write(template.render(workflows=workflows))

@click.command()
@click.option("--workflow", required=True, help="The CWL workflow file (it can be an URL or a file on the File System)")
@click.option('--puml', type=click.Choice(DiagramType, case_sensitive=False), required=True, help="The PlantUML diagram type.")
@click.option("--output", type=click.Path(path_type=Path), required=True, help="Output file path")
def main(
    workflow: str,
    puml: DiagramType,
    output: Path
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

    output.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Saving the new PlantUML Workflow diagram to {output}...")

    with output.open("w") as f:
        to_puml(
            cwl_document=cwl_document,
            diagram_type=puml,
            output_stream=f
        )

    logger.info(f"PlantUML Workflow {puml.name.lower()} diagram successfully rendered to {output}!")

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")
