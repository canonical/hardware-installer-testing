#!/usr/bin/python3
"""
Calls testflinger job to run installer test
"""
import argparse
import json
import logging
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import List

logging.basicConfig(level="INFO")

ROOT_DIR = pathlib.Path("./")
RESOURCE_DIR = ROOT_DIR / "robot" / "resources"


def parse_args():
    """
    Parses the command line args for this script.
    """
    parser = argparse.ArgumentParser(
        description="Script to run a robot framework job"
    )
    parser.add_argument(
        "--job-config",
        type=str,
        required=True,
        help="json config file for installer job definition",
    )
    parser.add_argument(
        "--c3-machine-id",
        type=str,
        required=True,
        help="c3 machine id for the device under test",
    )
    parser.add_argument(
        "--iso-url",
        type=str,
        required=True,
        help="url for the desktop iso you wish to test",
    )
    return parser.parse_args()


def load_config(config_filepath: str) -> dict:
    """Loads the specified json config"""
    logging.info(f"Loading json job config: {config_filepath}")
    config_file = pathlib.Path(config_filepath).read_text(encoding="utf-8")
    config_json = json.loads(config_file)
    return config_json


def load_list_of_templates(job_config: dict):
    """Loads the list of templates as specified in the job config"""
    logging.info("Loading list of templates")
    templates = []
    for template in job_config["templates"]:
        template_dir = (ROOT_DIR / "robot" / "templates" / template).glob("*")
        templates += [x for x in template_dir if x.is_file()]
    return templates


def load_local_resources(job_config: dict):
    """Loads any Robot Framework 'resources' as specified in the job config"""
    logging.info("Loading local resources")
    resources = []
    for resource in job_config["resources"]:
        resources.append(RESOURCE_DIR / resource)
    return resources


def load_testflinger_template(machine_id: str, job_config: dict) -> str:
    """
    Loads testflinger template
    """
    logging.info(f"Loading testflinger template for {machine_id}")
    if "tpm-fde" in job_config["test"]:
        template_file = (
            ROOT_DIR
            / "testflinger-definitions"
            / "tpm-fde"
            / f"{machine_id}.template.yaml"
        )
    else:
        template_file = (
            ROOT_DIR
            / "testflinger-definitions"
            / f"{machine_id}.template.yaml"
        )
    return template_file.read_text()


def get_robot_file_fp(job_config: dict):
    """
    Gets the filepath for the robot file
    """
    return (
        ROOT_DIR
        / "robot"
        / "suites"
        / job_config["suite"]
        / job_config["test"]
    )


def create_test_data_section(
    templates: List[pathlib.PosixPath],
    resources: List[pathlib.PosixPath],
    job_config_fp: str,
    job_config: dict,
) -> str:
    """
    Creates the test data section for the full testflinger file for the job
    """
    logging.info("Creating test data section for testflinger yaml file")
    test_data = "test_data:\n  attachments:\n"
    robot_file = get_robot_file_fp(job_config)
    test_data += f'    - local: "{robot_file}"\n      agent: "{robot_file}"\n'
    test_data += '    - local: "scripts/call_job.py"\n      agent: "scripts/call_job.py"\n'
    test_data += (
        f'    - local: "{job_config_fp}"\n      agent: "{job_config_fp}"\n'
    )
    for template in templates:
        test_data += f'    - local: "{template}"\n      agent: "{template}"\n'
    for resource in resources:
        test_data += f'    - local: "{resource}"\n      agent: "{resource}"\n'
    test_data += "  test_cmds: |\n"
    test_data += "    set -e\n"
    test_data += "    mkdir -p artifacts/logs/\n"
    test_data += "    cd attachments/test/\n"
    test_data += "    echo You can view the stream of the test here:\n"
    test_data += '    echo "http://${ZAPPER_IP}:60010/stream"\n'
    # test_data += "    sudo apt install python3.8-venv\n"
    # test_data += "    python3 -m venv env\n"
    # test_data += "    . env/bin/activate\n"
    # test_data += "    pip install -r requirements.txt\n"
    test_data += "    pip install paramiko\n"
    test_data += f"    ./scripts/call_job.py --job-config {job_config_fp} "
    test_data += "--client-ip $ZAPPER_IP --output-dir ../../artifacts/ --dut-ip $DEVICE_IP\n"
    return test_data


def write_complete_testflinger_yaml(
    template: str, job_config: dict, iso_url: str, job_config_fp: str
) -> str:
    """
    Takes the template file and appends the test_data section
    """
    logging.info("Creating full testflinger yaml file")
    templates = load_list_of_templates(job_config)
    resources = load_local_resources(job_config)
    test_data_section = create_test_data_section(
        templates, resources, job_config_fp, job_config
    )
    template = template.replace("<url>", iso_url)
    logging.info(
        f"Created full testflinger yaml file:\n{template}\n{test_data_section}"
    )
    return f"{template}\n{test_data_section}"


def execute(cmd: List[str]):
    """
    Executes a subprocess command and yields the terminal
    output line by line
    """
    logging.info(
        f"Executing the following command as a subprocess:\n{' '.join(cmd)}"
    )
    # pylint: disable=R1732
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True
    )
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def gather_artifacts(job_id: str) -> None:
    """
    Gathers the artifacts from the job run using:
    testflinger artifacts <job_id>
    and then untars them.
    """
    logging.info("Gathering testflinger artifacts...")
    try:
        gather = subprocess.run(
            [
                "testflinger",
                "artifacts",
                job_id,
            ],
            check=True,
            capture_output=True,
        )
        logging.info(f"Artifacts gathered: \n{gather.stdout.decode('utf-8')}")
    except subprocess.CalledProcessError as gather_error:
        logging.error(f"Failed to gather artifacts with {gather_error}")
    try:
        _ = subprocess.run(
            [
                "tar",
                "-xf",
                "artifacts.tgz",
            ],
            check=True,
            capture_output=True,
        )
        logging.info(
            "un-tar'd artifacts - they now exist in the artifacts/ directory"
        )
    except subprocess.CalledProcessError as untar_error:
        logging.error(f"Failed to untar artifacts with {untar_error}")


def main():
    """
    Main function
    """
    args = parse_args()
    job_config = load_config(args.job_config)
    machine_id = args.c3_machine_id
    testflinger_template = load_testflinger_template(machine_id, job_config)
    tf_data = write_complete_testflinger_yaml(
        testflinger_template, job_config, args.iso_url, args.job_config
    )
    job_id = None
    result = None
    with tempfile.NamedTemporaryFile(
        suffix=".yaml", delete=True, dir="."
    ) as testflinger_file:
        pathlib.Path(testflinger_file.name).write_text(
            tf_data, encoding="utf-8"
        )
        try:
            for line in execute(
                [
                    "testflinger",
                    "submit",
                    "-p",
                    testflinger_file.name,
                ]
            ):
                searched = re.search("job_id: (.*)\n", line)
                if "RESULT=PASS" in line:
                    result = True
                elif "RESULT=FAIL" in line:
                    result = False
                if searched is not None:
                    job_id = searched.group(1)
                    logging.info(
                        "********************************************"
                    )
                    print(f"Job id: {job_id}")
                print(line, end="")
        # pylint: disable=C0103,W0703
        except Exception as submission_error:
            print(f"Testflinger submission failed with: {submission_error}")
    gather_artifacts(job_id)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
