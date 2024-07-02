"""
Calls a robot framework job from robot/suites and runs it on a client board hooked up to a DUT
"""
import argparse
import base64
import json
import os
import pathlib
import subprocess

# import sys
import tempfile

import requests

# import requests
import rpyc

# import time


ROOT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/..")
# INSTALLER_RESOURCE = ROOT_DIR / "robot" / "resources" / "installer.resource"
RESOURCE_DIR = ROOT_DIR / "robot" / "resources"
# ugh, client machine id instead maybe?
HOSTDATA_API = "https://certification.canonical.com/api/v2/hostdata/"
MACHINE_API = "https://certification.canonical.com/api/v2/machines/"


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
        "--client-ip",
        type=str,
        required=True,
        help="IP of client machine to run the test on",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=False,
        default=".",
        help="Directory to place the html output file in.",
    )
    parser.add_argument(
        "--c3-client-id",
        type=str,
        required=True,
        help="client id for c3 authentication",
    )
    parser.add_argument(
        "--c3-secret",
        type=str,
        required=True,
        help="secret string for c3 authentication",
    )
    return parser.parse_args()


def get_access_token(client_id, secret):
    credential = base64.b64encode(
        "{0}:{1}".format(client_id, secret).encode("utf-8")
    ).decode("utf-8")
    headers = {
        "Authorization": "Basic {0}".format(credential),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {"grant_type": "client_credentials", "scope": "read write"}
    response = requests.post(
        "https://certification.canonical.com/oauth2/token/",
        headers=headers,
        data=params,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def c3_query(access_token, url):
    headers = {"Authorization": "Bearer {0}".format(access_token)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    results = response.json()
    for result in results["results"]:
        yield result

    if results["next"]:
        yield from c3_query(access_token, results["next"])


def load_config(config_filepath):
    """Loads the specified json config"""
    config_file = pathlib.Path(config_filepath).read_text(encoding="utf-8")
    config_json = json.loads(config_file)
    return config_json


def load_robot_file(job_config: dict):
    """Loads the robot file specified in the job config"""
    return (
        ROOT_DIR
        / "robot"
        / "suites"
        / job_config["suite"]
        / job_config["test"]
    ).read_bytes()


def load_list_of_templates(job_config: dict):
    """Loads the list of templates as specified in the job config"""
    templates = []
    for template in job_config["templates"]:
        template_dir = (ROOT_DIR / "robot" / "templates" / template).glob("*")
        templates += [x.absolute() for x in template_dir if x.is_file()]
    return templates


def load_local_resources(job_config: dict):
    """Loads any Robot Framework 'resources' as specified in the job config"""
    resources = []
    for resource in job_config["resources"]:
        resources.append(RESOURCE_DIR / resource)
    return resources


def gather_test_assets(templates: list, resources: list):
    """
    Gathers all of the assets required to run the
    test - this includes templates and resources
    """
    assets = {}
    for template in templates:
        assets[os.path.basename(str(template))] = template.read_bytes()
    for resource in resources:
        assets[os.path.basename(str(resource))] = resource.read_bytes()
    return assets


def client_connect(client_ip: str):
    """Connects to the specified client board"""
    return rpyc.connect(
        client_ip,
        60000,
        config={
            "allow_public_attrs": True,
            "sync_request_timeout": 2400,
        },
    )


def flash_usb(job_config: dict, variables: dict, connection: rpyc.Connection):
    """Flashes the USB connected to the client board with a specified iso"""
    robot_file = """*** Settings ***
Resource    ${USB_RESOURCES}

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Flash Noble USB
    [Documentation] Flashes the USB with the Noble ISO
    Download and Provision via USB    """
    robot_file += job_config["iso-url"] + "\n"
    robot_file_bytes = str.encode(robot_file)
    status, html = connection.root.robot_run(robot_file_bytes, {}, variables)
    return status, html


def reserve_machine(queue: str):
    """Reserves the machine via testflinger"""
    testflinger_config = f"""job_queue: {queue}
reserve_data:
  ssh_keys:
    - lp:andersson123
  timeout: 3600
"""  # Change the ssh keys later on ovvi
    with tempfile.NamedTemporaryFile() as testflinger_file:
        pathlib.Path(testflinger_file.name).write_text(
            testflinger_config, encoding="utf-8"
        )
        try:
            print("Submitting testflinger job to reserve machine")
            subprocess.run(
                [
                    "testflinger",
                    "submit",
                    testflinger_file.name,
                ],
                check=True,
            )
            print("Submitting testflinger job succeeded")
            return True
        except subprocess.CalledProcessError as _:
            print("Submitting testflinger job failed")
            return False


def get_machine_ip(machine_id: str, access_token: str):
    api_url = f"{HOSTDATA_API}/{machine_id}/"

    print(c3_query(access_token, api_url))
    # hostdata_json = json.loads(requests.get(api_url).content)
    # print(hostdata_json.keys())
    # print(hostdata_json["detail"])
    # return hostdata_json["ip_address"]


# def get_dut_machine_id(client_id: str):
#     api_url = f"{MACHINE_API}/{client_id}/"
#     machine_json = json.loads(requests.get(api_url).content)
#     return machine_json["parent_canonical_id"]


# def check_ssh_connectivity(machine_ip: str):
#     print(f"Checking connectivity to {machine_ip}")
#     ssh_command = f"ssh ubuntu@{machine_ip} :"
#     start = time.time()
#     timeout = 60
#     while (time.time() - start) < timeout:
#         try:
#             subprocess.run(
#                 ssh_command.split(" "),
#                 check=True,
#             )
#             return True
#         except subprocess.CalledProcessError as _:
#             print("ssh check failed")
#     return False


# def run_remote_command(machine_ip: str, command: str):
#     subprocess.run(
#         f"ssh@{machine_ip} {command}".split(" "),
#         check=True,
#     )


# def gather_boot_templates():
#     templates = []
#     templates_dir = (ROOT_DIR / "robot" / "templates" / "boot").glob("*")
#     templates = [x.absolute() for x in templates_dir if x.is_file()]
#     return templates


# def run_boot_process(connection: rpyc.Connection, variables: dict):
#     assets = gather_boot_templates()
#     robot_boot_file = (
#         ROOT_DIR / "robot" / "suites" / "boot" / "boot-into-usb.robot"
#     ).read_bytes()
#     status, html = connection.root.robot_run(robot_boot_file, assets, variables)
#     return status


def main():
    """Main function which runs the test specified in the job config"""
    args = parse_args()
    c3_token = get_access_token(args.c3_client_id, args.c3_secret)
    ########################################################
    # actual job stuff
    job_config = load_config(args.job_config)
    robot_file = load_robot_file(job_config)
    templates = load_list_of_templates(job_config)
    local_resources = load_local_resources(job_config)
    # Collect variables and assets
    variables = {
        "KVM_RESOURCES": "snippets/common/common_kvm.resource",
        "USB_RESOURCES": "resources/usb_disk.resource",
    }
    assets = gather_test_assets(templates, local_resources)
    client_ip = args.client_ip
    connection = client_connect(client_ip)
    ########################################################
    # Set up client connection
    ###################################################
    # How can we refactor this?
    # We can use, for now, whilst there's no
    # development stuff
    # api calls
    # the api requires authentication. UGH. I mean of course but still
    client_ip = get_machine_ip(args.client_id)
    # dut_machine_id = get_dut_machine_id(args.client_id)
    # dut_ip = get_machine_ip(dut_machine_id)
    # print(client_ip)
    # print(dut_machine_id)
    # print(dut_ip)
    ###################################################
    # run the actual job
    status, html = connection.root.robot_run(robot_file, assets, variables)
    print(status)
    print("installer job finished")
    output_html = pathlib.Path(f"{args.output_dir}/client-install-test.html")
    output_html.write_text(html, encoding="utf-8")
    ###################################################


if __name__ == "__main__":
    main()
