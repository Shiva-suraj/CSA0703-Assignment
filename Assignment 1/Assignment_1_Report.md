# Computer Networks – Assignment 1 (CO1)

**Name:** A. Siva suraj sai  
**Register Number:** 192425276  
**Title:** Keep the Data of an Automated Warehouse Correct, Complete and On Time

This report follows the uploaded CO1 Assignment 1 question paper. Calculations are shown with units. Where the question does not specify a value, the assumption is stated.

## Task 1 – Work Out the Load Before Buying the Link (4 marks)

### Traffic calculation
- Robots: each sends 120 bytes every 4 ms. Per robot = 120 × 8 / 0.004 = 240,000 bit/s = 0.24 Mbps. For 60 robots = **14.40 Mbps**.
- RFID: 800 × 200 bytes/s × 8 = **1.28 Mbps**.
- CCTV: 32 × 6 Mbps = **192 Mbps**.
- Office/handheld: 200 × 15% = 30 active users; 30 × 3 Mbps = **90 Mbps**.
- One zone total = 14.4 + 1.28 + 192 + 90 = **297.68 Mbps**.
- Six zones = 297.68 × 6 = **1,786.08 Mbps (1.786 Gbps)**.

CCTV carries the most data, but robot commands have the strictest delay requirement (8 ms). A 1 Gbps uplink is enough for one zone on average, but not for six zones. If CCTV and robot commands share a FIFO queue, video bursts can delay commands beyond the deadline; use QoS and a protected low-latency robot queue.

A 50 ms delay is most harmful to robot commands, then RFID parcel events, handheld scanners, office applications, and buffered CCTV. If CCTV sends only 8% of its continuous stream, CCTV becomes 192 × 0.08 = 15.36 Mbps. Revised zone total = **121.04 Mbps**; six zones = **726.24 Mbps**. This is below 1 Gbps on average, but burst capacity and headroom are still needed.

## Task 2 – Count the Domains in the Annexe Drawing (3 marks)

The two hubs each form one shared collision domain. The first switch has seven active ports (two hub links, four cameras and router G0/0); the second switch has seven active ports (router G0/1 and six printers). Total collision domains = **14**. The router separates the two sides into **2 broadcast domains**.

- Hub: Layer 1; repeats signals and does not split collision domains.
- Switch: Layer 2; forwards frames using MAC addresses.
- Router: Layer 3; routes IP packets and does not forward Layer-2 broadcasts.
- Switch-to-end-device and router-to-switch Ethernet links are point-to-point; each hub segment is shared/multipoint.

| Standard | Standards body |
|---|---|
| TIA/EIA-568 cabling | TIA / EIA |
| Wi-Fi 6 (IEEE 802.11ax) | IEEE |
| TCP (RFC 9293) | IETF |
| OSI (ISO/IEC 7498-1) | ISO/IEC |
| Bluetooth | Bluetooth SIG |
| 5G NR | 3GPP |

With one managed switch and three VLANs, 31 active switch ports (20 PCs + 4 cameras + 6 printers + one trunk) create 31 point-to-point collision domains. Three VLANs create three broadcast domains. This removes hub collision segments and isolates broadcasts, but does not itself provide encryption, QoS or extra uplink bandwidth.

## Task 3 – Open a Captured Scanner Message Layer by Layer (4 marks)

| Capture item | OSI layer | PDU |
|---|---|---|
| Ethernet II MAC addresses and EtherType | Layer 2 | Frame |
| IPv4 source/destination and TTL | Layer 3 | Packet |
| TCP ports, sequence and acknowledgement | Layer 4 | Segment |
| MQTT publish payload | Application layer | Data |

TTL falls from 64 to 62, so the packet crossed **2 routers**.

For 24 application bytes, assuming 20-byte IPv4 and 20-byte TCP headers: Ethernet payload = 20 + 20 + 24 = 64 bytes. Frame = 14 + 64 + 4 FCS = **82 bytes**. Overhead = 58 bytes, or 58/82 × 100 = **70.73%** of the frame. For a 1,460-byte TCP payload, total frame = 14 + 20 + 20 + 1,460 + 4 = **1,518 bytes**; overhead ratio = 58/1,518 × 100 = **3.82%**. Larger messages use fixed headers more efficiently.

