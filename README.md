### 用法

```
Usage: python netscan.py [OPTIONS] COMMAND [ARGS]...

Commands:
  ping        执行 Ping 扫描
  tcp         执行 TCP 扫描
  http        执行 HTTP 扫描
```

#### `ping` 子命令

```
Usage: python netscan.py ping ADDRESS

Arguments:
  address 目标地址，可以为ip、域名、cidr。默认为 'local'，表示扫描本地网段。
```

#### `tcp` 子命令

```
Usage: python netscan.py tcp ADDRESS [PORT] [OPTIONS]

Arguments:
  address 目标地址，可以为ip、域名、cidr。默认为 'local'，表示扫描本地网段。
  port    目标端口，默认为 80。

Options:
  -ap, --all-ports 扫描目标主机的所有端口（1-65535）。
```

#### `http` 子命令

```
Usage: python netscan.py http HOST [PORT] [OPTIONS]

Arguments:
  host    目标主机。
  port    目标端口，默认为 80。

Options:
  -m, --method      请求方法，默认为 'HEAD'。
  -ap, --all-ports   扫描目标主机的所有端口（1-65535）。
```
