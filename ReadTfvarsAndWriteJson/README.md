# ReadTfvarsAndWriteJson

Converts a Terraform `.tfvars` file to JSON.

```bash
# Uses dev.tfvars in this folder and writes dev.json
python ReadTfVarsAndWriteJson.py

# Custom input and output
python ReadTfVarsAndWriteJson.py path/to/prod.tfvars -o prod.json
```

Result:

```text
File .tfvars converted to 'dev.json' successfully.
```

See the [main README](../README.md) for an input/output example and limitations.
