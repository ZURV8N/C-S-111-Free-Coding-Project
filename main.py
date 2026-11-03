from classes import Host,Service
import json
from pathlib import Path

class DuplicateError(Exception):
    pass

hosts_dict = {}
services_dict = {}

def restore_hosts():
    path = Path("hosts.json")
    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            hosts = json.load(file)
    else:
        raise FileNotFoundError("Couldn't find hosts.json")

    restored_hosts = {}

    for host in hosts:
        host_id = host["id"]
        name = host["name"]
        ip_addr = host["ip_addr"]
        hst = Host(name, ip_addr, host_id)
        restored_hosts[name] = hst

    return restored_hosts

def restore_services():
    path = Path("services.json")
    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            services = json.load(file)
    else:
        raise FileNotFoundError("Couldn't find services.json")
    
    restored_services = {}

    for service in services:
        service_id = service["id"]
        name = service["name"]
        host = service["host"]
        port = service["port"]
        protocol = service["protocol"]
        srvc = Service(name, hosts_dict[host], port, protocol, service_id)
        restored_services[name] = srvc

    return restored_services

def create_host(name, ip_addr, host_id=None):
    global hosts_dict
    for key in hosts_dict.keys():
        if name == hosts_dict[key].name and ip_addr == hosts_dict[key].ip_addr:
            raise DuplicateError(f"Host '{name}' already exists with ip_address '{ip_addr}'.")
        elif name == hosts_dict[key].name and ip_addr != hosts_dict[key].ip_addr:
            raise DuplicateError(f"A host with name '{name}' already exists, but with a different ip address.")
        elif name != hosts_dict[key].name and ip_addr == hosts_dict[key].ip_addr:
            raise DuplicateError(f"A different host already exists at ip address '{ip_addr}'.")
    hosts_dict[name] = Host(name, ip_addr, host_id)

def create_service(name, host, port, protocol="TCP", service_id=None):
    """Takes necessary arguments for the creation of a service, checks them against the services
    that already exist, and raises an error if there's a conflict. If no conflict is found, it
    creates a service with the given fields, and attatches it to the services dictionary with
    the key set to the name value. Returns None."""
    global services_dict
    for key in services_dict.keys():
        a = b = c = ""
        dupe = False
        if name == services_dict[key].name:
            dupe = True
            a = f" with name {name},"
        if port == services_dict[key].port:
            dupe = True
            b = f" with port {port},"
        if host == services_dict[key].host.name:
            dupe = True
            c = f" with hostname {host},"   
        if dupe == True:
            err_string = f"A service already exists{a + b + c}"
            raise DuplicateError(err_string[:-1]+".") 
    services_dict[name] = Service(name, hosts_dict[host], port, protocol, service_id)

def startup():
    global hosts_dict
    global services_dict
    hosts_dict = restore_hosts()
    services_dict = restore_services()

def save_to_files(h_dict, s_dict):
    for host in h_dict.values():
        Host.save_host(host)
    for service in s_dict.values():
        Service.save_service(service)
    return

def main():
    global hosts_dict
    global services_dict
    startup()

    #create_host("pmox_host", "10.2.60.2")
    #print(hosts_dict["pmox_host"].id)

    #create_host("jellyfin_vm_host", "10.2.60.101")
    create_service("jellyfin_webpage", "jellyfin_vm_host", "8096")


    save_to_files(hosts_dict, services_dict)
    print("done")
    print(f"Host for jellyfin_webpage is {services_dict["jellyfin_webpage"].host} and the id is {services_dict["jellyfin_webpage"].id}")

if __name__ == "__main__":
    main()