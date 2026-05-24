# 🏗️ Terraform.Read
A collection of Python scripts to read Terraform files (`.tf`, `.tfvars`) and convert them to JSON. The goal is to simplify test automation for infrastructure defined as code.

## 📋 Description
This repository contains standalone utilities that parse Terraform configuration and produce JSON files ready to use in CI/CD pipelines, validations, or automated test suites.

| Module | Input | Output | Parser |
|--------|-------|--------|--------|
| `ReadAndWriteMain` | `main.tf` | `main.json` | [python-hcl2](https://pypi.org/project/python-hcl2/) |
| `ReadTfvarsAndWriteJson` | `dev.tfvars` | `dev.json` | Custom line-based parser |

## 📁 Project structure
```
Terraform.Read/
├── ReadAndWriteMain/
│   ├── main.tf                    # Sample Terraform file
│   ├── ReadMainAndWriteJson.py    # .tf → .json conversion script
│   └── README.md
├── ReadTfvarsAndWriteJson/
│   ├── dev.tfvars                 # Sample variables file
│   ├── ReadTfVarsAndWriteJson.py  # .tfvars → .json conversion script
│   └── README.md
└── README.md
```

## ⚙️ Requirements
- **Python** 3.7+
- **ReadAndWriteMain** requires the `python-hcl2` library:

```bash
pip install python-hcl2
```

`ReadTfvarsAndWriteJson` uses only the Python standard library.

## 🚀 Usage
### 📦 ReadAndWriteMain

Reads a `main.tf` file (`terraform`, `provider`, `locals`, `module` blocks, etc.) and exports it to JSON.

```bash
cd ReadAndWriteMain
python ReadMainAndWriteJson.py
```

**Expected output:**

```
File JSON saved in 'main.json'.
```

> Edit the `tf_file_path` and `output_json_file` variables at the bottom of `ReadMainAndWriteJson.py` to point to other files.

### 📦 ReadTfvarsAndWriteJson
Reads a `.tfvars` file with `key = value` assignments and produces a flat JSON file.

```bash
cd ReadTfvarsAndWriteJson
python ReadTfVarsAndWriteJson.py
```

**Expected output:**
```
File .tfvars converted to .json successfully.
```

> By default it processes `dev.tfvars` and writes `dev.json`. Update the paths in the script to match your environment.

## 💡 Use cases
- Generate JSON fixtures from real Terraform for unit or integration tests.
- Inspect the parsed structure of a `main.tf` without running `terraform plan`.
- Normalize environment variables (`.tfvars`) into a format consumable by other tools.

## 📝 Version
**1.0**
