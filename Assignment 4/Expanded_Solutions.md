# Assignment 4 – Expanded Solutions

These answers follow the six tasks in the supplied CO4 assignment. Assumptions are stated explicitly. Add individual Packet Tracer evidence, actual cable-test results and measured throughput before submission.

## Task 1 – Why does the whole computer lab go down? (6 marks)

### 1.1 Complaints and hidden weaknesses
The school has 45 computers in two labs connected through four cascaded hubs. A hub repeats every received signal to its other ports and does not learn MAC addresses. An upstream hub or cable failure can disconnect downstream devices and the server. All computers share collision and bandwidth resources, so simultaneous exam traffic creates contention, collisions, backoff and retransmissions. A hub also repeats traffic to every port, allowing a connected user to capture traffic that is not encrypted.

Other weaknesses: one large collision domain, no VLAN separation, poor fault isolation, limited scalability, no port security and a possible single point of failure at the internet router.

### 1.2 Extended-star redesign
Use a managed access switch in each lab, both connected directly to a central distribution switch. Connect the server to a protected server VLAN. Connect distribution to a router and firewall. Use Cat6/Cat6A structured cabling, patch panels and labelled outlets. Configure separate VLANs for staff, students, servers and guests; use ACLs and firewall rules.

Topology: Internet → ISP ONT → Router/Firewall → Distribution Switch → Lab-1 Switch, Lab-2 Switch and Server. PCs connect to their lab access switch.

Assume the old shared segment provides 100 Mbps total. Equal-share estimate: 100/45 = 2.22 Mbps per computer, before overhead and collisions. With dedicated 1 Gbps switch ports, each PC has a 1 Gbps access link; actual simultaneous throughput is limited by uplinks. Two 1 Gbps lab uplinks provide 2 Gbps aggregate, equivalent to about 44.4 Mbps per computer under an equal-share full-load assumption. A 10 Gbps distribution uplink provides more headroom.

### 1.3 Defence (under 100 words)
The extended star removes the cascading-hub dependency by giving each lab a direct switch uplink. Dedicated full-duplex switch ports reduce collisions and provide predictable access bandwidth. VLANs separate staff, student, server and guest traffic, while ACLs and a firewall restrict unauthorised access. Structured cabling and a central distribution point simplify fault isolation and expansion. Redundant uplinks can further reduce downtime.

### Alternative: Wi-Fi 6
Two APs serving 45 laptops share radio airtime. If both APs together deliver an assumed 600 Mbps usable throughput, the equal-share estimate is 600/45 = 13.3 Mbps per laptop. This is illustrative, not guaranteed. A switched star is more predictable for online exams; Wi-Fi is useful for mobility and supplementary access. AP placement, channel plan and client load must be surveyed.

## Task 2 – How many links can the polytechnic afford? (8 marks)

### 2.1 Link, port and cost calculation
Per leased link: Rs 1.20 lakh + two router ports (2 × Rs 0.25 lakh) = Rs 1.70 lakh/year.
- Bus/chain: 5 links, 10 ports, Rs 8.5 lakh/year.
- Ring: 6 links, 12 ports, Rs 10.2 lakh/year.
- Star centred on D: 5 links, 10 ports, Rs 8.5 lakh/year.
- Full mesh: 6×5/2 = 15 links, 30 ports, Rs 25.5 lakh/year.
- Hybrid: 6 links, 12 ports, Rs 10.2 lakh/year.

### 2.2 Single-link failure
A bus/chain can be split by a cut on the path to E or F. In a star, cutting D–E isolates E and cutting D–F isolates F. A ring survives one link cut because traffic can travel in the opposite direction. A full mesh has alternate paths after one link failure.

### 2.3 Cheapest qualifying hybrid
Create a triangle among critical sites D, E and F: D–E, E–F and F–D. Connect A, B and C individually to D. This gives six links and 12 router ports. Cost = 6 × Rs 1.70 lakh = Rs 10.2 lakh/year. If D–E fails, E reaches D through F; if D–F fails, F reaches D through E; if E–F fails, both retain direct links to D.

### 2.4 Python program
See Task02/reachability.py. It builds an undirected graph, performs depth-first search and tests every possible single-link removal. Expected pass counts: bus 3/5, ring 6/6, star 3/5, mesh 15/15 and hybrid 6/6.

### Additional questions
If A is also critical, the proposed hybrid does not meet the stronger requirement because A–D is its only link. Add a second independent path for A, such as A–E, or include A in a resilient core ring. For seven sites, full mesh links = 7×6/2 = 21; star links = 7−1 = 6.

### MPLS VPN alternative
At Rs 60,000 per site plus one Rs 25,000 port, six sites cost 6 × Rs 85,000 = Rs 5.10 lakh/year, excluding other charges. A failed access circuit isolates that site; a carrier-core failure may affect multiple sites. Dual-homing adds a second access circuit, preferably through a diverse route and separate POP/provider.

