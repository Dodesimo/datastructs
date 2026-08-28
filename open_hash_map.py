class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.is_deleted = False

class LinearProbingHashMap:
    INITIAL_CAPACITY = 9
    MAX_LOAD_FACTOR = 0.67

    def __init__(self):
        """
        Construct an empty hash map.

        Requirements:
        - backing_array has INITIAL_CAPACITY slots
        - each slot starts as None
        - size starts at 0
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY 
        self.size = 0

    def put(self, key, value):
        """
        Insert or update a key-value pair.

        Collision handling:
        - Use linear probing.
        - Starting index:

              hash(key) % capacity

        - Probe subsequent indices:

              (start + 1) % capacity
              (start + 2) % capacity
              ...

        Requirements:
        - If key already exists, update its value.
        - Updating an existing key does NOT increase size.
        - A deleted slot may be reused for insertion.
        - Before inserting a NEW key, resize if the resulting
          load factor would exceed MAX_LOAD_FACTOR.

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            ValueError if value is None
        """
        if key is None or value is None:
            raise ValueError("invalid data")
        
        if (self.size + 1) / len(self.backing_array) > self.MAX_LOAD_FACTOR:
            self._resize(2 * len(self.backing_array))

        position = hash(key) % len(self.backing_array)
        while True:
            if self.backing_array[position] is None or self.backing_array[position].is_deleted:
                break
            elif self.backing_array[position].key == key:
                self.backing_array[position].value = value
                return
            position = (position + 1) % len(self.backing_array)
        
        node = Entry(key, value)
        self.backing_array[position] = node
        self.size += 1
        return

    def get(self, key):
        """
        Return the value associated with key.

        Important:
        - A deleted entry does NOT end the search.
        - A None slot DOES end the search.

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            KeyError if key does not exist
        """
        if key is None:
            raise ValueError("invalid key")
        
        position = hash(key) % len(self.backing_array)
        while True:
            if self.backing_array[position] is None:
                raise KeyError("key doesn't exist")
            elif self.backing_array[position].key == key:
                return self.backing_array[position].value
            position = (position + 1) % len(self.backing_array)
        raise KeyError("key doesn't exist")

    def remove(self, key):
        """
        Remove key and return its value.

        IMPORTANT:
        Do NOT simply replace the entry with None.

        Instead, mark the entry as deleted.

        Why?
        Setting a deleted slot to None could break a probe chain.

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            KeyError if key does not exist
        """
        if key is None:
            raise ValueError("key is none")
        
        position = hash(key) % len(self.backing_array)
        while True:
            if self.backing_array[position] is None:
                raise KeyError("invalid key")
            if self.backing_array[position].key == key:
                self.backing_array[position].is_deleted = True
                self.size -= 1
                return self.backing_array[position].value
            position = (position + 1) % len(self.backing_array)
        raise KeyError("invalid key")

    def contains_key(self, key):
        """
        Return True if key exists.

        Complexity:
            Average: O(1)
            Worst case: O(n)
        """
        if key is None:
            raise ValueError("key is none")
        
        position = hash(key) % len(self.backing_array)
        while True:
            if self.backing_array[position] is None:
                return False
            if self.backing_array[position].key == key:
                return not self.backing_array[position].is_deleted
            position = (position + 1) % len(self.backing_array)
        return False

    def get_size(self):
        """
        Return the number of ACTIVE key-value pairs.

        Deleted entries should not count toward size.

        Complexity:
            O(1)
        """
        return self.size

    def is_empty(self):
        """
        Return True if no active entries exist.

        Complexity:
            O(1)
        """
        return self.size == 0

    def clear(self):
        """
        Reset the map.

        Requirements:
        - backing array returns to INITIAL_CAPACITY
        - all entries are removed
        - size becomes 0

        Complexity:
            O(1)
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.size = 0

    def get_backing_array(self):
        """
        Return the backing array.

        Useful for testing the internal representation.
        """
        return self.backing_array

    def _get_start_index(self, key):
        """
        Compute the initial probe index.

            hash(key) % len(backing_array)
        """
        return hash(key) % len(self.backing_array)

    def _resize(self, new_capacity):
        """
        Resize the hash map.

        Requirements:
        - Allocate a new backing array.
        - Rehash every ACTIVE entry.
        - Do not carry tombstones into the new table.
        - Preserve all active mappings.
        - size should remain logically unchanged.

        IMPORTANT:
        Entries cannot simply be copied to the same indices,
        because their probe sequences depend on capacity.

        Complexity:
            O(n)
        """
        new_backing_array = [None] * new_capacity
        for item in self.backing_array:
            if item is None or item.is_deleted:
                continue
            new_index = hash(item.key) % len(new_backing_array)
            while True:
                if new_backing_array[new_index] is None:
                    new_backing_array[new_index] = item
                    break
                new_index = (new_index + 1) % len(new_backing_array)
        self.backing_array = new_backing_array

