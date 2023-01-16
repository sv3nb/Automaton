#!/usr/bin/env bash

BR_ADDR="10.10.0.1"
BR_DEV="br0"

NS1="namespace1"
VETH1="veth0"
PEER1="veth1"	
PEER1_ADDR="10.10.0.10"

NS2="namespace2"
VETH2="veth2"
PEER2="veth3"
PEER2_ADDR="10.10.0.20"

# remove namespace if it exists.
ip netns del $NS1 &>/dev/null
ip netns del $NS2 &>/dev/null

# create namespace
ip netns add $NS1
ip netns add $NS2

# create veth link
ip link add ${VETH1} type veth peer name ${PEER1}
ip link add ${VETH2} type veth peer name ${PEER2}

# setup veth link
ip link set ${VETH1} up
ip link set ${VETH2} up

# add peers to ns
ip link set ${PEER1} netns ${NS1}
ip link set ${PEER2} netns ${NS2}

# setup peer ns interface
ip netns exec ${NS1} ip link set ${PEER1} up
ip netns exec ${NS2} ip link set ${PEER2} up

# assign ip address to ns interfaces
ip netns exec ${NS1} ip addr add ${PEER1_ADDR}/24 dev ${PEER1}
ip netns exec ${NS2} ip addr add ${PEER2_ADDR}/24 dev ${PEER2}

# setup bridge
ip link add ${BR_DEV} type bridge
ip link set ${BR_DEV} up

# assign veth pairs to bridge
ip link set ${VETH1} master ${BR_DEV}
ip link set ${VETH2} master ${BR_DEV}

# setup bridge ip
ip addr add ${BR_ADDR}/24 dev ${BR_DEV}

# add default routes for ns
ip netns exec ${NS1} ip route add default via ${BR_ADDR}
ip netns exec ${NS2} ip route add default via ${BR_ADDR}

# enable ip forwarding
bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# Flush nat rules.
iptables -t nat -F

iptables -t nat -A POSTROUTING -s ${BR_ADDR}/16! -o ${BR_DEV} -j MASQUERADE
