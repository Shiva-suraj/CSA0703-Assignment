"""Calculate loss, average one-way delay and RFC 3550-style jitter."""
TRACE = [
    (1, 0, 48), (2, 20, 71), (3, 40, 86), (4, 60, None),
    (5, 80, 131), (6, 100, 142), (7, 120, 175), (8, 140, 190),
    (9, 160, None), (10, 180, 236), (11, 200, 248), (12, 220, 271)
]

def metrics(trace):
    received = [(seq, tx, rx) for seq, tx, rx in trace if rx is not None]
    loss = 100 * (len(trace) - len(received)) / len(trace)
    delays = [rx - tx for _, tx, rx in received]
    avg_delay = sum(delays) / len(delays) if delays else 0.0
    jitter = 0.0
    for i in range(1, len(received)):
        _, tx1, rx1 = received[i - 1]
        _, tx2, rx2 = received[i]
        variation = abs((rx2 - rx1) - (tx2 - tx1))
        jitter += (variation - jitter) / 16
    return loss, avg_delay, jitter

if __name__ == "__main__":
    loss, delay, jitter = metrics(TRACE)
    print(f"packet loss {loss:.1f} %")
    print(f"average delay {delay:.1f} ms, jitter {jitter:.2f} ms")
