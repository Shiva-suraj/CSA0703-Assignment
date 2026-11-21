from itertools import combinations

SITES = "ABCDEF"
LAKH_PER_LINK = 1.7
TOPOLOGIES = {
    "bus": [("A","B"),("B","C"),("C","D"),("D","E"),("E","F")],
    "ring": [("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),("F","A")],
    "star": [(site,"D") for site in "ABCEF"],
    "mesh": list(combinations(SITES, 2)),
    "hybrid": [("D","E"),("E","F"),("F","D"),
               ("A","D"),("B","D"),("C","D")]
}

def reachable(edges, start):
    graph = {site: [] for site in SITES}
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    visited = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)
    return visited

for name, edges in TOPOLOGIES.items():
    passed = 0
    for broken in edges:
        remaining = [edge for edge in edges if edge != broken]
        seen = reachable(remaining, "D")
        if "E" in seen and "F" in seen:
            passed += 1
    cost = len(edges) * LAKH_PER_LINK
    print(f"{name:<6} links {len(edges):2d} cost Rs {cost:5.1f} lakh "
          f"E and F survive {passed}/{len(edges)} cuts")
