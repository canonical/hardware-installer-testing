import os
import argparse
import json
import rpyc
import pathlib


ROOT_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/..")
RESOURCES = ROOT_DIR / "robot" / "resources" / "installer.resource"


def parse_args():
    parser = argparse.ArgumentParser(description="Script to run a robot framework job")
    parser.add_argument("--job-config", type=str, required=True,
                        help="json config file for installer job definition")
    parser.add_argument("--zapper-ip", type=str, required=True,
                        help="IP of zapper machine to run the test on")
    return parser.parse_args()


def load_config(config_filepath):
    config_file = pathlib.Path(config_filepath).read_text()
    config_json = json.loads(config_file)
    return config_json


def load_robot_file(job_config: dict):
    return (ROOT_DIR / "robot" / "suites" / job_config["suite"] / job_config["test"]).read_text()


def load_list_of_templates(job_config: dict):
    templates = []
    for template in job_config["templates"]:
        template_dir = (ROOT_DIR / "robot" / "templates" / template).glob("*")
        templates += [x.absolute() for x in template_dir if x.is_file()]
    return templates


def zapper_connect(zapper_ip):
    return rpyc.connect(
        zapper_ip,
        60000,
        config={
            "allow_public_attrs": True
        },
    )


def main():
    args = parse_args()
    job_config = load_config(args.job_config)
    robot_file = load_robot_file(job_config)
    templates = load_list_of_templates(job_config)
    connection = zapper_connect(args.zapper_ip)
    assets = {}
    variables = {
        "KVM_RESOURCES": "snippets/common/common_kvm.resource",
    }
    for template in templates:
        assets[template] = template.read_bytes()
    status, html = connection.root.robot_run(robot_file, assets, variables)
    print(status)
    output_html = pathlib.Path("/tmp/zapper-install-test.html", "w")
    output_html.write_text(html)


if __name__ == "__main__":
    main()
