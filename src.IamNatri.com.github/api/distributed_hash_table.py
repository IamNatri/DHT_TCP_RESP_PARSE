

class DistributedHashTable:
    def __init__(self):
        self.hash_table = {}

    def put(self, key, value):
        self.hash_table[key] = value

    def get(self, key):
        if key not in self.hash_table:
            return None
        return self.hash_table.get(key)

    def delete(self, key):
        self.hash_table.pop(key, None)

    def __str__(self):
        return str(self.hash_table)
