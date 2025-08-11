# Introduction 

This project aims to deliver a simple yet powerful CLI tool to ingest [CWL Workflows](https://www.commonwl.org/) and generate [PantUM diagrams](https://plantuml.com/).

## Installation

```
pip install cwl2puml
```

## CLI execution

```
Usage: cwl2puml [OPTIONS]

Options:
  --workflow TEXT            The CWL workflow file (it can be an URL or a file
                             on the File System)  [required]
  --puml [components|class]  The PlantUML diagram type.  [required]
  --output PATH              Output file path  [required]
  --help                     Show this message and exit.
```

i.e.

```
cwl2puml \
--workflow https://raw.githubusercontent.com/eoap/ogc-api-processes-with-zoo/refs/heads/feature-EOEPCA-469/cwl-workflows/eoap-api.cwl \
--puml components \
--output ./test.puml
```

Output would be

```
2025-08-11 13:58:40.945 | INFO     | cwl_loader:load_cwl_from_location:186 - Loading CWL document from https://raw.githubusercontent.com/eoap/ogc-api-processes-with-zoo/refs/heads/feature-EOEPCA-469/cwl-workflows/eoap-api.cwl...
2025-08-11 13:58:41.463 | INFO     | cwl_loader:load_cwl_from_yaml:117 - Updating the model to v1.2...
2025-08-11 13:58:41.478 | INFO     | cwl_loader:load_cwl_from_yaml:128 - Raw CWL document successfully updated to v1.2! Now converting to the CWL model...
2025-08-11 13:58:54.228 | INFO     | cwl_loader:load_cwl_from_yaml:136 - Raw CWL document successfully updated to v1.2! Now dereferencing the FQNs...
2025-08-11 13:58:54.228 | INFO     | cwl_loader:_clean_process:62 -   Cleaning Workflow eoap-api...
2025-08-11 13:58:54.228 | INFO     | cwl_loader:_clean_process:62 -   Cleaning CommandLineTool stac-client...
2025-08-11 13:58:54.228 | INFO     | cwl_loader:_clean_process:62 -   Cleaning CommandLineTool ogc-api-processes-client...
2025-08-11 13:58:54.228 | INFO     | cwl_loader:load_cwl_from_yaml:144 - CWL document successfully dereferenced!
2025-08-11 13:58:54.228 | INFO     | cwl2puml:main:167 - ------------------------------------------------------------------------
2025-08-11 13:58:54.228 | INFO     | cwl2puml:main:171 - Saving the new PlantUML Workflow diagram to test.puml...
2025-08-11 13:58:54.247 | INFO     | cwl2puml:main:180 - PlantUML Workflow components diagram successfully rendered to test.puml!
2025-08-11 13:58:54.248 | INFO     | cwl2puml:main:184 - Total time: 13.3030 seconds
2025-08-11 13:58:54.248 | INFO     | cwl2puml:main:185 - Finished at: 2025-08-11T13:58:54.248
```

then try to `cat ./test.puml`:

```
@startuml
skinparam linetype ortho

node "Workflow 'eoap-api'" {
    component "eoap-api" as eoap_api {
        portin "stac_api_endpoint" as eoap_api_stac_api_endpoint
        portin "search_request" as eoap_api_search_request
        portin "processes_api_endpoint" as eoap_api_processes_api_endpoint
        portin "execute_request" as eoap_api_execute_request
        portout "search_output" as eoap_api_search_output
        portout "process_output" as eoap_api_process_output
    }

    component "discovery" as eoap_api_discovery {
        portin "api_endpoint" as eoap_api_discovery_api_endpoint
        eoap_api_stac_api_endpoint .down.> eoap_api_discovery_api_endpoint
        portin "search_request" as eoap_api_discovery_search_request
        eoap_api_search_request .down.> eoap_api_discovery_search_request
        portout "search_output" as eoap_api_discovery_search_output
    }

    component "processes" as eoap_api_processes {
        portin "api_endpoint" as eoap_api_processes_api_endpoint
        eoap_api_processes_api_endpoint .down.> eoap_api_processes_api_endpoint
        portin "execute_request" as eoap_api_processes_execute_request
        eoap_api_execute_request .down.> eoap_api_processes_execute_request
        portin "search_results" as eoap_api_processes_search_results
        eoap_api_discovery_search_output .down.> eoap_api_processes_search_results
        portout "process_output" as eoap_api_processes_process_output
    }
}

node "CommandLineTool 'stac-client'" {
    component "stac-client" as stac_client {
        portin "api_endpoint" as stac_client_api_endpoint
        portin "search_request" as stac_client_search_request
        portout "search_output" as stac_client_search_output
    }
}

node "CommandLineTool 'ogc-api-processes-client'" {
    component "ogc-api-processes-client" as ogc_api_processes_client {
        portin "api_endpoint" as ogc_api_processes_client_api_endpoint
        portin "execute_request" as ogc_api_processes_client_execute_request
        portin "search_results" as ogc_api_processes_client_search_results
        portout "process_output" as ogc_api_processes_client_process_output
    }
}

eoap_api_discovery_search_output .up.> eoap_api_search_output
eoap_api_processes_process_output .up.> eoap_api_process_output
eoap_api_discovery .right.> stac_client
eoap_api_processes .right.> ogc_api_processes_client
@enduml
```