- FCS mismatch: Layer 2.
- No route to destination IP: Layer 3.
- No listener on TCP port 1883: Layer 4 / transport endpoint.
- Switch mainly inspects Layer 2; router inspects Layer 3 (and may use L4 ACLs); application firewall can inspect application payloads.

### Completed Ethernet II / FCS program
```python
import struct
import zlib

def mac_bytes(text):
    return bytes(int(part, 16) for part in text.split(":"))

def mac_text(raw):
    return ":".join(f"{b:02x}" for b in raw)

def build(dst, src, ethertype, payload):
    header = struct.pack("!6s6sH", mac_bytes(dst), mac_bytes(src), ethertype)
    payload = payload + bytes(max(0, 46 - len(payload)))
    fcs = struct.pack("<I", zlib.crc32(header + payload))
    return header + payload + fcs

def parse(frame):
    dst, src, ethertype = struct.unpack("!6s6sH", frame[:14])
    fcs_ok = struct.pack("<I", zlib.crc32(frame[:-4])) == frame[-4:]
    return mac_text(dst), mac_text(src), hex(ethertype), len(frame), fcs_ok

data = b"BIN-42 qty=17 ok"
frame = build("00:1d:9c:c7:b0:41", "3c:52:82:4e:11:07", 0x0800, data)
print("parsed       :", parse(frame))
bad = bytearray(frame)
bad[20] ^= 0x01
print("1 bit flipped: FCS ok =", parse(bytes(bad))[-1])
print(f"overhead     : {len(frame) - len(data)} bytes for {len(data)} bytes of data")
```

For 1,400 data bytes, frame size = 14 + 1,400 + 4 = 1,418 bytes; overhead is 18 bytes (1.27%). For the 16-byte payload padded to minimum size, overhead is 48 bytes (75% of the 64-byte frame). UDP has an 8-byte header versus TCP's usual 20-byte header, saving **12 bytes/message**; it also avoids TCP connection handshake/close, but gives up TCP's built-in reliability, ordering and congestion control.

## Task 4 – Choose a Medium for Each Run (4 marks)

| Run | Recommendation | Reason |
|---|---|---|
| Robot cell, 70 m, beside motors | Cat6A S/FTP or fibre | Shielding / electrical isolation |
| Office to switch, 130 m | Fibre | Exceeds 100 m copper Ethernet channel limit |
| Floor to data hall, 700 m | Single-mode fibre | Exceeds stated 550 m 1 Gbps multimode reach |
| Warehouse to data centre, 600 km | Carrier leased line / managed WAN over fibre | Long-haul service needs carrier equipment |

The 700 m run is the stated multimode-limit trap. Shannon capacity is C = B log₂(1+SNR), with SNRlinear = 10^(dB/10):
- 500 MHz, 35 dB: SNR ≈ 3162.3; capacity ≈ **5.81 Gbps**.
- 500 MHz, 12 dB: SNR ≈ 15.85; capacity ≈ **2.04 Gbps**.
- Wi-Fi alternative, 80 MHz and 18 dB: capacity ≈ **483 Mbps** (theoretical only; not a latency guarantee).

S/FTP shields reduce electromagnetic interference when screens, connectors and bonding are installed correctly.

### Completed optical link-budget functions
```python
def total_loss(km, db_per_km, connectors, splices):
    return km * db_per_km + connectors * 0.5 + splices * 0.1

def margin(tx_dbm, rx_sensitivity_dbm, loss_db):
    return (tx_dbm - loss_db) - rx_sensitivity_dbm
```

Expected link results from the question data:
- 0.7 km single-mode: loss 2.45 dB, margin 16.55 dB, OK.
- 0.7 km multimode: loss 4.30 dB, margin 5.20 dB, OK.
- 10 km single-mode: loss 6.10 dB, margin 12.90 dB, OK.
- 40 km single-mode: loss 17.00 dB, margin 2.00 dB, FAIL.

