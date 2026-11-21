# Task 6 – Business Park Network Design

Five towers × 800 employees = 4,000 employees. At 1.5–2 devices per employee, plan for 6,000–8,000 employee devices before guests, CCTV and building systems.

## Topology
- Two redundant Layer-3 core switches in the data centre.
- Two distribution switches per tower, each with diverse fibre uplinks to both core switches.
- Managed PoE access switches on each floor.
- Redundant edge firewalls/routers and two ISP connections.
- Separate tenant, management, guest, CCTV/IoT and data-centre networks.

## Address plan
| Segment | Prefix |
|---|---|
| Tenant | 10.10.0.0/16 |
| Management | 10.20.0.0/16 |
| Guest | 10.30.0.0/16 |
| CCTV/IoT | 10.40.0.0/16 |
| Data centre | 10.50.0.0/16 |
| Network transit | 10.255.0.0/16 |

## Capacity example
Assume 25% of 800 users are active at peak and each averages 4 Mbps: 200 × 4 = 800 Mbps. Add 30% headroom = 1.04 Gbps. Consider 2 × 10 Gbps diverse uplinks per tower and validate with real traffic.

For 48 × 1 Gbps access ports and one 10 Gbps uplink, oversubscription = 48/10 = 4.8:1. With two active 10 Gbps uplinks it is 48/20 = 2.4:1.

## Security
- Guest Wi-Fi: internet-only, with client isolation.
- CCTV: cameras reach approved recording servers only.
- Management: reachable only from administrator systems.
- Tenant: isolated according to tenant policy.
- Data centre: allow only required application ports.

## Validation
Test gateway access, tenant isolation, guest internet-only access, camera restrictions, alternate-path connectivity after a tower-to-core link failure, and ISP failover. Record convergence time and screenshots. Final quantities require floor plans, AP survey, camera bitrates and concurrency estimates.