## Task 3 – Devices, media and cabling (9 marks)

### 3.1 Cable-run review
The permanent link limit is 90 m and the complete copper channel limit is 100 m.
- 70 m reading-hall AP: acceptable if channel and installation meet limits; Cat6 is suitable.
- 88 m computer lab: within 90 m but leaves little margin; Cat6A is preferred for new high-capacity installation.
- 102 m staff room: exceeds 100 m; move the switch or use fibre to a local switch.
- 95 m CCTV: acceptable only if 95 m is the complete channel and permanent link is at most 90 m; if it is fixed cable length, it fails.
- 380 m main-building link: use fibre, not one copper Ethernet run.

### Split-pair fault
Wiring pins in numerical order can separate conductors that should form a twisted pair. A continuity tester may pass because each pin has electrical continuity, but the link can fail at gigabit speed because pair balance and crosstalk performance are poor. Use a cable certifier to test wire map, split pairs, NEXT, return loss and length.

### 3.2 Device selection and domains
Use Layer-2 managed switches for endpoint access, Layer-3 switches for high-speed inter-VLAN routing, routers for WAN connectivity, APs for wireless access and firewalls for security. Do not use hubs. Each switched physical port is its own collision domain; full-duplex Ethernet has no collisions. Each VLAN is a broadcast domain. Four VLANs (staff, students, servers, guests) mean four broadcast domains.

### 3.3 Bill of materials
Include managed access switches, Layer-3 distribution switch, router, firewall, APs, Cat6A cable, fibre backbone, patch panels, racks, connectors, patch cords, SFP/SFP+ optics and UPS. Measure actual cable routes and add 10% spare. Exact quantities require floor plans, outlet counts and AP locations.

### 3.4 T568A/T568B pinout
| Pin | T568A | T568B |
|---|---|---|
|1|White/Green|White/Orange|
|2|Green|Orange|
|3|White/Orange|White/Green|
|4|Blue|Blue|
|5|White/Blue|White/Blue|
|6|Orange|Green|
|7|White/Brown|White/Brown|
|8|Brown|Brown|

A straight-through cable uses the same standard at both ends (A-A or B-B). Test wire map and performance, not continuity alone.

### Fibre versus 5 GHz bridge
Fibre at 380 m offers stable high capacity, low electromagnetic interference and future upgrades. A 5 GHz bridge may avoid trenching but needs clear line of sight, alignment, legal radio settings and lightning protection; rain and interference can reduce availability. Fibre is preferred for a permanent critical backbone; wireless may be a temporary or backup path.

## Task 4 – Shared media, WLAN, backbone and WAN (7 marks)

### 4.1 ALOHA and CSMA/CD
Pure ALOHA: S = G e^(−2G). Slotted ALOHA: S = G e^(−G).
- G=0.5: pure = 0.1839 (18.39%); slotted = 0.3033 (30.33%).
- G=1: pure = 0.1353 (13.53%); slotted = 0.3679 (36.79%).

For 200 m shared Ethernet, propagation speed = 2×10^8 m/s. One-way delay = 1 μs; round trip = 2 μs. At 100 Mbps, bits in 2 μs = 200 bits = 25 bytes. At 1 Gbps, bits in 2 μs = 2,000 bits = 250 bytes. Standard minimum Ethernet frame is 64 bytes. Switched full-duplex Ethernet avoids collisions and does not need CSMA/CD. Wi-Fi uses CSMA/CA because a radio cannot reliably detect a collision while transmitting.

### 4.2 Wi-Fi 6 for 250 phones
Plan AP quantity by coverage and capacity; an initial design might use 8–10 APs (about 25–32 clients/AP), then validate with a site survey and traffic measurements. At 2.4 GHz, use 20 MHz channels 1, 6 and 11 with careful reuse. At 5 GHz, use a non-overlapping channel plan permitted by local rules; 20/40 MHz widths are often practical in dense deployments.
- OFDMA divides a channel into resource units for multiple clients.
- MU-MIMO serves multiple compatible clients using spatial streams.
- Target Wake Time schedules client wake periods and saves airtime/battery.
- BSS colouring helps identify overlapping co-channel BSS transmissions.
Bluetooth is suitable for headsets and clickers, not high-throughput phone access or backbone links.

### 4.3 ATM, MPLS and WAN
AAL5 data = 1,500-byte IP packet + 8-byte trailer = 1,508 bytes. ATM cells = ceiling(1,508/48) = 32. Wire bytes = 32×53 = 1,696. Overhead versus the 1,500-byte IP packet = (1,696−1,500)/1,500×100 = 13.07%. Two MPLS labels add 8 bytes, or 8/1,500×100 = 0.533%.
- Frame Relay uses DLCI.
- ATM uses VPI/VCI.
- MPLS uses labels.
Label example: ingress pushes 17; next router swaps 17→24; next swaps 24→39; egress removes the label.
Leased lines provide dedicated capacity but usually cost more. MPLS VPN offers provider-managed connectivity and QoS classes subject to SLA. SD-WAN can steer traffic over two broadband links based on loss, latency and jitter, but broadband is not necessarily guaranteed.

