# Assignment 5 – CO5
## Measuring Network Performance and Securing Applications

**Student:** A. Siva suraj sai  
**Register Number:** 192425276  
**Course:** Computer Networks (CSA07)  
**Total:** 50 marks  
**GitHub repository:** https://github.com/Shiva-suraj/CSA0703-Assignment

This folder contains expanded worked answers and implementation guidance for the supplied CO5 Assignment 5 brief. Numerical values are calculated examples. Real-network measurements, Wireshark captures, simulator files and screenshots must be collected by the student and added to the task folders.

## Case study
An online ticket-booking company provides a booking/payment website, email confirmations, live chat, voice support, recorded help videos and nightly synchronisation with 15 regional offices. Festival traffic causes slow pages and choppy calls; a previous denial-of-service incident took the booking site offline for two hours.

---

# PART A – DESIGN

## A1 – Where does the delay come from? (7 marks)

### A1.1 Delay calculation
Given packet size 1,200 bytes = 9,600 bits, link rate 50 Mbps, distance 1,800 km, four routers, each with 0.8 ms queuing and 0.05 ms processing. Assume fibre propagation speed 2 × 10^8 m/s.

- Transmission = 9,600 / 50,000,000 = 0.000192 s = **0.192 ms**.
- Propagation = 1,800,000 / (2 × 10^8) = **9 ms**.
- Queuing = 4 × 0.8 = **3.2 ms**.
- Processing = 4 × 0.05 = **0.2 ms**.
- Total = 0.192 + 9 + 3.2 + 0.2 = **12.592 ms**.

Propagation dominates (about 71.5%). Upgrading links to 500 Mbps reduces transmission to 0.0192 ms, saving only 0.1728 ms. New total is about 12.4192 ms if other delays stay unchanged. Therefore bandwidth alone will not solve this example; routing distance, congestion and queue management matter more.

### A1.2 Bandwidth-delay product
BDP = 10 Gbps × 0.040 s = 400,000,000 bits = **50,000,000 bytes (about 47.68 MiB)**. A 128 KiB TCP window holds 131,072 bytes. Maximum throughput = 131,072 / 0.04 = 3,276,800 bytes/s = **26.2144 Mbps**. The window is much smaller than the BDP, so there is not enough unacknowledged data in flight to fill the link. TCP window scaling and sufficiently large buffers are required.

### A1.3 Targets and measurement tools
| Application | Example target | Tools |
|---|---|---|
| Booking page | p95 load <2 s; loss <1%; DNS <100 ms | Browser timing, ping, traceroute, Wireshark |
| Payment page | p95 server response <1 s; valid TLS; no transaction loss | Browser tools, TLS capture, application logs |
| Voice | one-way delay <150 ms; jitter <30 ms; loss <1% | RTP analysis, iperf3 UDP, ping |
| Recorded video | sustained throughput ≥ bitrate ×1.3 | iperf3, player statistics, SNMP |
| Email | internal delivery usually <60 s | SMTP logs, DNS MX lookup, Wireshark |
| Nightly sync | complete in maintenance window; integrity verified | rsync logs, iperf3, SNMP |

Active measurement injects test traffic (ping, traceroute, iperf3). Passive measurement observes existing traffic/counters (Wireshark, SNMP, logs). Browser real-user monitoring can collect DNS, connect, TLS, TTFB, download time, geography and browser errors. It cannot independently reveal router queue occupancy, physical-layer loss or unused path capacity. Combine real-user monitoring with synthetic tests and network telemetry.

## A2 – Follow the application protocols (5 marks)

### A2.1 SMTP
Example booking confirmation exchange:
```text
C: EHLO booking.example.com
S: 250-mail.booking.example.com
S: 250-STARTTLS
C: STARTTLS
S: 220 Ready to start TLS
  [TLS handshake and client authentication]
C: MAIL FROM:<no-reply@booking.example.com>
S: 250 2.1.0 Sender accepted
C: RCPT TO:<customer@example.net>
S: 250 2.1.5 Recipient accepted
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: Subject: Booking confirmation
C: Booking reference: BK10293
C: .
S: 250 2.0.0 Message accepted
C: QUIT
S: 221 Bye
```
MX records identify the receiving mail server. Port 587 is for authenticated message submission. STARTTLS encrypts the connection. SPF identifies authorised senders, DKIM signs messages and DMARC tells receivers how to handle failed alignment and provides reports. These controls reduce forged confirmation emails.

