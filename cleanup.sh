#! /bin/sh

ip netns delete host1
ip netns delete host2

ip link delete host1-veth0
ip link delete host2-veth1
ip link delete host2-veth2
