# Job Templates

The job templates listed in this directory represent a manually curated list of
available job templates for UFDL.

These images are only those related to the image segmentation data-domain.

Example JSON structure:

```json
{
  "name": "MyJobTemplate",
  "scope": "my_scope",
  "framework": "tensorflow|1.15",
  "domain": "is",
  "job_type": "predict",
  "executor_class": "MyExecutorClass",
  "required_packages": "",
  "body": "{}",
  "licence": "Apache 2.0",
  "inputs": [
    {
      "name": "input1",
      "type": "str",
      "options": "my_options",
      "help": "The first input"
    },
    {
      "name": "input2",
      "type": "dataset",
      "help": "The second input"
    }
  ],
  "parameters": [
    {
      "name": "parameter1",
      "type": "int",
      "default": "42",
      "help": "The first parameter"
    },
    {
      "name": "parameter2",
      "type": "str",
      "default": "this is not a test (yes it is)",
      "help": "The second parameter"
    },
    {
      "name": "parameter3",
      "type": "bool",
      "default": "False",
      "help": "The third parameter"
    }
  ]
}
```
