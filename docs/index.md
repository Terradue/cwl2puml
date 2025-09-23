# Introduction 

This project aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PlantUML diagrams](https://plantuml.com/).

## Installation

```
pip install cwl2puml
```

or, for early adopters:

```
pip install --no-cache-dir git+https://github.com/Terradue/cwl2puml@main
```

## CLI execution

```
Usage: cwl2puml [OPTIONS] WORKFLOW

  Converts a CWL, given its document model, to a PlantUML diagram.

  Args:     `workflow` (`str`): The CWL workflow file (it can be an URL or a
  file on the File System)     `workflow-id` (`str`): The ID of the main
  Workflow to render     `output` (`Path`): The output file where streaming
  the PlantUML diagram     `convert_image` (`bool`): Flag to ton on/off the
  image generation (on, by default)     `puml_server` (`str`): The host of a
  PlantUML as a service server (uml.planttext.com by default)
  `image_format` (`ImageFormat`): The output image format of the PlantUML
  diagram ('png' by default)

  Returns:     `None`: none

Options:
  --workflow-id TEXT        ID of the main Workflow  [required]
  --output PATH             Output directory path  [required]
  --convert-image BOOLEAN   Flag to ton on/off the image generation (on, by
                            default)
  --puml-server TEXT        The host of a PlantUML as a service server
                            (uml.planttext.com by default)
  --image-format [png|svg]  The output image format of the PlantUML diagram
                            ('png' by default)
  --help                    Show this message and exit.
```

i.e.

```
cwl2puml \
    --workflow-id main \
    --output . \
    --convert-image no \
    https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl
```

Output would be

```
2025-09-22 16:22:42.498 | DEBUG    | cwl_loader:load_cwl_from_location:213 - Loading CWL document from https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl...
2025-09-22 16:22:42.687 | DEBUG    | cwl_loader:_load_cwl_from_stream:216 - Reading stream from https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl...
2025-09-22 16:22:42.727 | DEBUG    | cwl_loader:load_cwl_from_stream:190 - CWL data of type <class 'ruamel.yaml.comments.CommentedMap'> successfully loaded from stream
2025-09-22 16:22:42.727 | DEBUG    | cwl_loader:load_cwl_from_yaml:135 - No needs to update the Raw CWL document since it targets already the v1.2
2025-09-22 16:22:42.727 | DEBUG    | cwl_loader:load_cwl_from_yaml:137 - Parsing the raw CWL document to the CWL Utils DOM...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:150 - Raw CWL document successfully parsed to the CWL Utils DOM!
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:152 - Dereferencing the steps[].run...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:70 - Checking if https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl#stac must be externally imported...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:74 - run_url: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl - uri: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:70 - Checking if https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl#rio_stack must be externally imported...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:74 - run_url: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl - uri: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:70 - Checking if https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl#rio_warp_stack must be externally imported...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:74 - run_url: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl - uri: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:70 - Checking if https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl#rio_color must be externally imported...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_on_process:74 - run_url: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl - uri: https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:159 - steps[].run successfully dereferenced! Now dereferencing the FQNs...
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:163 - CWL document successfully dereferenced!
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:166 - Sorting Process instances by dependencies....
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:load_cwl_from_yaml:168 - Sorting process is over.
2025-09-22 16:22:43.285 | DEBUG    | cwl_loader:_load_cwl_from_stream:224 - Stream from https://raw.githubusercontent.com/eoap/how-to/refs/heads/main/cwl-workflows/conditional-workflows.cwl successfully load!
2025-09-22 16:22:43.286 | INFO     | cwl2puml.cli:main:66 - ------------------------------------------------------------------------
2025-09-22 16:22:43.286 | INFO     | cwl2puml.cli:main:72 - Saving PlantUML activity diagram to activity.puml...
2025-09-22 16:22:43.301 | SUCCESS  | cwl2puml.cli:main:83 - PlantUML activity diagram successfully rendered to activity.puml!
2025-09-22 16:22:43.301 | INFO     | cwl2puml.cli:main:72 - Saving PlantUML component diagram to component.puml...
2025-09-22 16:22:43.325 | SUCCESS  | cwl2puml.cli:main:83 - PlantUML component diagram successfully rendered to component.puml!
2025-09-22 16:22:43.325 | INFO     | cwl2puml.cli:main:72 - Saving PlantUML class diagram to class.puml...
2025-09-22 16:22:43.346 | SUCCESS  | cwl2puml.cli:main:83 - PlantUML class diagram successfully rendered to class.puml!
2025-09-22 16:22:43.347 | INFO     | cwl2puml.cli:main:72 - Saving PlantUML sequence diagram to sequence.puml...
2025-09-22 16:22:43.382 | SUCCESS  | cwl2puml.cli:main:83 - PlantUML sequence diagram successfully rendered to sequence.puml!
2025-09-22 16:22:43.382 | INFO     | cwl2puml.cli:main:72 - Saving PlantUML state diagram to state.puml...
2025-09-22 16:22:43.425 | SUCCESS  | cwl2puml.cli:main:83 - PlantUML state diagram successfully rendered to state.puml!
2025-09-22 16:22:43.425 | INFO     | cwl2puml.cli:main:89 - Total time: 0.9278 seconds
2025-09-22 16:22:43.426 | INFO     | cwl2puml.cli:main:90 - Finished at: 2025-09-22T16:22:43.425
```

then, for example, try to `cat ./activity.puml` :

```
/'
 ' Diagram generated by cwl2puml v0.23.0
 ' timestamp: 2025-09-22T16:22:43.301
 '/
@startuml
start

split
    
    :stac-item; <<input>>
split again
    
    :epsg_code; <<input>>
split again
    
    :bands; <<input>>
end split
    
repeat
        
:step: step_curl
CommandLineTool: stac;
        
repeat while (dotproduct step_curl/common_band_name)

if ($( inputs.epsg_code == "native"))
           
:step: step_stack
CommandLineTool: rio_stack;
        
endif

if ($( inputs.epsg_code != "native"))

:step: step_warp_stack
CommandLineTool: rio_warp_stack;
        
endif
               
:step: step_color
CommandLineTool: rio_color;
        
split
    
    :rgb-tif; <<output>>
split again
    
    :stack; <<output>>
end split
    
stop
@enduml
```
