import asyncio

async def fetch_data(source: str, delay: float) -> dict:
    """
    Simulate fetching data from a source that takes some time.
    """
    print(f"Starting to fetch from {source}...")
    await asyncio.sleep(delay)
    print(f"Finished fetching from {source}")
    return {"source":source, "delay":delay}


async def fetch_serial() -> list[dict]:
    """Fetch three sources sequentially. Total time is the sum of delays."""
    start = asyncio.get_event_loop().time()
    
    result_a = await fetch_data("source_A", 1.0)
    result_b = await fetch_data("source_B", 1.0)
    result_c = await fetch_data("source_C", 1.0)
    
    duration = asyncio.get_event_loop().time() - start
    print(f"Serial version took {duration:.2f} seconds")
    return [result_a, result_b, result_c]

async def fetch_parallel() -> list[dict]:
    """Fetch three sources concurrently. Total time is roughly the max delay."""
    start = asyncio.get_event_loop().time()

    # We wrap around list() because Type checker thinks asyncio.gather() is returning a tuple, while your function says it returns a list.
    results = list(await asyncio.gather(
    fetch_data("source_A", 1.0),
    fetch_data("source_B", 1.0),
    fetch_data("source_C", 1.0),
    ))
    
    duration = asyncio.get_event_loop().time() - start
    print(f"Parallel version took {duration:.2f} seconds")
    return results

async def main():
    print("--- Serial fetch ---")
    serial_results = await fetch_serial()
    print(f"Got {len(serial_results)} results\n")
    
    print("--- Parallel fetch ---")
    parallel_results = await fetch_parallel()
    print(f"Got {len(parallel_results)} results")


if __name__ == "__main__":
    asyncio.run(main())