With four connectors and six splices, fixed loss is 2.6 dB. To retain 3 dB margin, fibre attenuation can be at most 13.4 dB, so distance = 13.4/0.35 = **38.29 km**. The 40 km link needs an engineered higher-budget optic, regeneration or amplification.

## Task 5 – Wi-Fi 6, 5G or Short-Range Radio for Moving Equipment? (4 marks)

For a 900 m route:
- Wi-Fi AP spacing 25 m: about 36 cells / 35 handovers; 35 × 120 ms = **4.2 seconds** unreachable time.
- 5G coverage 150 m: about 6 cells / 5 handovers; 5 × 15 ms = **75 ms** unreachable time.
- Both totals exceed the 8 ms command deadline. 5G is better in this example, but a 15 ms handover still needs overlap, local control and fail-safe handling.

5G mapping: AMRs/robots = URLLC; CCTV = eMBB; RFID = mMTC. Bluetooth suits nearby accessories; Zigbee suits low-rate sensors; NFC suits very short-range tap identification. Wi-Fi 6 fast roaming (802.11r) and OFDMA help but do not remove interference, contention and variable delay.

Zigbee reader calculation: one reader = 200 × 8 = 1.6 kbps. 120 readers = 192 kbps, requiring **2 gateways** at 100 kbps usable each. 800 readers = 1,280 kbps, requiring **13 gateways**.

## Task 6 – Interpret an Ethernet Port Report (4 marks)

CRC errors mean received frames fail the FCS check. Full-duplex switched links do not normally have collisions, so zero collisions is expected. Many CRC/frame errors suggest damaged cable, poor termination, interference, faulty port or transceiver.

100BASE-TX uses two pairs (pins 1–2 and 3–6); 1000BASE-T uses all four pairs. Test all pairs with a cable certifier; inspect patch panels and leads; check interface counters with `ethtool eth0`, `ethtool -S eth0` and `ip -s link show eth0`.

- ff:ff:ff:ff:ff:ff = broadcast.
- 33:33:00:00:00:01 = IPv6 multicast mapping.
- 3c:52:82:4e:11:07 = unicast; 3C:52:82 is its OUI prefix.

PoE: 12 × 25.5 W = 306 W; 10 × 12.95 W = 129.5 W; total = **435.5 W**. A 370 W budget is short by **65.5 W**. Add a higher-budget/second PoE switch or suitable injectors.

A star uplink has no alternate path if the link fails. A triangle with RSTP can recover through the alternate path; classic STP may take 30–50 s and RSTP about 1–2 s, depending on configuration.

## Task 7 – Will the Receiver Notice the Error? (4 marks)

Generator 10011 has degree 4. Append four zeros to data 1010011101 and divide by modulo-2 XOR. Remainder = **0010**, so codeword = **10100111010010**.

| Received frame | Remainder | Result |
|---|---|---|
| 10100111010010 | 0000 | Accept |
| 10000111000010 | 1101 | Reject |

CRC-4 detects all burst errors up to 4 bits. An error polynomial that is a multiple of the generator can be missed. Two-dimensional parity can detect and locate a single flipped bit, but a four-bit rectangle (two flips in each of two rows and columns) can escape parity checks.

For words 4500, 0054, 1C46, 4000, 4001 (hex), Internet checksum = **1E64**.

### Completed checksum code
```python
def checksum(words):
    total = 0
    for w in words:
        total += w
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF

def verify(words, csum):
    return checksum(words + [csum]) == 0
```

Swapping two 16-bit words may pass the Internet checksum because addition is commutative. CRC usually detects the order change because it processes the ordered bit sequence.

## Task 8 – Correct the Error or Ask Again? (3 marks)

For 11 data bits, r=4 because 2⁴=16 ≥ 11+4+1. Total Hamming(15,11) bits = 15; check-bit overhead = 4/15 = **26.67%**.

