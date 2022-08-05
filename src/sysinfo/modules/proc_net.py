import struct
import socket
from sysinfo_lib import parseSpaceTable, tableToDict


def parser_route(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)
        if to_camelcase:
            output = tableToDict(output, "iface")
        else:
            output = tableToDict(output, "Iface")

    return {"output": output, "unprocessed": []}


def split_every_n(data, n):
    return [data[i : i + n] for i in range(0, len(data), n)]


def parse_ipv4_address(address):
    hex_addr, hex_port = address.split(":")

    addr_list = split_every_n(hex_addr, 2)
    addr_list.reverse()
    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    port = str(int(hex_port, 16))

    return addr, port


def parse_ipv6_address(address):
    hex_addr, hex_port = address.split(":")

    addr = bytes.fromhex(hex_addr)
    addr = struct.unpack(">IIII", addr)
    addr = struct.pack("@IIII", *addr)
    addr = socket.inet_ntop(socket.AF_INET6, addr)
    port = str(int(hex_port, 16))

    return addr, port


def extend_address4(entry, name, name_addr, name_port):
    if name in entry:
        address, port = parse_ipv4_address(entry[name])
        entry[name_addr] = address
        entry[name_port] = port


def extend_address6(entry, name, name_addr, name_port):
    if name in entry:
        address, port = parse_ipv6_address(entry[name])
        entry[name_addr] = address
        entry[name_port] = port


def parser_tcp_udp(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)

        for entry in output:
            extend_address4(entry, "local_address", "local_addr", "local_port")
            extend_address4(entry, "rem_address", "rem_addr", "rem_port")
            extend_address4(entry, "localAddress", "localAddr", "localPort")
            extend_address4(entry, "remAddress", "remAddr", "remPort")

    return {"output": output, "unprocessed": []}


def parser_tcp_udp_6(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)

        for entry in output:
            extend_address6(entry, "local_address", "local_addr", "local_port")
            extend_address6(entry, "rem_address", "rem_addr", "rem_port")
            extend_address6(entry, "localAddress", "localAddr", "localPort")
            extend_address6(entry, "remAddress", "remAddr", "remPort")

    return {"output": output, "unprocessed": []}


def parser_arp(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "proc_net_route",
            "system": ["linux"],
            "cmd": "cat /proc/net/route",
            "description": "IP routing information",
            "parser": parser_route,
        }
    )

    main.register(
        {
            "name": "proc_net_ax25_route",
            "system": ["linux"],
            "cmd": "cat /proc/net/ax25_route",
            "description": "AX25 routing information",
            "parser": parser_route,
        }
    )

    main.register(
        {
            "name": "proc_net_ipx_route",
            "system": ["linux"],
            "cmd": "cat /proc/net/ipx_route",
            "description": "IPX routing information",
            "parser": parser_route,
        }
    )

    main.register(
        {
            "name": "proc_net_tcp",
            "system": ["linux"],
            "cmd": "cat /proc/net/tcp",
            "description": "TCP socket table",
            "parser": parser_tcp_udp,
        }
    )

    main.register(
        {
            "name": "proc_net_udp",
            "system": ["linux"],
            "cmd": "cat /proc/net/udp",
            "description": "UDP socket table",
            "parser": parser_tcp_udp,
        }
    )

    main.register(
        {
            "name": "proc_net_tcp6",
            "system": ["linux"],
            "cmd": "cat /proc/net/tcp6",
            "description": "TCP6 socket table",
            "parser": parser_tcp_udp_6,
        }
    )

    main.register(
        {
            "name": "proc_net_udp6",
            "system": ["linux"],
            "cmd": "cat /proc/net/udp6",
            "description": "UDP6 socket table",
            "parser": parser_tcp_udp_6,
        }
    )

    main.register(
        {
            "name": "proc_net_arp",
            "system": ["linux"],
            "cmd": "cat /proc/net/arp",
            "description": "ARP ",
            "parser": parser_arp,
        }
    )
