def visualize_real_chain(blockchain_logger):

    chain = blockchain_logger.get_chain()

    print("\n===== BLOCKCHAIN VIEW =====\n")

    for block in chain:
        print(f"Block #{block['index']}")
        print("Time:", block["timestamp"])
        print("Prev Hash:", block["prev_hash"])
        print("Hash:", block["hash"])
        print("Data:", block["data"])
        print("-" * 40)