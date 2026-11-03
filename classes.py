import subprocess as subp
import socket
import uuid
import json
from pathlib import Path


class Host:
    def __init__(self, name, ip_addr, host_id=None):
        self.name = name
        self.ip_addr = ip_addr
        self.id = host_id if host_id is not None else str(uuid.uuid4())

    def icmp_ping(self, count = 1):
        ping_res = subp.run(["ping", self.ip_addr, "-n", str(count)], capture_output=True, text=True)
        icmp_res = {
            ""
        }
        return(ping_res.returncode)

    @staticmethod
    def save_host(host, filename="hosts.json"):
        path = Path(filename)

        if path.exists():
            with path.open("r", encoding="utf-8") as file:
                hosts_list = json.load(file)
        else:
            hosts_list = []

        for saved_host in hosts_list:
            if saved_host["id"] == host.id:
                return 

        host_data = {
            "id": host.id,
            "name": host.name,
            "ip_addr": host.ip_addr
        }

        hosts_list.append(host_data)

        # Write the updated list back to the file
        with path.open("w", encoding="utf-8") as file:
            json.dump(hosts_list, file, indent=4)

class Service:
    def __init__(self, name, host, port, protocol = "TCP", service_id=None):
        self.name = name
        self.host = host
        self.port = port
        self.protocol = protocol
        self.id = service_id if service_id is not None else str(uuid.uuid4())

    def tcp_connect_test(self, timeout = 3):
        if self.protocol == "TCP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                sock.connect((self.host.ip_addr, int(self.port)))
                return("TCP port is reachable")
            except (socket.timeout, OSError) as error:
                return(f"Connection failed: {error}")
            finally:
                sock.close()

    @staticmethod
    def save_service(service, filename="services.json"):
        path = Path(filename)

        if path.exists():
            with path.open("r", encoding="utf-8") as file:
                services_list = json.load(file)
        else:
            services_list = []

        for saved_service in services_list:
            if saved_service["id"] == service.id:
                return 

        service_data = {
            "id": service.id,
            "name": service.name,
            "host": service.host.name,
            "port": service.port,
            "protocol": service.protocol
        }

        services_list.append(service_data)

        # Write the updated list back to the file
        with path.open("w", encoding="utf-8") as file:
            json.dump(services_list, file, indent=4)