# pyns2
pyns2(renamed from netns-siml) is network simulator with linux network namespace create virtual network by yaml format config file.
## support
Now `veth` and `bridge` type interface is supported.

## example
This is the example of network definition. This file is in `examples/example-bridge.yml`

```yaml
example-network-bridge:
    host:
        ifaces:
            br0:
                type: "bridge"
                ifaces:
                    - "veth1-br"
                    - "veth2-br"

    netns:
        host1:
            ifaces:
                host1-veth1:
                    type: "veth"
                    address: "10.0.0.1/24"
                    peer: "veth1-br"

        host2:
            ifaces:
                host2-veth1:
                    type: "veth"
                    address: "10.0.0.2/24"
                    peer: "veth2-br"

```

- to start virtual network
    ```
    $ python main.py run <file>
    ```

- to delete virtual network
    ```
    $ python delete <file>
    ```
