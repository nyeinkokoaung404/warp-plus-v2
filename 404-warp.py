import ipaddress
import platform
import subprocess
import os
import datetime
import base64
import json
# i Am 4-0-4 / t.me/nkka404
warp_cidr = [
    "162.159.192.0/24",
    "162.159.193.0/24",
    "162.159.195.0/24",
    "162.159.204.0/24",
    "188.114.96.0/24",
    "188.114.97.0/24",
    "188.114.98.0/24",
    "188.114.99.0/24",
]

script_directory = os.path.dirname(__file__)
Bestip_path = os.path.join(script_directory, "Bestip.txt")
result_path = os.path.join(script_directory, "result.csv")


def create_ips():
    c = 0
    top_ips = sum(len(list(ipaddress.IPv4Network(cidr))) for cidr in warp_cidr)

    with open(Bestip_path, "w") as file:
        for cidr in warp_cidr:
            ip_addresses = list(ipaddress.IPv4Network(cidr))
            for addr in ip_addresses:
                c += 1
                file.write(str(addr))
                if c != top_ips:
                    file.write("\n")


if os.path.exists(Bestip_path):
    print("Bestip.txt exists.")
else:
    print("Creating Bestip.txt File.")
    create_ips()
    print("Bestip.txt File Created Successfully!")


def arch_suffix():
    machine = platform.machine().lower()
    if machine.startswith("i386") or machine.startswith("i686"):
        return "386"
    elif machine.startswith(("x86_64", "amd64")):
        return "amd64"
    elif machine.startswith(("armv8", "arm64", "aarch64")):
        return "arm64"
    elif machine.startswith("s390x"):
        return "s390x"
    else:
        raise ValueError("Unsupported CPU architecture")


arch = arch_suffix()

print("Fetch warp program...")
url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-{arch}"

subprocess.run(["wget", url, "-O", "warp"])
os.chmod("warp", 0o755)
command = "./warp >/dev/null 2>&1"
print("Scanning ips...")
process = subprocess.Popen(command, shell=True)

process.wait()

if process.returncode != 0:
    print("Error: Warp execution failed.")
else:
    print("Warp executed successfully.")

Bestip = []

with open(result_path, "r") as csv_file:
    next(csv_file)
    c = 0
    for line in csv_file:
        Bestip.append(line.split(",")[0])
        c += 1
        if c == 2:
            break

with open("Bestip.txt", "w") as f:
    for ip in Bestip:
        f.write(f"{ip}\n")


formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def export_Hiddify(t_ips):
    config_prefix = f"warp://{t_ips[0]}?ifp=1-3&ifpm=m4#TEHRAN-404&&detour=warp://{t_ips[1]}?ifp=1-2&ifpm=m5#BERLIN-404"
    return config_prefix, formatted_time


title = (
    "//profile-title: base64:"
    + base64.b64encode("Warp+By404".encode("utf-8")).decode("utf-8")
    + "\n"
)
update_interval = "//profile-update-interval: 1\n"
sub_info = "//subscription-userinfo: upload=5368709120; download=117037858816; total=955630223360; expire=1762677732\n"
profile_web = "//profile-web-page-url: https://github.com/nyeinkokoaung404\n"
last_modified = "//last update on: " + formatted_time + "\n"

config_prefix, _ = export_Hiddify(Bestip)
with open("404-warp.json", "w") as op:
    op.write(
        title + update_interval + sub_info + profile_web + last_modified + config_prefix
    )


os.remove(Bestip_path)
os.remove(result_path)
os.remove("warp")


def toSingBox(tag, clean_ip, detour):
    print("Generating Warp Conf")
    command = 'wget -N "https://gitlab.com/fscarmen/warp/-/raw/main/api.sh" && sudo bash api.sh -r'
    prc = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = prc.stdout

    if (prc.returncode == 0) and output:
        try:
            data = json.loads(output)
            wg = {
                "tag":f"{tag}",
                "type":"vless",
                "server":f"{clean_ip.split(':')[0]}",
                "server_port":443,
                "uuid":"765e5bee-afec-410b-ad82-3e94d45e3e56",
                "transport":{
                "path":"/SG1",
                "type":"ws",
                "headers":{
                "Host":"agustus.jrflashervpn.my.id"
           }
         },
                "tls":{
                "enabled":True,
                "server_name":"agustus.jrflashervpn.my.id",
                "insecure":True
         },
                "tcp_fast_open":False
            }

            for file in ["api.sh"]:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Removed {file}")
                else:
                    print(f"{file} not found, skipping removal")

            return wg
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON output")
            return None
        except KeyError as e:
            print(f"Error: Missing key in JSON data: {e}")
            return None
    else:
        print("Error: Command execution failed or produced no output")
        return None


def export_SingBox(t_ips):
    with open("assets/404-singbox-template.json", "r") as f:
        data = json.load(f)

    data["outbounds"][7]["outbounds"].extend(["auto", "direct", "🚀TEHRAN-404", "🚀BERLIN-404", "@nkka404", "🇳🇱H2-404", "🇲🇲ATOM(500MB)-404", "🇯🇵JP-404",])

    tehran_wg = toSingBox("🚀TEHRAN-404", t_ips[0], "direct")
    if tehran_wg:
        data["outbounds"].insert(2, tehran_wg)
    else:
        print("Failed to generate 🚀TEHRAN-404 configuration")

    berlin_wg = toSingBox("🚀BERLIN-404", t_ips[1], "🚀TEHRAN-404")
    if berlin_wg:
        data["outbounds"].insert(3, berlin_wg)
    else:
        print("Failed to generate 🚀BERLIN-404 configuration")

    with open("404-sing-box.json", "w") as f:
        json.dump(data, f, indent=4)


def main(script_dir):
    try:
        arch = arch_suffix()
        print("Fetch warp program...")
        url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-{arch}"
        subprocess.run(["wget", url, "-O", "warp"], check=True)
        os.chmod("warp", 0o755)
        print("Scanning ips...")
        subprocess.run(
            ["./warp"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("Warp executed successfully.")

        result_path = os.path.join(script_dir, "result.csv")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:

        if os.path.exists("warp"):
            os.remove("warp")

        top_ips = []
        with open(result_path, "r") as csv_file:
            next(csv_file)
            for _ in range(2):
                line = next(csv_file, None)
                if line:
                    top_ips.append(line.split(",")[0])

        export_Hiddify(top_ips)
        export_SingBox(top_ips)

        if os.path.exists(result_path):
            os.remove(result_path)


if __name__ == "__main__":
    script_directory = os.path.dirname(__file__)
    main(script_directory)
