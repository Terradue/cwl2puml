"""
CWL Loader (c) 2025

CWL Loader is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_loader import load_cwl_from_location
from cwl2puml import (
    DiagramType,
    to_puml
)
from io import StringIO
from unittest import TestCase

class Testloading(TestCase):

    def setUp(self):
        self.graph = load_cwl_from_location(path='https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-1.cwl')

    def tearDown(self):
        self.graph = None

    def _test_diagram(self, diagram_type: DiagramType):
        self.assertIsNotNone(self.graph, "Expected non null $graph, found None")
        self.assertIsInstance(self.graph, list, f"Expecting graph as list, found {type(self.graph)}")

        out = StringIO()
        to_puml(
            cwl_document=self.graph,
            workflow_id='pattern-1',
            diagram_type=diagram_type,
            output_stream=out
        )
        puml_output = out.getvalue()

        self.assertIsNotNone(puml_output, "Expected non null PlantUML text for {diagram_type.name()}, found None")
        self.assertGreater(len(puml_output), 0, "Expected non empty PlantUML text for {diagram_type.name()}")

    def test_components_diagram(self):
        self._test_diagram(DiagramType.COMPONENT)

    def test_class_diagram(self):
        self._test_diagram(DiagramType.CLASS)

    def test_sequence_diagram(self):
        self._test_diagram(DiagramType.SEQUENCE)

    def test_state_diagram(self):
        self._test_diagram(DiagramType.STATE)
