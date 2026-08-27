class Node:
    def __init__(self, key, value):
        """
        Node stored inside a bucket's linked list.

        Each entry stores:
        - key
        - value
        - next entry in the chain
        """
        self.key = key
        self.value = value
        self.next = None


class ClosedAddressHashMap:
    INITIAL_CAPACITY = 9
    MAX_LOAD_FACTOR = 0.67

    def __init__(self):
        """
        Construct an empty hash map.

        Requirements:
        - backing_array has INITIAL_CAPACITY buckets
        - each bucket starts as None
        - size starts at 0
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.size = 0

    def put(self, key, value):
        """
        Insert or update a key-value pair.

        Behavior:
        - If key already exists, replace its value.
        - If key does not exist, insert a new Entry.
        - New entries should be stored in the appropriate bucket.
        - Handle collisions using separate chaining.

        Resizing:
        - Before inserting a NEW key, determine whether the
          resulting load factor would exceed MAX_LOAD_FACTOR.
        - If so, resize first.

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            ValueError if value is None
        """
        if key is None or value is None:
            raise ValueError("invalid data")
        
        new_load_factor = (self.size + 1) / len(self.backing_array) # number of elements divided by the number of buckets
        if new_load_factor >= self.MAX_LOAD_FACTOR:
            self._resize(2 * len(self.backing_array))
        
        node = Node(key, value)
        bucket = hash(key) % len(self.backing_array)

        if not self.backing_array[bucket]:
            self.backing_array[bucket] = node
            self.size += 1
            return

        previous = None
        curr = self.backing_array[bucket]
        while curr:
            if curr.key == key:
                curr.value = value
                return
            previous = curr
            curr = curr.next
        
        # not found, so add it to the linked list for that
        previous.next = node
        self.size += 1
        return


    def get(self, key):
        """
        Return the value associated with key.

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            KeyError if key does not exist
        """
        if key is None:
            raise ValueError("not found")

        bucket = hash(key) % len(self.backing_array)
        curr = self.backing_array[bucket]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next

        raise KeyError("key doesn't exist")

    def remove(self, key):
        """
        Remove the entry associated with key and return its value.

        You must correctly handle:
        - removing the first node of a chain
        - removing from the middle
        - removing the final node

        Complexity:
            Average: O(1)
            Worst case: O(n)

        Raise:
            ValueError if key is None
            KeyError if key does not exist
        """
        if key is None:
            raise ValueError("invalid key")
        
        bucket = self.backing_array[hash(key) % len(self.backing_array)]
        if not bucket:
            raise KeyError("not found")
        elif bucket.key == key:
            item = bucket.value
            self.backing_array[hash(key) % len(self.backing_array)] = bucket.next
            self.size -= 1
            return item
        else:
            prev = None
            curr = bucket
            found = False
            item = None
            while curr:
                if curr.key == key:
                    item = curr.value
                    found = True
                    break
                prev = curr
                curr = curr.next
            if not found:
                raise KeyError("not found")
            if not curr:
                # means last element is the item
                prev.next = None
            else:
                prev.next = curr.next
            self.size -= 1
            return item

    def contains_key(self, key):
        """
        Return True if key exists in the map.

        Complexity:
            Average: O(1)
            Worst case: O(n)
        """
        if key is None:
            raise ValueError("not found")

        bucket = hash(key) % len(self.backing_array)
        curr = self.backing_array[bucket]
        while curr:
            if curr.key == key:
                return True
            curr = curr.next

        return False

    def get_size(self):
        """
        Return the number of key-value pairs.

        Complexity:
            O(1)
        """
        return self.size

    def is_empty(self):
        """
        Return True if the map contains no entries.

        Complexity:
            O(1)
        """
        return self.size == 0

    def clear(self):
        """
        Reset the map.

        Requirements:
        - backing array returns to INITIAL_CAPACITY
        - size becomes 0

        Complexity:
            O(1)
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.size = 0

    def get_backing_array(self):
        """
        Return the backing array.

        Mainly useful for testing the internal structure.
        """
        return self.backing_array

    def _get_index(self, key):
        """
        Compute the bucket index for key.

        Use Python's hash(key), then map it into the valid
        range of the backing array.

        Complexity:
            O(1), assuming hashing the key is O(1)
        """
        return hash(key) % len(self.backing_array)

    def _resize(self, new_capacity):
        """
        Resize the hash map.

        Requirements:
        - Allocate a new backing array.
        - Reinsert / rehash every existing entry.
        - Preserve all key-value mappings.
        - size should remain logically unchanged.

        IMPORTANT:
        You cannot simply copy buckets to the same indices.

        Why?
        The bucket index depends on capacity:

            hash(key) % capacity

        Changing capacity can therefore change every key's bucket.

        Complexity:
            O(n)
        """
        '''
        for this don't try to iterate through every single new backing array's node list because that's o(n^2)
        make insertions o(1) by always adding to the head
        '''
        new_backing_array = [None] * (new_capacity)
        for bucket in self.backing_array:
            if not bucket:
                continue
            while bucket:
                nextNode = bucket.next
                newIndex = hash(bucket.key) % len(new_backing_array)
                bucket.next = new_backing_array[newIndex]
                new_backing_array[newIndex] = bucket
                bucket = nextNode
        self.backing_array = new_backing_array

