import psutil, ping3, click
import socket, ipaddress, re, os
from threading import Thread
from http.client import HTTPConnection


def log(s):
	print(s + '\n', end='')


def local_cidr() -> str:
	networks = []
	i = 0
	for interface, addrs in psutil.net_if_addrs().items():
		print(f'{interface}:')
		for addr in addrs:
			if addr.family == socket.AF_INET:
				cidr = f'{addr.address}/{addr.netmask}'
				networks.append(cidr)
				print(str([i]).ljust(10, '·') + cidr)
				i += 1
	index = int(input('Enter the number: '))
	return networks[index]


@click.group()
def cli():
	pass


@cli.command()
@click.argument('address', default='local')
def ping(address):
	if address == 'local':
		address = local_cidr()
	try:
		__multi_ping(address)
	except:
		__ping(address)


def __ping(host):
	t = ping3.ping(host, 2)
	if t:
		log(f"{host.ljust(16, ' ')}{round(t*1000)}ms")


def __multi_ping(cidr):
	for ip in ipaddress.ip_network(cidr, strict=False):
		Thread(target=__ping, args=[ip.exploded]).start()


@cli.command(help='')
@click.argument('address', default='local')
@click.argument('port', type=int, default=80)
@click.option('-ap', '--all-ports', is_flag=True)
def tcp(address, port, all_ports):
	socket.setdefaulttimeout(2)

	if all_ports:
		__all_tcp_ports(address)
		return

	if address == 'local':
		address = local_cidr()
	try:
		__tcp_scan(address, port)
	except:
		__tcp(address, port)


def __tcp(host, port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
		try:
			conn.connect((host, port))
			log(f'{host}:{port}')
		except:
			pass


def __tcp_scan(cidr, port):
	for ip in ipaddress.ip_network(cidr, strict=False):
		Thread(target=__tcp, args=[ip.exploded, port]).start()


def __all_tcp_ports(host):
	for port in range(1, 65536):
		Thread(target=__tcp, args=[host, port]).start()


@cli.command()
@click.argument('host')
@click.argument('port', type=int, default=80)
@click.option('-m', '--method', default='HEAD')
@click.option('-ap', '--all-ports', is_flag=True)
def http(host, port, method: str, all_ports):
	method = method.upper()

	if all_ports:
		__all_http_port(host, method)
		return

	__http(host, port, method)


def __http(host, port, method):
	try:
		http = HTTPConnection(host, port, 5)
		http.request(method, '/')
		res = http.getresponse()
		log(f'[{res.status} {res.reason}] http://{host}:{port}')
	except:
		pass
	finally:
		http.close()


def __all_http_port(host, method):
	for port in range(1, 65536):
		Thread(target=__http, args=[host, port, method]).start()


if __name__ == '__main__':
	cli()
