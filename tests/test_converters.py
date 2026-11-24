import json
from pathlib import Path

import ReadMainAndWriteJson as main_tf
import ReadTfVarsAndWriteJson as tfvars

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_TF = ROOT / "ReadAndWriteMain" / "main.tf"
SAMPLE_TFVARS = ROOT / "ReadTfvarsAndWriteJson" / "dev.tfvars"


def test_main_tf_sample():
    data = main_tf.load_tf_file(SAMPLE_TF)

    assert data["terraform"] == [{"required_version": "1.2.3"}]
    assert data["provider"][0]["aws"]["shared_credentials_files"] == ["$HOME/.aws/credentials"]
    assert data["locals"][0]["environment"] == "${terraform.workspace}"
    assert data["module"][0]["ecs-cluster"]["source"] == "./modules/ecs-cluster"


def test_tfvars_sample_keeps_lists():
    data = tfvars.load_tfvars_file(SAMPLE_TFVARS)

    assert data["aws_region"] == "sa-east-1"
    assert data["subnets"] == ["subnet-86bd71dd", "subnet-dc439195"]


def test_tfvars_types_multiline_and_comments(tmp_path):
    source = tmp_path / "test.tfvars"
    source.write_text(
        "  # indented comment\n"
        "count   = 3 # inline comment\n"
        "enabled = true\n"
        "// slash comment\n"
        "tags = {\n"
        '  Name = "web"\n'
        '  Env  = "dev"\n'
        "}\n"
        "ports = [\n"
        "  80,\n"
        "  443,\n"
        "]\n",
        encoding="utf-8",
    )

    data = tfvars.load_tfvars_file(source)

    assert data == {
        "count": 3,
        "enabled": True,
        "tags": {"Name": "web", "Env": "dev"},
        "ports": [80, 443],
    }


def test_cli_writes_json_next_to_input(tmp_path):
    source = tmp_path / "prod.tfvars"
    source.write_text('region = "us-east-1"\n', encoding="utf-8")

    assert tfvars.main([str(source)]) == 0
    assert json.loads((tmp_path / "prod.json").read_text(encoding="utf-8")) == {"region": "us-east-1"}


def test_cli_custom_output(tmp_path):
    output = tmp_path / "out" / "main.json"
    output.parent.mkdir()

    assert main_tf.main([str(SAMPLE_TF), "-o", str(output)]) == 0
    assert "terraform" in json.loads(output.read_text(encoding="utf-8"))


def test_cli_missing_file_returns_error(tmp_path, capsys):
    assert tfvars.main([str(tmp_path / "missing.tfvars")]) == 1
    assert main_tf.main([str(tmp_path / "missing.tf")]) == 1
    assert "not found" in capsys.readouterr().err