def main():

    # ==================================================
    # TEST 1: INITIALIZATION
    # ==================================================

    table = LinearProbingHashMap()

    assert table.get_size() == 0
    assert table.is_empty() is True
    assert len(table.get_backing_array()) == 9

    for slot in table.get_backing_array():
        assert slot is None

    print("Test 1 passed: initialization")

    
    # ==================================================
    # TEST 2: BASIC PUT / GET
    # ==================================================

    table.put("a", 10)
    table.put("b", 20)
    table.put("c", 30)

    assert table.get_size() == 3    
    assert table.get("a") == 10
    assert table.get("b") == 20
    assert table.get("c") == 30

    print("Test 2 passed: basic put/get")

    
    # ==================================================
    # TEST 3: UPDATE EXISTING KEY
    # ==================================================

    table = LinearProbingHashMap()

    table.put("a", 10)

    assert table.get_size() == 1

    table.put("a", 100)

    assert table.get_size() == 1
    assert table.get("a") == 100

    print("Test 3 passed: update existing key")

    
    # ==================================================
    # COLLISION KEY FOR CONTROLLED TESTING
    # ==================================================

    class CollisionKey:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return 5

        def __eq__(self, other):
            return (
                isinstance(other, CollisionKey)
                and self.value == other.value
            )


    # ==================================================
    # TEST 4: LINEAR PROBING
    # ==================================================

    table = LinearProbingHashMap()

    k1 = CollisionKey("a")
    k2 = CollisionKey("b")
    k3 = CollisionKey("c")

    table.put(k1, 10)
    table.put(k2, 20)
    table.put(k3, 30)

    backing = table.get_backing_array()

    start = table._get_start_index(k1)
    
    assert backing[start].key == k1
    assert backing[(start + 1) % len(backing)].key == k2
    assert backing[(start + 2) % len(backing)].key == k3

    print("Test 4 passed: linear probing")

    
    # ==================================================
    # TEST 5: COLLISION GET
    # ==================================================

    assert table.get(k1) == 10
    assert table.get(k2) == 20
    assert table.get(k3) == 30

    print("Test 5 passed: get through probe chain")

    
    # ==================================================
    # TEST 6: REMOVE CREATES TOMBSTONE
    # ==================================================

    removed = table.remove(k2)

    assert removed == 20
    assert table.get_size() == 2
    assert table.contains_key(k2) is False

    deleted_slot = backing[(start + 1) % len(backing)]

    assert deleted_slot is not None
    assert deleted_slot.is_deleted is True

    print("Test 6 passed: tombstone created")

    
    # ==================================================
    # TEST 7: SEARCH PASSES TOMBSTONE
    # ==================================================

    # k3 was inserted AFTER k2 in the same probe chain.
    #
    # Search for k3 must continue past k2's deleted slot.

    assert table.get(k3) == 30

    print("Test 7 passed: search continues past tombstone")

    
    # ==================================================
    # TEST 8: TOMBSTONE REUSE
    # ==================================================

    k4 = CollisionKey("d")

    table.put(k4, 40)

    assert table.get(k4) == 40
    assert table.get_size() == 3

    # Ideally, the first tombstone in the probe sequence
    # should be reused.
    reused = table.get_backing_array()[
        (start + 1) % len(table.get_backing_array())
    ]

    assert reused.key == k4
    assert reused.is_deleted is False

    print("Test 8 passed: tombstone reused")

    
    # ==================================================
    # TEST 9: WRAPAROUND PROBING
    # ==================================================

    class EndCollisionKey:
        def __init__(self, value):
            self.value = value

        def __hash__(self):
            # With capacity 9, starts at index 8.
            return 8

        def __eq__(self, other):
            return (
                isinstance(other, EndCollisionKey)
                and self.value == other.value
            )

    table = LinearProbingHashMap()

    a = EndCollisionKey("a")
    b = EndCollisionKey("b")
    c = EndCollisionKey("c")

    table.put(a, 1)
    table.put(b, 2)
    table.put(c, 3)

    backing = table.get_backing_array()

    assert backing[8].key == a
    assert backing[0].key == b
    assert backing[1].key == c

    assert table.get(a) == 1
    assert table.get(b) == 2
    assert table.get(c) == 3

    print("Test 9 passed: wraparound probing")

    
    # ==================================================
    # TEST 10: REMOVE FIRST ITEM IN PROBE CHAIN
    # ==================================================

    table.remove(a)

    assert table.contains_key(a) is False

    # These must still remain reachable.
    assert table.get(b) == 2
    assert table.get(c) == 3

    print("Test 10 passed: remove first probe entry")

    
    # ==================================================
    # TEST 11: MISSING KEY
    # ==================================================

    table = LinearProbingHashMap()

    table.put("a", 10)

    try:
        table.get("missing")
        assert False, "Expected KeyError"
    except KeyError:
        pass

    try:
        table.remove("missing")
        assert False, "Expected KeyError"
    except KeyError:
        pass

    print("Test 11 passed: missing key")

    
    # ==================================================
    # TEST 12: NONE INPUT
    # ==================================================

    table = LinearProbingHashMap()

    try:
        table.put(None, 10)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        table.put("a", None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        table.get(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    print("Test 12 passed: None rejected")

    
    # ==================================================
    # TEST 13: RESIZE
    # ==================================================

    table = LinearProbingHashMap()

    original_capacity = len(table.get_backing_array())

    # capacity = 9
    #
    # 6 / 9 = 0.666...
    #
    # The 7th active entry should trigger resize.

    for i in range(6):
        table.put(i, i * 10)

    assert len(table.get_backing_array()) == original_capacity

    table.put(6, 60)

    assert len(table.get_backing_array()) > original_capacity
    assert table.get_size() == 7

    for i in range(7):
        assert table.get(i) == i * 10

    print("Test 13 passed: resize")

    
    # ==================================================
    # TEST 14: RESIZE REMOVES TOMBSTONES
    # ==================================================

    table = LinearProbingHashMap()

    for i in range(6):
        table.put(i, i)

    table.remove(1)
    table.remove(3)

    # Force enough new insertions to eventually resize.
    for i in range(6, 20):
        table.put(i, i)

    for slot in table.get_backing_array():
        if slot is not None:
            assert slot.is_deleted is False

    assert table.contains_key(1) is False
    assert table.contains_key(3) is False

    print("Test 14 passed: resize removes tombstones")

    
    # ==================================================
    # TEST 15: MANY COLLISIONS
    # ==================================================

    table = LinearProbingHashMap()

    keys = []

    for i in range(100):
        key = CollisionKey(i)
        keys.append(key)
        table.put(key, i)

    assert table.get_size() == 100

    for i in range(100):
        assert table.get(keys[i]) == i

    print("Test 15 passed: many collisions")

    
    # ==================================================
    # TEST 16: REMOVE MANY COLLIDING ENTRIES
    # ==================================================

    for i in range(0, 100, 2):
        assert table.remove(keys[i]) == i

    assert table.get_size() == 50

    for i in range(1, 100, 2):
        assert table.get(keys[i]) == i

    print("Test 16 passed: remove many collisions")

    
    # ==================================================
    # TEST 17: CONTAINS KEY
    # ==================================================

    table = LinearProbingHashMap()

    table.put("apple", 1)

    assert table.contains_key("apple") is True
    assert table.contains_key("banana") is False

    table.remove("apple")

    assert table.contains_key("apple") is False

    print("Test 17 passed: contains_key")

    
    # ==================================================
    # TEST 18: CLEAR
    # ==================================================

    table = LinearProbingHashMap()

    for i in range(100):
        table.put(i, i)

    assert len(table.get_backing_array()) > 9

    table.clear()

    assert table.get_size() == 0
    assert table.is_empty() is True
    assert (
        len(table.get_backing_array())
        == LinearProbingHashMap.INITIAL_CAPACITY
    )

    for slot in table.get_backing_array():
        assert slot is None

    print("Test 18 passed: clear")


    print()
    print("============================")
    print("ALL TESTS PASSED")
    print("============================")

if __name__ == "__main__":
    main()