### A2.2 SFTP, rsync and SNMP
FTP uses a control connection (TCP 21) and a separate data connection, complicating firewalls/NAT. SFTP uses SSH on TCP 22 and one connection. rsync over SSH transfers changed blocks, preserves metadata and supports efficient repeated synchronisation.

SNMP counter delta = 1,425,000,000 − 1,250,000,000 = 175,000,000 octets in 60 s. Rate = 175,000,000 × 8 / 60 = **23.33 Mbps**. Utilisation on 100 Mbps = **23.33%**. Calculate inbound/outbound separately; consider counter wrap and 32-bit versus 64-bit counters. SNMPv3 provides authentication, integrity and optional privacy/encryption; SNMPv2c community strings are not encrypted.

### A2.3 DNS and HTTP
High DNS timing indicates resolver/cache issues; high connect time indicates TCP/path delay; high TLS time indicates handshake/certificate/server issues; high TTFB suggests server/application/database delay; high download time suggests large content or low throughput. HTTP 3xx is redirect, 4xx is client/request error (404, 401), and 5xx is server error (500, 503).

**Alternative: HTTPS cloud object store for 20 GB.** Assuming decimal 20 GB = 160 Gb and 5% overhead, useful rate = 95 Mbps. Time = 160,000 Mb / 95 Mb/s = **1,684 s = 28.1 minutes**. SFTP is convenient with existing infrastructure; cloud object storage often offers multipart/resumable upload, checksums and regional durability. Compare storage, request and egress charges against server maintenance and bandwidth.

## A3 – Peer-to-peer, VoIP and overlays (5 marks)

### A3.1 Distribute a 6 GB package
6 GB = 48 Gb. Client-server lower bound is 48 Gb / 200 Mbps = **240 s (4 min)**, limited by head-office upload. In ideal P2P, 15 offices contribute 15 × 40 = 600 Mbps upload; combined with the 200 Mbps seed, aggregate is 800 Mbps. Idealised lower bound = 48 Gb / 800 Mbps = **60 s**. Real P2P is slower due to startup, piece scheduling, protocol overhead and peer availability. P2P may be unsuitable for confidential data, offline peers or restricted uploads.

### A3.2 Voice bandwidth
20 ms packetisation gives 50 packets/s. G.729 payload = 8 kbps × 0.02 s = 160 bits = 20 bytes. Add 40-byte IP/UDP/RTP header: 60 bytes × 8 × 50 = **24 kbps per direction** (excluding Layer 2). 1 Mbps / 24 kbps = **41 calls** in this simplified model. Real capacity is lower after Layer-2/tunnel overhead and headroom. SIP establishes/modifies/terminates sessions; RTP carries media.

### A3.3 Overlay networks
A CDN uses edge caches near users to reduce video/static-content latency and origin load. A VPN creates encrypted logical tunnels over the public internet for secure regional-office connectivity. With a 1 Gbps CDN edge in each region, ideal edge delivery time for 6 GB is 48 Gb / 1,000 Mbps = **48 s** per region if content is pre-positioned. The 200 Mbps origin needs 240 s to seed one copy; pre-positioning to all edges needs sufficient origin capacity or scheduled replication. CDN cost includes storage, cache-fill and delivery; it improves geographic resilience.

## A4 – Find the hole in the firewall (4 marks)

### A4.1 SSL/TLS
The certificate chain links the server certificate to a trusted CA and lets the browser validate hostname, validity and signatures. TLS negotiates version, cipher and key agreement, authenticates the server and derives session keys. On public Wi-Fi an observer may see IPs, timing, packet sizes and some metadata, but correctly protected HTTPS content, passwords and payment details remain encrypted (unless endpoint or trust is compromised).

### A4.2 Firewall rules
Rules are top-to-bottom. Original rule 2 allows all sources to TCP 3306, making rule 3 (deny any to 3306) unreachable. This exposes the database. Correct order:
```text
1 allow tcp any           -> 443
2 allow tcp 10.5.0.0/16   -> 3306
3 deny   tcp any           -> 3306
4 allow tcp 10.5.0.0/16   -> 22
5 deny   tcp any           -> 22
6 allow udp any            -> 53
7 deny   all any           -> any
```
A stateless filter checks packet headers independently. A stateful firewall tracks permitted sessions and allows valid replies. An application proxy terminates and inspects application requests, enabling URL/content policy but adding processing delay.

