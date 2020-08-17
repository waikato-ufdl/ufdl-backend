# Job Templates

The job templates listed in this directory represent a manually curated list of
available job templates for UFDL.

These images are only those related to the image classification data-domain.

Example JSON structure:

```json
{
  "name": "MyJobTemplate",
  "scope": "my_scope",
  "framework": "tensorflow|1.15",
  "domain": "ic",
  "job_type": "predict",
  "executor_class": "MyExecutorClass",
  "required_packages": "",
  "body": "{}",
  "licence": "Apache 2.0",
  "inputs": [
    "input1|str|my_options",
    "input2|dataset"
  ],
  "parameters": [
    "parameter1|int|42",
    "parameter2|str|this is not a test (yes it is)",
    "parameter3|bool|False"
  ]
}
```
