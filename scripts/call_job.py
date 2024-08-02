#!/usr/bin/python3
"""
Calls a robot framework job from robot/suites and runs it on a client board hooked up to a DUT
"""
import argparse
import json
import os
import pathlib
import webbrowser

import rpyc

ROOT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/..")
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
        "--client-ip",
        type=str,
        required=True,
        help="ip of client machine hooked up to the DUT",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=False,
        default=".",
        help="Directory to place the html output file in.",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        required=False,
        action="store_true",
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


def main():
    """Main function which runs the test specified in the job config"""
    args = parse_args()
    job_config = load_config(args.job_config)
    robot_file = load_robot_file(job_config)
    templates = load_list_of_templates(job_config)
    local_resources = load_local_resources(job_config)
    client_ip = args.client_ip
    # Collect variables and assets
    variables = {
        "KVM_RESOURCES": "snippets/common/common_kvm.resource",
        "USB_RESOURCES": "resources/usb_disk.resource",
    }
    assets = gather_test_assets(templates, local_resources)
    connection = client_connect(client_ip)

    status, html = connection.root.robot_run(robot_file, assets, variables)
    print(status)
    print("installer job finished")
    output_html = pathlib.Path(f"{args.output_dir}/client-install-test.html")
    output_html.write_text(html, encoding="utf-8")
    if args.interactive:
        webbrowser.open(str(output_html))


if __name__ == "__main__":
    main()
