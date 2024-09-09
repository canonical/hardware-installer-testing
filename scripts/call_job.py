#!/usr/bin/python3
"""
Calls a robot framework job from robot/suites and runs it on a client board hooked up to a DUT
"""
import argparse
import json
import logging
import os
import pathlib
import time
import sys
import webbrowser

import paramiko
import rpyc

logging.basicConfig(level="INFO")

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
        "--dut-ip",
        type=str,
        required=False,
        help="ip of DUT",
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
    logging.info("Loading job config...")
    config_file = pathlib.Path(config_filepath).read_text(encoding="utf-8")
    config_json = json.loads(config_file)
    return config_json


def load_robot_file(job_config: dict):
    """Loads the robot file specified in the job config"""
    logging.info(f"Loading specified robot file {job_config['test']}")
    return (
        ROOT_DIR
        / "robot"
        / "suites"
        / job_config["suite"]
        / job_config["test"]
    ).read_bytes()


def load_list_of_templates(job_config: dict):
    """Loads the list of templates as specified in the job config"""
    logging.info("Loading templates")
    templates = []
    for template in job_config["templates"]:
        template_dir = (ROOT_DIR / "robot" / "templates" / template).glob("*")
        templates += [x.absolute() for x in template_dir if x.is_file()]
    return templates


def load_local_resources(job_config: dict):
    """Loads any Robot Framework 'resources' as specified in the job config"""
    logging.info("Loading resources")
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
    logging.info("Gathering templates")
    for template in templates:
        assets[os.path.basename(str(template))] = template.read_bytes()
    logging.info("Gathering resources")
    for resource in resources:
        assets[os.path.basename(str(resource))] = resource.read_bytes()
    return assets


def client_connect(client_ip: str):
    """Connects to the specified client board"""
    logging.info(f"Connecting to {client_ip}")
    return rpyc.connect(
        client_ip,
        60000,
        config={
            "allow_public_attrs": True,
            "sync_request_timeout": 2400,
        },
    )


def run_paramiko_command(ssh_client: paramiko.SSHClient, command: str) -> str:
    """Runs a command via paramiko"""
    logging.info(f"Running the following command via paramiko: {command}")
    stdin, stdout, _ = ssh_client.exec_command(command)  # the _ is stderr
    stdin.close()
    return stdout.read().decode("utf-8")


def connect_with_paramiko(dut_ip: str, username: str, password: str, retries:int=10, delay:int=5) -> paramiko.SSHClient:
    logging.info(f"Setting up paramiko connection to {dut_ip}")
    for retry in range(retries):
        logging.info(f"Attempt {retry+1} to set up connection to {dut_ip}...")
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=dut_ip, username=username, password=password)
            return ssh_client
        except Exception as e:
            logging.warning(f"Connecting to DUT failed with {e}, retrying another {retries-(retry+1)} times")
        time.sleep(delay)
    logging.error(f"Couldn't connect to {dut_ip} after {retries} retries")
    sys.exit(1)



def copy_logs(dut_ip: str, output_dir: str):
    """
    Copies logs under /var/log/installer/ and a journalctl
    snippet from the DUT to the testflinger agent/host machine
    """
    logging.info("Collecting logs from DUT")
    username = "ubuntu"
    password = "ubuntu"
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=dut_ip, username=username, password=password)
    logging.info("paramiko connection set up!")
    command = (
        """python3 -c 'import os; result = [os.path.join(dp, f) for dp, dn, """
        + """filenames in os.walk("/var/log/installer/") for f in filenames]; """
        + """print(" ".join(result));'"""
    )
    stdout = run_paramiko_command(ssh_client=ssh_client, command=command)
    files = stdout.replace("\n", "").split(" ")
    command = "mkdir -p /tmp/installer-logs/"
    run_paramiko_command(ssh_client=ssh_client, command=command)
    logging.info("Copying files under / to /tmp/")
    for file in files:
        file_name = file.split("/")[-1]
        command = f"echo {password} | sudo -S cat {file} > /tmp/installer-logs/{file_name}"
        run_paramiko_command(ssh_client=ssh_client, command=command)
    logging.info("Done copying files")
    logging.info("Copying files from DUT to host machine")
    ftp_client = ssh_client.open_sftp()
    for file in files:
        file_name = file.split("/")[-1]
        logging.info(f"Copying {file_name}")
        ftp_client.get(
            f"/tmp/installer-logs/{file_name}", f"{output_dir}/{file_name}"
        )
    ftp_client.close()
    logging.info("Cleaning up temporary directory on DUT")
    command = "rm -r /tmp/installer-logs/"
    run_paramiko_command(ssh_client=ssh_client, command=command)
    logging.info("Done copying logs - now gathering journalctl snippet")
    command = "journalctl -b 0 --no-pager"
    jrnl_output = run_paramiko_command(ssh_client=ssh_client, command=command)
    pathlib.Path(f"{output_dir}/journalctl-b-0.log").write_text(
        jrnl_output, encoding="utf-8"
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
    logging.info(f"Connected to {client_ip}!")

    status, html = connection.root.robot_run(robot_file, assets, variables)
    print("RESULT=PASS" if status else "RESULT=FAIL")
    print("installer job finished")
    output_html = pathlib.Path(f"{args.output_dir}/client-install-test.html")
    output_html.write_text(html, encoding="utf-8")
    if args.interactive:
        webbrowser.open(str(output_html))
    if args.dut_ip:
        copy_logs(args.dut_ip, args.output_dir)
    else:
        logging.info("DUT ip address not provided, not copying logs!")
    sys.exit(0 if status else 1)


if __name__ == "__main__":
    main()
