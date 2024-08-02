#!/usr/bin/python3
"""
Calls testflinger job to run installer test
"""
import argparse
import json
import pathlib
import re
import subprocess
import tempfile
from typing import List

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
    config_file = pathlib.Path(config_filepath).read_text(encoding="utf-8")
    config_json = json.loads(config_file)
    return config_json


def load_list_of_templates(job_config: dict):
    """Loads the list of templates as specified in the job config"""
    templates = []
    for template in job_config["templates"]:
        template_dir = (ROOT_DIR / "robot" / "templates" / template).glob("*")
        templates += [x for x in template_dir if x.is_file()]
    return templates


def load_local_resources(job_config: dict):
    """Loads any Robot Framework 'resources' as specified in the job config"""
    resources = []
    for resource in job_config["resources"]:
        resources.append(RESOURCE_DIR / resource)
    return resources


def load_testflinger_template(machine_id: str) -> str:
    """
    Loads testflinger template
    """
    template_file = (
        ROOT_DIR / "testflinger-definitions" / f"{machine_id}.template.yaml"
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
    iso_url: str,
    job_config: dict,
) -> str:
    """
    Creates the test data section for the full testflinger file for the job
    """
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
    test_data += "    mkdir artifacts\n"
    test_data += "    cd attachments/test/\n"
    test_data += f"    ./scripts/call_job.py --job-config {job_config_fp} "
    test_data += "--client-ip $ZAPPER_IP --output-dir .\n"
    test_data += "    mv *.html ../../artifacts/\n"
    test_data = test_data.replace("<url>", iso_url)
    return test_data


def write_complete_testflinger_yaml(
    template: str, job_config: dict, iso_url: str, job_config_fp: str
) -> str:
    """
    Takes the template file and appends the test_data section
    """
    templates = load_list_of_templates(job_config)
    resources = load_local_resources(job_config)
    test_data_section = create_test_data_section(
        templates, resources, job_config_fp, iso_url, job_config
    )
    return f"{template}\n{test_data_section}"


def execute(cmd):
    """
    Executes a subprocess command and yields the terminal
    output line by line
    """
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


def main():
    """
    Main function
    """
    args = parse_args()
    job_config = load_config(args.job_config)
    machine_id = args.c3_machine_id
    testflinger_template = load_testflinger_template(machine_id)
    tf_data = write_complete_testflinger_yaml(
        testflinger_template, job_config, args.iso_url, args.job_config
    )
    print(tf_data)
    job_id = None
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
                if searched is not None:
                    job_id = searched.group(1)
                    print("*" * 100 + f"\nJob id: {job_id}")
                print(line, end="")
        # pylint: disable=W0718
        except Exception as e:
            print(f"Testflinger submission failed with {e}")
    print(job_id)
    # need to add this too
    # testflinger artifacts 10372257-1e53-4807-961f-a03a4a95d3c2
    # to have the artifacts in jenkins
    # and in the jenkins job tar -xf the file, archive the html


if __name__ == "__main__":
    main()
