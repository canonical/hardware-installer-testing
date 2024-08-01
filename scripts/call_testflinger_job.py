#!/usr/bin/python3
import argparse
import pathlib
import json
import tempfile
import subprocess
import re
import os
from typing import List


# ROOT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/..")
ROOT_DIR = pathlib.Path("./")
# INSTALLER_RESOURCE = ROOT_DIR / "robot" / "resources" / "installer.resource"
RESOURCE_DIR = ROOT_DIR / "robot" / "resources"

"""
Need to also add step for grub
Need to write a file like this:
---
job_queue: 202207-30464
provision_data:
  url: https://releases.ubuntu.com/noble/ubuntu-24.04-desktop-amd64.iso
  robot_tasks:
    - hp/pro/sff_400_g9/boot/boot_from_usb.robot
    - common/grub/stop/stop_at_grub.robot
  live_image: true
  wait_until_ssh: false
  skip_download: true  # only needed rn for testing whilst the usb has the correct iso on it
test_data: # example below
  attachments:
    - local: "config.json"
      agent: "data/config/config.json"
    - local: "images/ubuntu-logo.png"
    - local: "scripts/my_test_script.sh"
      agent: "script.sh"
  test_cmds: |
    # can use these
    # $ZAPPER_IP
    # $DEVICE_IP
    ls -alR
    cat attachments/test/data/config/config.json
    chmod u+x attachments/test/script.sh
    attachments/test/script.sh

For attachments, can either attach each template and resource etc separately, or tar up locally but that involves creating tmp directory or something and seems kinda long

Need a template for each machine? At least for the robot_tasks bit
and then this script fills out the test_data section?
test_cmds should be the same for each, so filled out by script

So I need to:
- create a template version of the above?
- actually just embed in script?
- needs to also copy the script which runs the test to the testflinger agent, so testflinger can run the script

steps of this script:
- takes job config
- takes machine id as argument
- writes full testflinger.yaml file to run job, including:
  - all of the templates specified by the job config
  - all of the resources specified by the job config
- templates should go with the same full file path to make more compatible with call_job.py
- same for resources

I should refactor this too at some point as some functions will end up being shared

"""


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
    template_file = ROOT_DIR / "testflinger-definitions" / f"{machine_id}.template.yaml"
    return template_file.read_text()


def create_test_data_section(templates: List[pathlib.PosixPath],
                             resources: List[pathlib.PosixPath],
                             job_config_fp: str,
                             iso_url: str,
                             job_config: dict) -> str:
    test_data = "test_data:\n  attachments:\n"
    test_data += f'    - local: "scripts/call_job.py"\n      agent: "scripts/call_job.py"\n'
    test_data += f'    - local: "{job_config_fp}"\n      agent: "{job_config_fp}"\n'
    for template in templates:
        test_data += f'    - local: "{template}"\n      agent: "{template}"\n'
    for resource in resources:
        test_data += f'    - local: "{resource}"\n      agent: "{resource}"\n'
    test_data += "  test_cmds: |\n"
    test_data += f"    ls\n"
    test_data += f"    cd attachments/test/\n"
    test_data += f"    ./scripts/call_job.py --job-config {job_config_fp} --client-ip $ZAPPER_IP --output-dir ."
    test_data = test_data.replace("<url>", iso_url)
    return test_data


def write_complete_testflinger_yaml(template: str, job_config: dict, iso_url: str, job_config_fp: str) -> str:
    templates = load_list_of_templates(job_config)
    resources = load_local_resources(job_config)
    test_data_section = create_test_data_section(templates, resources, job_config_fp, iso_url, job_config)
    return f"{template}\n{test_data_section}"


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def main():
    args = parse_args()
    job_config = load_config(args.job_config)
    machine_id = args.c3_machine_id
    testflinger_template = load_testflinger_template(machine_id)
    tf_data = write_complete_testflinger_yaml(testflinger_template, job_config, args.iso_url, args.job_config)
    # print(tf_data)
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
                print(line, end="")
        except Exception as e:
            print(f"Testflinger submission failed with {e}")


if __name__ == "__main__":
    main()