def main():

    # ==================================================
    # TEST 1: INITIALIZATION
    # ==================================================

    table = ClosedAddressHashMap()

    assert table.get_size() == 0
    assert table.is_empty() is True
    assert len(table.get_backing_array()) == 9

    for bucket in table.get_backing_array():
        assert bucket is None

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

    assert table.is_empty() is False

    print("Test 2 passed: put/get")

    
    # ==================================================
    # TEST 3: UPDATE EXISTING KEY
    # ==================================================

    table = ClosedAddressHashMap()

    table.put("a", 10)

    assert table.get_size() == 1

    table.put("a", 100)

    assert table.get_size() == 1
    assert table.get("a") == 100

    print("Test 3 passed: update existing key")

    
    # ==================================================
    # TEST 4: CONTAINS KEY
    # ==================================================

    table = ClosedAddressHashMap()

    table.put("apple", 1)
    table.put("banana", 2)

    assert table.contains_key("apple") is True
    assert table.contains_key("banana") is True
    assert table.contains_key("orange") is False

    print("Test 4 passed: contains_key")

    
    # ==================================================
    # TEST 5: COLLISIONS
    # ==================================================

    class CollisionKey:
        """
        Every instance deliberately has the same hash value.

        This forces collisions so we can test chaining.
        """

        def __init__(self, value):
            self.value = value

        def __hash__(self):
            return 42

        def __eq__(self, other):
            return (
                isinstance(other, CollisionKey)
                and self.value == other.value
            )

    table = ClosedAddressHashMap()

    k1 = CollisionKey("a")
    k2 = CollisionKey("b")
    k3 = CollisionKey("c")

    table.put(k1, 10)
    table.put(k2, 20)
    table.put(k3, 30)

    assert table.get_size() == 3

    assert table.get(k1) == 10
    assert table.get(k2) == 20
    assert table.get(k3) == 30

    print("Test 5 passed: collision handling")

    
    # ==================================================
    # TEST 6: COLLISION CHAIN STRUCTURE
    # ==================================================

    index = table._get_index(k1)
    node = table.get_backing_array()[index]

    keys = []

    while node is not None:
        keys.append(node.key)
        node = node.next

    assert len(keys) == 3
    assert k1 in keys
    assert k2 in keys
    assert k3 in keys

    print("Test 6 passed: chain structure")

    
    # ==================================================
    # TEST 7: REMOVE BASIC
    # ==================================================

    table = ClosedAddressHashMap()

    table.put("a", 10)
    table.put("b", 20)
    table.put("c", 30)

    removed = table.remove("b")

    assert removed == 20
    assert table.get_size() == 2

    assert table.contains_key("b") is False
    assert table.get("a") == 10
    assert table.get("c") == 30

    print("Test 7 passed: remove")

    
    # ==================================================
    # TEST 8: REMOVE FROM COLLISION CHAIN
    # ==================================================

    table = ClosedAddressHashMap()

    k1 = CollisionKey("a")
    k2 = CollisionKey("b")
    k3 = CollisionKey("c")

    table.put(k1, 10)
    table.put(k2, 20)
    table.put(k3, 30)

    assert table.remove(k2) == 20

    assert table.get_size() == 2

    assert table.get(k1) == 10
    assert table.get(k3) == 30
    assert table.contains_key(k2) is False

    print("Test 8 passed: remove from collision chain")

    
    # ==================================================
    # TEST 9: REMOVE ALL COLLIDING ELEMENTS
    # ==================================================

    table = ClosedAddressHashMap()

    k1 = CollisionKey("a")
    k2 = CollisionKey("b")
    k3 = CollisionKey("c")

    table.put(k1, 10)
    table.put(k2, 20)
    table.put(k3, 30)

    table.remove(k1)
    table.remove(k2)
    table.remove(k3)

    assert table.get_size() == 0
    assert table.is_empty() is True

    index = table._get_index(k1)

    assert table.get_backing_array()[index] is None

    print("Test 9 passed: remove entire chain")

    
    # ==================================================
    # TEST 10: MISSING KEY
    # ==================================================

    table = ClosedAddressHashMap()

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

    print("Test 10 passed: missing key")

    
    # ==================================================
    # TEST 11: NONE INPUT
    # ==================================================

    table = ClosedAddressHashMap()

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

    print("Test 11 passed: None rejected")

    
    # ==================================================
    # TEST 12: RESIZE
    # ==================================================

    table = ClosedAddressHashMap()

    original_capacity = len(table.get_backing_array())

    # At capacity 9 and load factor 0.67:
    #
    # 6 / 9 = 0.666...
    #
    # Adding the 7th entry should cause a resize.

    for i in range(6):
        table.put(i, i * 10)

    assert len(table.get_backing_array()) == original_capacity

    table.put(6, 60)
    
    assert len(table.get_backing_array()) > original_capacity
    
    assert table.get_size() == 7

    for i in range(7):
        assert table.get(i) == i * 10

    print("Test 12 passed: resize")

    
    # ==================================================
    # TEST 13: REHASHING
    # ==================================================

    table = ClosedAddressHashMap()

    for i in range(100):
        table.put(i, i * 2)

    assert table.get_size() == 100

    for i in range(100):
        assert table.get(i) == i * 2

    print("Test 13 passed: rehashing")

    
    # ==================================================
    # TEST 14: MANY COLLISIONS
    # ==================================================

    table = ClosedAddressHashMap()

    keys = []

    for i in range(100):
        key = CollisionKey(i)
        keys.append(key)
        table.put(key, i)

    assert table.get_size() == 100

    for i in range(100):
        assert table.get(keys[i]) == i

    print("Test 14 passed: many collisions")

    
    # ==================================================
    # TEST 15: CLEAR
    # ==================================================

    table = ClosedAddressHashMap()

    for i in range(100):
        table.put(i, i)

    assert len(table.get_backing_array()) > 9

    table.clear()

    assert table.get_size() == 0
    assert table.is_empty() is True

    assert (
        len(table.get_backing_array())
        == ClosedAddressHashMap.INITIAL_CAPACITY
    )

    for bucket in table.get_backing_array():
        assert bucket is None

    print("Test 15 passed: clear")


    print()
    print("============================")
    print("ALL TESTS PASSED")
    print("============================")
    

if __name__ == "__main__":
    main()