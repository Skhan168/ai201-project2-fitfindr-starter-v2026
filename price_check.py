from agent import _parse_query
from mcp_client import call_tool

QUERIES = [
    "vintage graphic tee under $30",
    "denim jacket under $50",
    "silk slip dress in midi length under $40",
    "baggy cargo pants under $40",
    "tee under $20",
]

for i, q in enumerate(QUERIES, 1):
    p = _parse_query(q)
    results = call_tool("search_listings", {
        "description": p["description"],
        "size": p["size"],
        "max_price": p["max_price"],
    })
    prices = [r["price"] for r in results]
    over = [x for x in prices if x > p["max_price"]]
    verdict = "PASS" if not over else "FAIL"
    print(f"Query {i}: {q!r}  ceiling={p['max_price']}  {len(prices)} results")
    print(f"  prices: {prices}")
    print(f"  over ceiling: {over or 'none'}  -> {verdict}")