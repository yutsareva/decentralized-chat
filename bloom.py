from bloom_filter import BloomFilter

bloom = BloomFilter(max_elements=10000, error_rate=0.1)


def add_elem(msg):
    bloom.add(msg)


def exists(msg):
    return msg in bloom
