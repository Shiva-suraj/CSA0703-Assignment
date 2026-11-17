# Computer Networks – Assignment 2 (CO2)

**Student:** A. Siva suraj sai  
**Register number:** 192425276  
**Course:** Computer Networks

> This Markdown copy provides the written assignment outline and key results. Download the formatted PDF from the ChatGPT conversation and upload it here if a PDF copy is required. Packet Tracer/GNS3 screenshots and actual simulation outputs must be added after running the configurations.

## Q1 – IPv4 addressing, fragmentation and switching (6 marks)

- Library PC: `10.20.7.255/22` is the broadcast address of `10.20.4.0/22`; it is not a valid host address.
- Lab server: `172.20.70.0/19` is a valid host address in `172.20.64.0/19`.
- Hostel AP: `192.168.45.130/26` is a valid host, but gateway `192.168.45.1` is outside its subnet.
- Branch router: `198.51.100.34/28` is a valid host in `198.51.100.32/28`.
- A 4,000-byte IPv4 datagram with a 20-byte header has 3,980 payload bytes. At MTU 1,500, the fragments are: payload 1,480 (offset 0, MF=1), payload 1,480 (offset 185, MF=1), payload 1,020 (offset 370, MF=0).
- PMTUD uses ICMP feedback to discover a smaller path MTU. Blocking required ICMP can cause a PMTUD black hole.
- Datagram switching routes packets independently; virtual-circuit switching establishes a logical path first.
- For 180 simultaneous DHCP clients, /24 is the smallest conventional subnet (254 usable addresses). A /25 is too small.

## Q2 – Subnetting, VLSM and route summarisation (8 marks)

### Equal-size subnetting
A /25 is needed to support the largest department (110 hosts), providing 126 usable addresses. Five /25 networks require 640 addresses, so they cannot fit in the supplied /24.

### VLSM allocation within 192.168.50.0/24

| Department | Network | Usable host range | Broadcast |
|---|---|---|---|
| Production | 192.168.50.0/25 | .50.1–.50.126 | .50.127 |
| Design | 192.168.50.128/26 | .50.129–.50.190 | .50.191 |
| Stores | 192.168.50.192/27 | .50.193–.50.222 | .50.223 |
| Guest Wi-Fi | 192.168.50.224/28 | .50.225–.50.238 | .50.239 |
| WAN | 192.168.50.240/30 | .50.241–.50.242 | .50.243 |

The remaining addresses cannot provide a CCTV /27. Obtain the adjacent 192.168.51.0/24, making a /23 block, and allocate CCTV as 192.168.51.0/27 (30 usable hosts).

- Four contiguous networks 172.18.24.0/24–172.18.27.0/24 summarise to 172.18.24.0/22.
- Adding 172.18.28.0/24 requires 172.18.24.0/21 as a single summary, which also covers three unowned /24 networks.
- VLSM requires classless routing protocols that carry prefix information.

## Q3 – Longest-prefix matching and floating static routes (6 marks)

- 172.20.18.70 matches 172.20.18.64/26.
- 172.20.18.130 matches 172.20.18.0/24.
- 172.20.20.5 matches 172.20.16.0/20.
- 172.20.99.9 matches 172.20.0.0/16.
- 192.168.200.15 matches the OSPF route 192.168.200.0/24.
- 8.8.8.8 uses the default route.

Example Cisco static routes:

```text
ip route 0.0.0.0 0.0.0.0 203.0.113.1
ip route 0.0.0.0 0.0.0.0 198.51.100.1 250
```

The second route is a floating backup because its administrative distance is higher. IP SLA can detect upstream forwarding failure even when the local interface remains up.

## Q4 – Distance-vector routing and count to infinity (6 marks)

Use the Bellman-Ford update:

`D(u,d) = min(cost(u,n) + D(n,d))`

For links P-Q=4, P-R=1, Q-R=2, Q-S=6, R-S=3 and S-T=5, the converged distances are:

