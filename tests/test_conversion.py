# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cwl_loader import load_cwl_from_location
from cwl_utils.parser import Process
from cwl2puml import (
    DiagramType,
    to_puml
)
from io import StringIO
from typing import List
from unittest import TestCase

class Testloading(TestCase):

    def setUp(self):
        self.graph: Process | List[Process] = load_cwl_from_location(path='https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-1.cwl')

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
