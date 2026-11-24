# ReadAndWriteMain

Converts a Terraform `.tf` file to JSON.

```bash
# Uses main.tf in this folder and writes main.json
python ReadMainAndWriteJson.py

# Custom input and output
python ReadMainAndWriteJson.py path/to/main.tf -o output.json
```

Result:

```text
File JSON saved in 'main.json'.
```

See the [main README](../README.md) for an input/output example and limitations.