## Task 5 – VLANs and switch configuration (7 marks)

### 5.1 VLANs and trunk
Create VLAN 100 Staff, 200 Students, 300 Guest and 99 Native-Mgmt. Assign Fa0/1–8 to staff, Fa0/9–20 to students, Fa0/21–24 to guest. Configure Gi0/1 as an 802.1Q trunk allowing only 99,100,200,300. A VLAN tag adds 4 bytes; a standard 1,518-byte Ethernet frame becomes 1,522 bytes when tagged.

### 5.2 Inter-VLAN routing and ACLs
Use router-on-a-stick or Layer-3 switch SVIs. Example subnets: VLAN100 192.168.100.0/24; VLAN200 192.168.200.0/24; VLAN300 192.168.30.0/24; VLAN99 192.168.99.0/24. Guests should reach the internet but not private internal networks. Students should reach only library-server services approved by policy and should not access staff devices.

### 5.3 Tests and broadcast domains
Before VLANs, the common LAN is one broadcast domain. After creating four VLANs there are four broadcast domains. Test student-to-staff (blocked), student-to-library-server (permitted services only), guest-to-internet (allowed), guest-to-private-network (blocked). Record ping and ACL evidence.

### Layer-3 switch alternative
Router-on-a-stick routes all inter-VLAN traffic over one trunk, which can become a bottleneck. A Layer-3 switch with SVIs can route internally at switching-fabric speed and use multiple high-speed paths. Router-on-a-stick remains suitable for small, low-traffic or budget-constrained networks.

## Task 6 – Business-park design challenge (13 marks)

### Stage 1: Requirements
Five towers × 800 employees = 4,000 employees. At 1.5–2 connected devices per employee, plan for 6,000–8,000 employee devices before guests, CCTV and building systems. Define measurable targets for availability, segmentation, capacity, Wi-Fi coverage, security, growth and dual-ISP failover.

### Stage 2: Hierarchical hybrid topology
Use two Layer-3 core switches in the data centre. Each tower has a distribution pair connected to both core switches using diverse fibre paths. Floor access switches connect PCs, phones, cameras and APs. Use star access connections, redundant mesh-like core paths and routed point-to-point links between core and distribution.

### Stage 3: Device and security decisions
Use redundant Layer-3 core/distribution switches, PoE access switches, single-mode fibre between buildings, Cat6A to endpoints, centrally managed Wi-Fi APs, redundant firewalls and two ISP connections. Separate tenant, management, guest, CCTV/IoT and data-centre networks. Guest clients must be internet-only; cameras must reach only approved recording and management servers.

### Stage 4: Addressing and capacity
Example address blocks:
- Tenant: 10.10.0.0/16
- Management: 10.20.0.0/16
- Guest: 10.30.0.0/16
- CCTV/IoT: 10.40.0.0/16
- Data centre: 10.50.0.0/16
- Network transit: 10.255.0.0/16

Assume 25% of 800 tower users are active simultaneously (200 users) and each averages 4 Mbps: 200×4 = 800 Mbps. Add 30% headroom: 1.04 Gbps. A single 1 Gbps uplink is insufficient; consider 2×10 Gbps diverse uplinks per tower, then validate with real traffic. For 48×1 Gbps access ports feeding one 10 Gbps uplink, oversubscription = 48/10 = 4.8:1. With two active 10 Gbps uplinks, it is 48/20 = 2.4:1.

Bill of materials includes two core switches, ten tower distribution switches (two per tower), access switches sized by floor ports, data-centre leaf switches, redundant edge firewalls/routers, dual ISP circuits, fibre, Cat6A, optics, APs, racks and UPS. Exact quantities require building plans and site survey.

### Stage 5: Packet Tracer and tests
Model two towers, dual core, data-centre server, guest and CCTV VLANs, two ISP routers and representative endpoints. Test same-VLAN connectivity, tenant isolation, guest internet-only access, CCTV restrictions, ISP failover and survival of a tower-to-core link failure. Save simulation, configurations, ping/traceroute output and screenshots.

### Alternative: large Layer-2 versus routed distribution
A large Layer-2 network has larger broadcast domains and can suffer broad impact from loops or misconfiguration. Spanning Tree blocks loops but recovery depends on configuration. A routed distribution layer with OSPF and equal-cost paths provides smaller failure domains and can use multiple active paths. Routed distribution is recommended for eight years of growth.

## Conclusion
A reliable network should match topology to availability, capacity, security and budget. Switched extended stars suit labs; a small redundant core suits critical sites; fibre and standards-compliant cabling suit campus backbones; VLANs and ACLs provide segmentation; Wi-Fi 6 supports dense wireless clients; and a routed hierarchical design supports business-park growth.