### Completed stateful firewall function
```python
INSIDE = "10.5."
table = set()
def decide(src, sport, dst, dport):
    if src.startswith(INSIDE):
        table.add((src, sport, dst, dport))
        return "allow"
    return "allow" if (dst, dport, src, sport) in table else "deny"
```
For a 60-second timeout, store each tuple with a timestamp and remove entries older than 60 seconds before lookup. A reply after 90 seconds is denied because the state has expired. A production firewall should track TCP flags/state too.

A cloud WAF can detect SQL injection and cross-site scripting patterns that a basic packet firewall cannot understand. It adds inspection latency, so pilot it and measure p95 response time. It is justified for a public booking/payment service alongside secure coding and rate limits.

## A5 – Denial-of-service protection (4 marks)

### A5.1 Attack sizing
Half-open capacity = 2,048 connections with 45 s timeout. Average SYN rate to fill it = 2,048 / 45 = **45.51 SYN/s**, assuming no entries complete or expire early. SYN cookies encode connection state in the SYN-ACK and allocate full state only after a valid ACK.

DNS amplification = 3,000-byte answer / 40-byte query = **75×**. A 10 Mbps attacker could theoretically induce **750 Mbps** at the victim before overhead/limits. Reflection and spoofing make victim-side blocking difficult.

### A5.2 Protection plan
| Attack | Controls | Reason |
|---|---|---|
| SYN flood | SYN cookies, SYN rate limits, connection limits, upstream scrubbing | Reduces half-open state pressure and absorbs floods upstream |
| DNS amplification | BCP 38 ingress filtering, resolver response-rate limits, scrubbing | Stops spoofing and limits amplification |
| HTTP flood | CDN/WAF, app rate limits, bot detection, autoscaling | Filters abusive application requests |

For 50,000 sources, one ACL entry per source means 50,000 entries. At one second per manual entry, that is 13.9 hours before validation; spoofed addresses also change. Individual blocking is not scalable.

---

# PART B – IMPLEMENTATION AND EXPERIMENTAL INVESTIGATION

## B1 – Measure a real network (7 marks)

### B1.1 Delay and path
Select authorised servers in the same city, another state and another continent. Run 100 pings and traceroute at morning, afternoon and evening. Record min/average/max RTT, jitter, loss and route.
```bash
ping -c 100 <server>
traceroute <server>
# Windows: ping -n 100 <server> ; tracert <server>
```
Propagation lower bound for a 1,000 km one-way fibre path is approximately 2 × 1,000,000 / (2 × 10^8) = 10 ms RTT. Actual RTT is higher due to route length, switching, queuing and processing.

### B1.2 Throughput
```bash
# Receiver
iperf3 -s
# Sender
iperf3 -c <receiver-ip> -t 30
iperf3 -c <receiver-ip> -t 30 -P 4
iperf3 -c <receiver-ip> -u -b 20M -t 30
```
Repeat on wired and wireless links at least three times. Record link speed, TCP bitrate/retransmissions, UDP bitrate/jitter/loss and test duration.

### B1.3 and B1.4 Wireshark
Capture only your own authorised call/stream. RTP Stream Analysis provides sequence, loss and jitter information. Throughput = captured payload bits / capture duration. One-way delay needs synchronised clocks or controlled endpoint timestamps. Compare actual measurements with A1.3 targets and label pass/borderline/fail.

### Completed VoIP metrics function
```python
def metrics(trace):
    got = [(s, tx, rx) for s, tx, rx in trace if rx is not None]
    loss = 100 * (len(trace) - len(got)) / len(trace)
    delays = [rx - tx for s, tx, rx in got]
    avg_delay = sum(delays) / len(delays) if delays else 0.0
    jitter = 0.0
    for i in range(1, len(got)):
        _, tx1, rx1 = got[i-1]
        _, tx2, rx2 = got[i]
        d = abs((rx2-rx1) - (tx2-tx1))
        jitter += (d-jitter)/16
    return loss, avg_delay, jitter
```
The supplied trace has 2 losses in 12 packets = **16.7% loss**. The assignment's expected result is average delay 49.8 ms, jitter 2.80 ms, MOS 2.75 (poor). Remove the two lost packets and execute the original complete program to obtain the new MOS. A calculated MOS can differ from listener opinion due to burst loss, concealment, echo and background noise.

