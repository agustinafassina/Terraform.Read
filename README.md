# 🏗️ Terraform.Read

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://github.com/agustinafassina/Terraform.Read/actions/workflows/tests.yml/badge.svg)

A collection of Python scripts to read Terraform files (`.tf`, `.tfvars`) and convert them to JSON. The goal is to simplify test automation for infrastructure defined as code.

## 📋 Description

This repository contains standalone utilities that parse Terraform configuration and produce JSON files ready to use in CI/CD pipelines, validations, or automated test suites.

| Module                   | Input     | Output  | Parser |
|--------------------------|-----------|---------|--------|
| `ReadAndWriteMain`       | `.tf`     | `.json` | [python-hcl2](https://pypi.org/project/python-hcl2/) |
| `ReadTfvarsAndWriteJson` | `.tfvars` | `.json` | [python-hcl2](https://pypi.org/project/python-hcl2/) |

Both scripts keep value types: lists, maps, numbers and booleans are written as real JSON types, not as strings.

## 📁 Project structure

```text
Terraform.Read/
├── .github/workflows/tests.yml    # CI: runs the tests on every push / PR
├── ReadAndWriteMain/
│   ├── main.tf                    # Sample Terraform file
│   ├── ReadMainAndWriteJson.py    # .tf → .json conversion script
│   └── README.md
├── ReadTfvarsAndWriteJson/
│   ├── dev.tfvars                 # Sample variables file
│   ├── ReadTfVarsAndWriteJson.py  # .tfvars → .json conversion script
│   └── README.md
├── tests/                         # pytest test suite
├── requirements.txt
├── requirements-dev.txt
├── CHANGELOG.md
└── README.md
```

## ⚙️ Installation

Requires **Python 3.10+**.

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## 🚀 Usage

Both scripts accept the input file as an argument and an optional `-o/--output` path. If no output is given, the JSON is written next to the input with the same name (`dev.tfvars` → `dev.json`). With no arguments they use the sample file in their folder.

```bash
python <script>.py [input] [-o OUTPUT]
```

If a file cannot be read or written, the script prints the error to stderr and exits with code `1`, so CI/CD pipelines fail as expected.

### 📦 ReadAndWriteMain

Reads a `.tf` file (`terraform`, `provider`, `locals`, `module` blocks, etc.) and exports it to JSON.

```bash
python ReadAndWriteMain/ReadMainAndWriteJson.py path/to/main.tf -o main.json
```

**Input:**

```hcl
locals {
  instance_name = "instance-name-terraform-test"
  environment   = terraform.workspace
}

module "ecs-cluster" {
  source      = "./modules/ecs-cluster"
  environment = local.environment
}
```

**Output:**

```json
{
    "locals": [
        {
            "instance_name": "instance-name-terraform-test",
            "environment": "${terraform.workspace}"
        }
    ],
    "module": [
        {
            "ecs-cluster": {
                "source": "./modules/ecs-cluster",
                "environment": "${local.environment}"
            }
        }
    ]
}
```

### 📦 ReadTfvarsAndWriteJson

Reads a `.tfvars` file and writes its variables as a JSON object.

```bash
python ReadTfvarsAndWriteJson/ReadTfVarsAndWriteJson.py envs/prod.tfvars
```

**Input:**

```hcl
aws_region    = "sa-east-1"
instance_type = "t2.small"
subnets       = ["subnet-86bd71dd", "subnet-dc439195"]
```

**Output:**

```json
{
    "aws_region": "sa-east-1",
    "instance_type": "t2.small",
    "subnets": [
        "subnet-86bd71dd",
        "subnet-dc439195"
    ]
}
```

## ⚠️ Limitations

- **Expressions are not evaluated.** References and functions such as `terraform.workspace`, `local.environment` or `var.x` are kept as strings wrapped in `${...}`. The scripts read the files; they don't run Terraform.
- **Comments are dropped** from the output.
- **Blocks are lists.** Top-level blocks (`provider`, `module`, `resource`...) are always lists, because a file can declare the same block type more than once.

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest
```

The tests also run on GitHub Actions on every push to `develop`/`main` and on every pull request.

## 💡 Use cases

- Generate JSON fixtures from real Terraform for unit or integration tests.
- Inspect the parsed structure of a `main.tf` without running `terraform plan`.
- Normalize environment variables (`.tfvars`) into a format consumable by other tools.

## 📝 Version

See [CHANGELOG.md](CHANGELOG.md).
