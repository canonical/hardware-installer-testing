#!/usr/bin/python3
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
import webbrowser

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
        "--client-id",
        type=str,
        required=True,
        help="id of client machine in c3",
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
    parser.add_argument(
        "--interactive",
        "-i",
        required=False,
        action="store_true",
    )
    return parser.parse_args()


def get_access_token(client_id, secret):
    """
    Generates an access token for c3
    """
    credential = base64.b64encode(
        # "{0}:{1}".format(client_id, secret).encode("utf-8")
        f"{client_id}:{secret}".encode("utf-8")
    ).decode("utf-8")
    headers = {
        "Authorization": f"Basic {credential}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params = {"grant_type": "client_credentials", "scope": "read write"}
    response = requests.post(
        "https://certification.canonical.com/oauth2/token/",
        headers=headers,
        data=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def c3_query(access_token, url):
    """
    Function to query c3 api, provided by cert team
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    results = response.json()
    return results


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


# unused as of yet
# def flash_usb(job_config: dict, variables: dict, connection: rpyc.Connection):
#     """Flashes the USB connected to the client board with a specified iso"""
#     robot_file = """*** Settings ***
# Resource    ${USB_RESOURCES}

# *** Variables ***
# ${T}    ${CURDIR}

# *** Test Cases ***
# Flash Noble USB
#     [Documentation] Flashes the USB with the Noble ISO
#     Download and Provision via USB    """
#     robot_file += job_config["iso-url"] + "\n"
#     robot_file_bytes = str.encode(robot_file)
#     status, html = connection.root.robot_run(robot_file_bytes, {}, variables)
#     return status, html


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
        except subprocess.CalledProcessError as exc:
            raise subprocess.CalledProcessError(
                f"Submitting testflinger job failed with: {exc}", cmd=None
            ) from exc


def c3_get_machine_ip(machine_id: str, access_token: str):
    """
    Gets the ip address of a machine from c3 using its machine id
    """
    api_url = f"{HOSTDATA_API}{machine_id}/"
    data = c3_query(access_token, api_url)
    return data["ip_address"]


def c3_get_dut_machine_id(client_id: str, access_token: str):
    """
    Gets the machine id of the DUT based on the client id
    """
    api_url = f"{MACHINE_API}{client_id}/"
    data = c3_query(access_token, api_url)
    return data["parent_canonical_id"]


# unused as of yet
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


# unused as of yet
# def run_remote_command(machine_ip: str, command: str):
#     subprocess.run(
#         f"ssh@{machine_ip} {command}".split(" "),
#         check=True,
#     )


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
    ########################################################
    # Set up client connection
    ###################################################
    # in the future once c3 api is production ready this
    # may change - instead of using client id we may use dut id
    client_ip = c3_get_machine_ip(args.client_id, c3_token)
    dut_machine_id = c3_get_dut_machine_id(args.client_id, c3_token)
    reserve_machine(dut_machine_id)
    connection = client_connect(client_ip)

    # dut_ip = get_machine_ip(dut_machine_id, c3_token)
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
    if args.interactive:
        webbrowser.open(output_html)
    ###################################################


if __name__ == "__main__":
    main()