All pairwise distances in {000000, 011101, 101011, 110110} are 4, so dmin=4. It detects up to **3 errors** and corrects **1 error**.

Received Hamming word 1100100 differs from 1100110 at bit 6. Corrected word = **1100110**; data positions 3,5,6,7 give **0110**.

FEC corrects errors without waiting for a retransmission. ARQ detects errors and asks for another copy; on a LoRa link where retransmission costs 400 ms, FEC is useful for time-sensitive readings. Video and 5G use FEC because late retransmissions may be useless for real-time traffic.

### Completed two-dimensional parity correction logic
```python
def correct(frame):
    bad_rows = [r for r, row in enumerate(frame) if sum(row) % 2 != 0]
    bad_cols = [c for c in range(len(frame[0]))
                if sum(frame[r][c] for r in range(len(frame))) % 2 != 0]
    if not bad_rows and not bad_cols:
        return "no error"
    if len(bad_rows) == 1 and len(bad_cols) == 1:
        r, c = bad_rows[0], bad_cols[0]
        frame[r][c] ^= 1
        return ("corrected", r, c)
    return "uncorrectable"
```

At BER 1/500 over 15 bits, probability of at least one error = 1−0.998^15 ≈ **2.96%**. A 4-bit CRC detects errors but ARQ adds expected retransmission airtime of about 0.0296 × 400 ms = **11.84 ms** per reading (assuming one retry).

## Task 9 – How Big Must the Window Be? (4 marks)

For 1,200-byte frames on 1 Gbps:
- Transmission time = 1,200×8 / 1 Gbps = **9.6 μs**.
- One-way propagation = 600 km / (2×10⁸ m/s) = **3 ms**; RTT = 6 ms.
- a = 3 ms / 9.6 μs = **312.5**.
- Stop-and-wait utilisation = 1/(1+2a) = 1/626 = **0.1597%**, throughput ≈ **1.60 Mbps**.
- Window to fill link ≈ 1+2a = **626 frames**.
- Go-Back-N needs 10 sequence bits because W ≤ 2^k−1.
- Selective Repeat needs 11 sequence bits because W ≤ 2^(k−1).

With a full window and one early loss, Go-Back-N may resend the lost frame and following unacknowledged frames (up to the remaining window); Selective Repeat resends only the missing frame. HDLC uses 01111110 flags and inserts a 0 after five consecutive 1s. For data 0111110111111011, stuffed bits = **011111001111101011**.

For the alternative 500 km, 100 Mbps, 1,500-byte frame link: propagation = 2.5 ms; transmission = 0.12 ms; a ≈ 20.83; minimum window ≈ 42.67, so use **43 frames**. In the original link, a window of 400 gives 400/626 = **63.90%** utilisation and about **639 Mbps** throughput.

## Task 10 – Find Where the Delay Comes From (4 marks)

For 600 km fibre, one-way propagation = **3 ms**, RTT = **6 ms**. This is only the propagation component; routing, processing, queueing and access links add delay.

Traceroute interpretation:
- Hop 1: around 0.4–0.5 ms, local gateway.
- Hop 2: around 2.8 ms, upstream network.
- Hop 3: two probes around 3.5 ms and one 41 ms spike; likely transient queueing or ICMP rate limiting.
- Hop 4 stars: no response to traceroute probes; not proof that forwarding is broken.
- Hop 5 and 6: path continues at around 14–15 ms. The missing hop 4 means the exact location of the delay jump cannot be identified from this output alone.

Collect real evidence using `tracert` / `traceroute`, repeated `ping`, and Wireshark. Identify Ethernet MACs, IP addresses, TCP/UDP ports and application protocol. mtr repeatedly measures latency variation and loss; one traceroute is only a short snapshot. Intermediate-hop ICMP loss must be interpreted carefully.

## Task 11 – Defend the Network Design (4 marks)