## B2 – Simulate under varying conditions (5 marks)
Model head office, two regional offices, internet/WAN, booking servers and voice endpoints in Packet Tracer or NS-3. Test bandwidth (10/50/100 Mbps), one-way delay (10/40/100 ms) and users (50/100/500). Record throughput, RTT, loss, jitter and queue occupancy. Run 500-user flash-sale load, first best-effort then with LLQ priority for voice. LLQ should reduce voice delay under congestion, but policing is needed so voice cannot starve other traffic. Packet Tracer is simple for logical topology; NS-3 offers detailed simulation; Linux namespaces with tc netem include real host-stack behaviour but require more setup.

## B3 – Performance under stress and attack (8 marks)

### B3.1 Delay/loss profiles
| Profile | Added delay | Loss |
|---|---:|---:|
| 1 | 20 ms | 0.5% |
| 2 | 100 ms | 2% |
| 3 | 250 ms | 8% |

```bash
# Only on a controlled test namespace/interface
sudo tc qdisc add dev veth0 root netem delay 100ms loss 2%
tc qdisc show dev veth0
sudo tc qdisc del dev veth0 root
```
Run each profile for a fixed period at least three times. TCP goodput generally falls as RTT/loss rise due to congestion control and retransmissions. Voice quality declines with higher delay, jitter and loss.

### B3.2 TCP window
Use iperf3 with small and large windows (e.g. `-w 128K` and `-w 8M`) on a controlled long-delay path. Compare with A1.2 BDP of about 47.68 MiB. A window smaller than BDP limits throughput to window/RTT; actual performance also depends on autotuning, congestion control and loss.

### B3.3 Firewall and controlled flood
Verify HTTPS remains accessible, only 10.5.0.0/16 reaches TCP 3306 and SSH, DNS is permitted as required, and other inbound traffic is denied. In an isolated lab only, send controlled connection requests to a test server and compare response time/half-open queue with SYN cookies and rate limiting enabled and disabled. Never test a public site or shared network.

### B3.4 Queue management
Drop-tail fills the queue then drops packets, potentially creating bufferbloat and synchronised TCP loss. RED probabilistically drops/marks before full capacity. ECN marks packets instead of dropping them when endpoints and devices support it. Measure p95 queue delay, throughput, loss and retransmissions. Choose the approach from repeatable test evidence.

## B4 – Final engineering decision (5 marks)
If each user's average demand stays constant, tripling customers approximately triples offered load. If baseline utilisation is U%, projected utilisation is about 3U% until saturation; after saturation, queue delay and loss can rise sharply. Use measured RTTs to estimate overseas delay rather than guessing.

Test legitimate booking, payment, email and voice at three times baseline load. Confirm rate limits do not block normal customers, payment APIs remain reachable, database access is restricted and WAF/firewall logs show malicious requests blocked. Record false positives and p95 latency.

**Recommendation:** deploy a CDN for static assets/help videos; add regional application instances/read replicas where consistency permits; use QoS/LLQ for voice; increase WAN capacity; use SYN cookies, connection limits, upstream DDoS scrubbing, BCP 38 and a managed WAF; monitor with real-user metrics, synthetic probes, SNMPv3 and application logs. A multi-region cloud design can reduce overseas user-to-app RTT, but database replication adds cost and consistency delay. Estimate the benefit from measured RTT to the current and proposed regional endpoints.

## Practical evidence checklist
- Create TaskA1–TaskA5 and TaskB1–TaskB4 folders.
- Add completed Python programs, inputs, outputs and task READMEs.
- Add permitted Wireshark .pcapng captures with packet annotations.
- Add ping, traceroute, iperf3, SNMP and tc outputs with timestamps.
- Add Packet Tracer/NS-3 project files and configuration exports.
- Add baseline/congestion/loss/security comparison tables.
- Commit work progressively and be prepared to explain every calculation.

## References
- CO5 – Assignment 5 – CSA07, supplied assignment PDF.
- RFC 5321 (SMTP), RFC 6409 (Message Submission), RFC 7208 (SPF), RFC 6376 (DKIM), RFC 7489 (DMARC).
- RFC 3550 (RTP), RFC 8446 (TLS 1.3), RFC 9293 (TCP).
- RFC 3411/RFC 3414 (SNMP architecture/security), RFC 4987 (TCP SYN flooding).
- BCP 38 – ingress filtering.

**Academic note:** The report is an expanded worked guide. Execute the code and collect your own measurements/screenshots. DoS experiments must remain in an isolated lab or simulator.
