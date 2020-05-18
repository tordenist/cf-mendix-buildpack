import os
import subprocess
import urllib.request
import tarfile

WAZUH_ROOT_DIR = "/home/vcap/app/ossec"
WAZUH_CONFIG_DIR = WAZUH_ROOT_DIR + "/etc/"
WAZUH_BIN_DIR = WAZUH_ROOT_DIR + "/bin"
WAZUH_ETC_FILE = "/etc/ossec-init.conf"
CURRENT_DATE = subprocess.getoutput("date")

# def _is_wazuh_monitoring_enabled():
    # return os.environ.get("WAZUH_MONITORING_ENABLED") == "true"


def _get_wazuh_manager_addr():
    return os.getenv("WAZUH_MANAGER_ADDR")


def _is_installed():
    return os.path.exists(WAZUH_ROOT_DIR)

def _set_up_ossec_init():

    template = """DIRECTORY="{WAZUH_INSTALL}",
NAME="Wazuh",
VERSION="v3.12.0",
REVISION="31204",
DATE="{CURRENT_DATE}",
TYPE="agent"
"""
    context = {
     "WAZUH_INSTALL": WAZUH_ROOT_DIR,
     "CURRENT_DATE": CURRENT_DATE
     }

    with open("/home/vcap/app/ossec/etc/ossec-init.conf", "w") as myfile:
        myfile.write(template.format(**context))


def _set_up_wazuh_agent():
    lines = ""

    with open(WAZUH_CONFIG_DIR + "ossec.conf") as fh:
        WAZUH_MANAGER = _get_wazuh_manager_addr()
        lines = "".join(fh.readlines())
        lines = (
            lines.replace("MANAGER_IP", WAZUH_MANAGER)
        )
        with open(WAZUH_CONFIG_DIR + "ossec.conf", "w") as fh:
            fh.write(lines)


# TEST S3 BUCKET
def download_wazuh():
    url = "http://wazuh-agent-test-bucket.s3.eu-west-2.amazonaws.com/wazuh-agent-vcap-3-12.tar.gz"
    urllib.request.urlretrieve(url, "/tmp/wazuh-agent.tar.gz")
    tar = tarfile.open("/tmp/wazuh-agent.tar.gz")
    tar.extractall("/home/vcap/app/")
    tar.close()
    _set_up_ossec_init()
    _set_up_wazuh_agent()


def start_wazuh_auth():
    global wazuh_auth
    WAZUH_MANAGER = _get_wazuh_manager_addr()
    wazuh_auth = subprocess.run(
        ["/home/vcap/app/ossec/bin/agent-auth", "-m", WAZUH_MANAGER]
    )


def start_wazuh_agent():
    global wazuh_agent
    wazuh_agent = subprocess.Popen(
        ["/home/vcap/app/ossec/bin/ossec-control", "start"]
    )