Recommended design:
- Fixed robot cells: industrial Ethernet over shielded Cat6A or fibre, full duplex and QoS.
- AMRs: private 5G URLLC with overlapping cells and local fail-safe control.
- Office/handhelds: Wi-Fi 6, managed APs, fast roaming, VLANs and QoS.
- CCTV: wired Ethernet or engineered eMBB; local analytics to reduce continuous video load.
- RFID: wired or low-power sensor network with enough gateways.
- Backbone: redundant single-mode fibre with 10 Gbps-capable uplinks.
- Data-centre WAN: leased line/managed WAN; SD-WAN backup for suitable traffic.

Ethernet FCS/CRC detects frame errors. TCP provides acknowledgement, retransmission, sequencing and flow control. Use large windows on long-delay paths; FEC for noisy links where retransmission is too slow; QoS and traffic shaping for robot traffic.

Two major risks are wireless interference/roaming variability and capacity or single-point failures. For six zones, continuous-video estimate is 1.786 Gbps, so 1 Gbps is insufficient. Local analytics estimate is 726.24 Mbps average, but headroom and redundancy are still needed. SD-WAN broadband is suitable for office traffic, updates and non-urgent clips; time-critical operational traffic should use the engineered low-latency path.

## Task 12 – Re-evaluate and Adapt the Design (8 marks)

**Decision: MODIFY** the original design. Retain the fibre backbone, managed Ethernet, VLANs and Wi-Fi 6 for office/handhelds; add private 5G URLLC for AMRs and local fail-safe control.

**Assumption for traffic:** the question does not state AMR command size/interval. Assume each of 80 AMRs sends the same 120-byte command every 4 ms as the original robots. Per AMR = 0.24 Mbps; 80 AMRs = **19.2 Mbps**. Six-zone continuous-video total becomes 1,786.08 + 19.2 = **1,805.28 Mbps**. With local CCTV analytics, 726.24 + 19.2 = **745.44 Mbps**. If all 80 AMRs were in one zone, that zone would rise to 316.88 Mbps.

Task 5 shows Wi-Fi handover interruption around 4.2 seconds and 5G around 75 ms per trip estimate. Both exceed an 8 ms command deadline if treated as a full outage. 5G is a better mobility option, but still needs overlapping coverage, make-before-break where supported, local autonomy and safe-stop behaviour. Bandwidth is not the main challenge; reliable low-latency mobility is.

Revised design:
1. Private 5G URLLC for AMR command/control with overlapping aisle coverage.
2. Industrial Ethernet for fixed robot cells.
3. Wi-Fi 6 for office and handheld traffic.
4. eMBB or wired Ethernet for high-rate CCTV; local analytics to reduce backbone load.
5. Redundant single-mode fibre, managed switches, VLANs, QoS, UPS and edge controllers.
6. Local fail-safe behaviour if wireless communication is lost.

**Defence:** MODIFY rather than replace because the fixed network remains suitable. Add 5G for mobility, but verify the 8 ms end-to-end requirement with real handover, load and jitter testing. The 15 ms supplied handover estimate is still above the command deadline.

## Overall conclusion

CCTV dominates bandwidth, while robots and AMRs dominate delay risk. A single 1 Gbps uplink is insufficient for the continuous-video six-zone case, but local video analytics reduces average traffic. Managed switches, VLANs, QoS, fibre, shielded cabling, private 5G and suitable error-control mechanisms provide a scalable design. The final system must be validated with actual measurements and safe failover behaviour.

## References
- Course-provided CO1 Assignment 1 question paper.
- IEEE 802.3 Ethernet and IEEE 802.11 wireless LAN standards.
- IETF RFC 9293 – Transmission Control Protocol.
- IETF RFC 1071 – Computing the Internet Checksum.
- ISO/IEC 7498-1 – OSI Basic Reference Model.
- 3GPP specifications for 5G New Radio.
- TIA structured cabling standards and Bluetooth SIG specifications.

**Submission reminder:** Add your own executed code, Packet Tracer files, Wireshark captures, ping/traceroute output and screenshots to the task folders. The written calculations and code here do not replace the assignment's required practical evidence.
