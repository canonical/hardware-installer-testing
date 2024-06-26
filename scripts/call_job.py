"""
Calls a robot framework job from robot/suites and runs it on a zapper board hooked up to a DUT
"""
import argparse
import json
import os
import pathlib
import subprocess

# import sys
import tempfile
import time

# import requests
import rpyc

ROOT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/..")
# INSTALLER_RESOURCE = ROOT_DIR / "robot" / "resources" / "installer.resource"
RESOURCE_DIR = ROOT_DIR / "robot" / "resources"
# ugh, zapper machine id instead maybe?
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
        "--zapper-ip",
        type=str,
        required=True,
        help="IP of zapper machine to run the test on",
    )
    return parser.parse_args()


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


def zapper_connect(zapper_ip: str):
    """Connects to the specified zapper board"""
    return rpyc.connect(
        zapper_ip,
        60000,
        config={
            "allow_public_attrs": True,
            "sync_request_timeout": 2400,
        },
    )


def flash_usb(job_config: dict, variables: dict, connection: rpyc.Connection):
    """Flashes the USB connected to the zapper board with a specified iso"""
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


# def get_machine_ip(machine_id: str):
#     api_url = f"{HOSTDATA_API}/{machine_id}/"
#     hostdata_json = json.loads(requests.get(api_url).content)
#     print(hostdata_json.keys())
#     print(hostdata_json["detail"])
#     return hostdata_json["ip_address"]


# def get_dut_machine_id(zapper_id: str):
#     api_url = f"{MACHINE_API}/{zapper_id}/"
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
    zapper_ip = args.zapper_ip
    connection = zapper_connect(zapper_ip)
    # Set up zapper connection
    ###################################################
    # development stuff
    # api calls
    # the api requires authentication. UGH. I mean of course but still
    # zapper_ip = get_machine_ip(args.zapper_id)
    # dut_machine_id = get_dut_machine_id(args.zapper_id)
    # dut_ip = get_machine_ip(dut_machine_id)
    # print(zapper_ip)
    # print(dut_machine_id)
    # print(dut_ip)
    # sys.exit(0)
    # Reserve the machine
    # print(f"Reserving machine {dut_machine_id}")
    # if not reserve_machine(dut_machine_id):
    #     print(f"Reserving machine {dut_machine_id} failed!")
    # print(f"Machine {dut_machine_id} reserved")
    # # Double check connectivity to machine
    # print(f"Machine {dut_machine_id} reserved, checking connectivity...")
    # if not check_ssh_connectivity(dut_ip):
    #     print(f"ssh-ing to machine {dut_ip} failed!")
    # print(f"ssh-ing to machine {dut_ip} succeeded!")
    # print(f"Checking connectivity to zapper {zapper_ip}")
    # if not check_ssh_connectivity(zapper_ip):
    #     print(f"ssh-ing to machine {zapper_ip} failed!")
    # print(f"ssh-ing to machine {zapper_ip} succeeded!")
    # Double check that the usb is connected
    # print("enabling usb on zapper machine")
    # run_remote_command(zapper_ip, "zapper typecmux set DUT")
    # Flash the usb with the iso
    # print(f"Flashing zapper usb with iso...")
    # status, html = flash_usb(job_config, variables, connection)
    # Reboot the DUT
    # run_remote_command(dut_ip, "reboot")
    # Run the robot job to boot into the installer
    # run_boot_process(connection, variables)
    ###################################################
    status, html = connection.root.robot_run(robot_file, assets, variables)
    print(status)
    print("installer job finished")
    output_html = pathlib.Path("/tmp/zapper-install-test.html")
    output_html.write_text(html, encoding="utf-8")
    time.sleep(15)
    post_boot_robot_file = (
        ROOT_DIR / "robot" / "suites" / job_config["suite"] / "post-boot.robot"
    ).read_bytes()
    status, html = connection.root.robot_run(
        post_boot_robot_file, assets, variables
    )
    print("post boot job finished")
    print(status)
    output_html = pathlib.Path("/tmp/zapper-install-test-post-boot.html")
    output_html.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