| Router | P | Q | R | S | T |
|---|---:|---:|---:|---:|---:|
| P | 0 | 3 | 1 | 4 | 9 |
| Q | 3 | 0 | 2 | 5 | 10 |
| R | 1 | 2 | 0 | 3 | 8 |
| S | 4 | 5 | 3 | 0 | 5 |
| T | 9 | 10 | 8 | 5 | 0 |

After R-S fails, the corrected shortest-path matrix is:

| Router | P | Q | R | S | T |
|---|---:|---:|---:|---:|---:|
| P | 0 | 3 | 1 | 9 | 14 |
| Q | 3 | 0 | 2 | 6 | 11 |
| R | 1 | 2 | 0 | 8 | 13 |
| S | 9 | 6 | 8 | 0 | 5 |
| T | 14 | 11 | 13 | 5 | 0 |

Count to infinity occurs when routers repeatedly increase stale route metrics. Split horizon with poison reverse advertises an unusable metric back to the neighbour from which a route was learned. EIGRP uses DUAL and may switch to a feasible successor when the feasibility condition is met.

## Q5 – OSPF DR/BDR and Dijkstra (6 marks)

- Highest OSPF interface priority becomes DR; a tie is broken by highest Router ID. Priority 0 is ineligible.
- R3 (priority 100, RID 3.3.3.3) is DR; R2 (priority 100, RID 2.2.2.2) is BDR.
- Six routers: full mesh 15 adjacencies; with DR/BDR, 9.
- Twenty routers: full mesh 190; with DR/BDR, 37.
- OSPF does not pre-empt the current DR/BDR when a higher-priority router joins.

Dijkstra from A for the supplied graph gives: C=2, B=3 via C, D=7 via C-B, E=9 via C, and F=11 via C-E.

## Q6 – IPv6, ICMP, multicast and SDN (5 marks)

- Compressed IPv6 address: `2001:db8:a0::ff:1`.
- Modified EUI-64 identifier from MAC 3C:52:82:4E:11:07: `3e52:82ff:fe4e:1107`.
- Link-local address: `fe80::3e52:82ff:fe4e:1107`.
- IPv4 multicast 239.130.5.9 maps to Ethernet multicast `01:00:5E:02:05:09`; 32 IPv4 groups can share one Ethernet multicast MAC.
- IGMP reports multicast group membership; IGMP snooping limits forwarding to interested switch ports.
- OpenFlow priority 300 SSH rule drops; priority 200 destination subnet rule forwards to port 2; unmatched traffic goes to the controller.
- IPv6-only sensors with redundant NAT64/DNS64 gateways can reduce the need for public IPv4 addresses; use dual-stack during legacy transition.

## Q7 – Network redesign and validation (13 marks)

**Problem:** the original 192.168.50.0/24 allocation leaves insufficient address space for a CCTV /27.

**Redesign:** add adjacent 192.168.51.0/24 and use the combined 192.168.50.0/23. Retain all existing department subnets and allocate CCTV as 192.168.51.0/27 with gateway 192.168.51.1.

**Pass criteria:**
1. Six subnets do not overlap.
2. Each subnet has enough usable host addresses.
3. All gateways respond to ping.
4. Twenty CCTV clients can be configured.
5. Routing table contains the CCTV subnet.
6. Inter-VLAN traceroute follows the configured Layer-3 gateway path.

Useful Cisco validation commands:

```text
show ip interface brief
show vlan brief
show interfaces trunk
show ip route
ping 192.168.51.1
traceroute 192.168.50.1
```

Save the Packet Tracer/GNS3 topology, actual CLI outputs, screenshots and test results in this folder before submission.

## References

- Supplied Computer Networks CO2 Assignment 2 PDF.
- RFC 791 – Internet Protocol.
- RFC 1191 – Path MTU Discovery.
- RFC 2328 – OSPF Version 2.
- RFC 4291 – IPv6 Addressing Architecture.
- RFC 4443 – ICMPv6.
- RFC 4632 – CIDR.
- Python 3 documentation.
- Cisco IOS routing configuration documentation.
