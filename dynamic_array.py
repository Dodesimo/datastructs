class DynamicArray:
    INITIAL_CAPACITY = 9

    def __init__(self):
        """
        Construct an empty DynamicArray.

        Requirements:
        - backing_array should have length INITIAL_CAPACITY
        - size should start at 0
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.size = 0
        

    def add_at_index(self, index, data):
        """
        Add data at the specified index.

        Valid indices:
            0 <= index <= size

        Elements at index and after must shift right.

        Complexity:
            - Amortized O(1) when index == size
            - O(n) otherwise

        Raise:
            IndexError if index < 0 or index > size
            ValueError if data is None
        """
        if index < 0 or index > self.size:
            raise IndexError("out of bounds access")
        if data is None:
            raise ValueError("data is none")

        if self.size == len(self.backing_array):
            self._resize()
        
        for i in range(self.size - 1, index - 1, -1):
            self.backing_array[i + 1] = self.backing_array[i]

        self.backing_array[index] = data
        self.size += 1
        
        
    def add_to_front(self, data):
        """
        Add data to the front of the array.

        Complexity:
            O(n)

        Raise:
            ValueError if data is None
        """
        self.add_at_index(0, data)

    def add_to_back(self, data):
        """
        Add data to the back of the array.

        Complexity:
            Amortized O(1)

        Raise:
            ValueError if data is None
        """
        self.add_at_index(self.size, data)

    def remove_at_index(self, index):
        """
        Remove and return the element at index.

        Elements after index must shift left.

        Complexity:
            - O(1) when removing index size - 1
            - O(n) otherwise

        Raise:
            IndexError if index < 0 or index >= size
        """
        if index < 0 or index >= self.size:
            raise IndexError("can't remove from index if its out of bounds")
        
        '''
        suppose we want to remove at a particular index
        copy over all items to the right of it to the previous value
        and then set the last value to None
        '''
        item = self.backing_array[index]
        for i in range(index + 1, self.size):
            self.backing_array[i - 1] = self.backing_array[i]
        self.backing_array[self.size - 1] = None
        self.size -= 1
        return item


    def remove_from_front(self):
        """
        Remove and return the first element.

        Complexity:
            O(n)

        Raise:
            IndexError if the array is empty
        """
        return self.remove_at_index(0)


    def remove_from_back(self):
        """
        Remove and return the final element.

        Complexity:
            O(1)

        Raise:
            IndexError if the array is empty
        """
        if self.size == 0:
            raise IndexError("can't remove from the back of an empty array")
        
        item = self.backing_array[self.size - 1]
        self.backing_array[self.size - 1] = None
        self.size -= 1
        return item

    def get(self, index):
        """
        Return the element at index.

        Complexity:
            O(1)

        Raise:
            IndexError if index < 0 or index >= size
        """
        if index < 0 or index >= self.size:
            raise IndexError("out of bounds access")
        return self.backing_array[index]

    def is_empty(self):
        """
        Return True if the array is empty.

        Complexity:
            O(1)
        """
        return self.size == 0

    def clear(self):
        """
        Clear the array.

        Requirements:
        - size becomes 0
        - backing_array is reset to INITIAL_CAPACITY

        Complexity:
            O(1)
        """
        self.size = 0
        self.backing_array = [None] * self.INITIAL_CAPACITY

    def get_backing_array(self):
        """
        Return the underlying backing array.

        Mainly useful for testing your implementation.
        """
        return self.backing_array

    def sizeOf(self):
        """
        Return the number of elements currently stored.

        Complexity:
            O(1)
        """
        return self.size

    def _resize(self):
        """
        Resize the backing array when it is full.

        Requirements:
        - Allocate a NEW backing array
        - New capacity should be 2 * old capacity
        - Copy existing elements into it
        - Replace the old backing array

        Do NOT use Python list append/extend to accomplish
        the resizing itself.
        """
        '''
        capacity is the largest possible size of the backing array
        size is the actual number of elements
        '''
        newBackingArray = [None] * (2 * len(self.backing_array))
        for i in range(len(self.backing_array)):
            newBackingArray[i] = self.backing_array[i]
        self.backing_array = newBackingArray


def main():

    # ==================================================
    # TEST 1: INITIALIZATION
    # ==================================================

    arr = DynamicArray()
    arr = DynamicArray()
    
    assert arr.sizeOf() == 0
    assert arr.is_empty() is True
    assert len(arr.get_backing_array()) == 9

    print("Test 1 passed: initialization")

    
    # ==================================================
    # TEST 2: ADD TO BACK
    # ==================================================

    arr.add_to_back(10)
    arr.add_to_back(20)
    arr.add_to_back(30)

    assert arr.sizeOf() == 3
    assert arr.get(0) == 10
    assert arr.get(1) == 20
    assert arr.get(2) == 30
    assert arr.is_empty() is False

    print("Test 2 passed: add_to_back")

    
    # ==================================================
    # TEST 3: ADD TO FRONT
    # ==================================================

    arr = DynamicArray()

    arr.add_to_front(30)
    arr.add_to_front(20)
    arr.add_to_front(10)

    assert arr.sizeOf() == 3
    assert arr.get(0) == 10
    assert arr.get(1) == 20
    assert arr.get(2) == 30

    print("Test 3 passed: add_to_front")

    
    # ==================================================
    # TEST 4: ADD AT INDEX
    # ==================================================

    arr = DynamicArray()

    arr.add_to_back(10)
    arr.add_to_back(30)
    arr.add_to_back(40)

    arr.add_at_index(1, 20)

    assert arr.sizeOf() == 4

    assert arr.get(0) == 10
    assert arr.get(1) == 20
    assert arr.get(2) == 30
    assert arr.get(3) == 40

    print("Test 4 passed: add_at_index")

    
    # ==================================================
    # TEST 5: ADD AT SIZE
    # ==================================================

    arr.add_at_index(arr.sizeOf(), 50)

    assert arr.sizeOf() == 5
    assert arr.get(4) == 50

    print("Test 5 passed: add_at_index at size")

    
    # ==================================================
    # TEST 6: RESIZING
    # ==================================================

    arr = DynamicArray()

    for i in range(9):
        arr.add_to_back(i)

    assert arr.sizeOf() == 9
    assert len(arr.get_backing_array()) == 9

    # This should trigger resizing.
    arr.add_to_back(9)

    assert arr.sizeOf() == 10
    assert len(arr.get_backing_array()) == 18

    for i in range(10):
        assert arr.get(i) == i

    print("Test 6 passed: resize")

    
    # ==================================================
    # TEST 7: MULTIPLE RESIZES
    # ==================================================

    arr = DynamicArray()

    for i in range(100):
        arr.add_to_back(i)

    assert arr.sizeOf() == 100
    assert len(arr.get_backing_array()) >= 100

    for i in range(100):
        assert arr.get(i) == i

    print("Test 7 passed: multiple resizes")

    
    # ==================================================
    # TEST 8: REMOVE AT INDEX
    # ==================================================

    arr = DynamicArray()

    for value in [10, 20, 30, 40, 50]:
        arr.add_to_back(value)

    removed = arr.remove_at_index(2)

    assert removed == 30
    assert arr.sizeOf() == 4

    assert arr.get(0) == 10
    assert arr.get(1) == 20
    assert arr.get(2) == 40
    assert arr.get(3) == 50

    # Make sure the unused position was cleared.
    assert arr.get_backing_array()[4] is None

    print("Test 8 passed: remove_at_index")

    
    # ==================================================
    # TEST 9: REMOVE FROM FRONT
    # ==================================================

    arr = DynamicArray()

    for value in [10, 20, 30]:
        arr.add_to_back(value)

    removed = arr.remove_from_front()

    assert removed == 10
    assert arr.sizeOf() == 2
    assert arr.get(0) == 20
    assert arr.get(1) == 30

    print("Test 9 passed: remove_from_front")

    
    # ==================================================
    # TEST 10: REMOVE FROM BACK
    # ==================================================

    arr = DynamicArray()

    for value in [10, 20, 30]:
        arr.add_to_back(value)

    removed = arr.remove_from_back()

    assert removed == 30
    assert arr.sizeOf() == 2
    assert arr.get(0) == 10
    assert arr.get(1) == 20

    assert arr.get_backing_array()[2] is None

    print("Test 10 passed: remove_from_back")

    
    # ==================================================
    # TEST 11: INVALID GET
    # ==================================================

    arr = DynamicArray()
    arr.add_to_back(10)

    try:
        arr.get(-1)
        assert False, "Expected IndexError for negative index"
    except IndexError:
        pass

    try:
        arr.get(1)
        assert False, "Expected IndexError for index == size"
    except IndexError:
        pass

    print("Test 11 passed: invalid get")

   
    # ==================================================
    # TEST 12: INVALID ADD INDEX
    # ==================================================

    arr = DynamicArray()

    try:
        arr.add_at_index(-1, 10)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    try:
        arr.add_at_index(1, 10)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 12 passed: invalid add index")

    
    # ==================================================
    # TEST 13: NONE VALUES
    # ==================================================

    arr = DynamicArray()

    try:
        arr.add_to_back(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        arr.add_to_front(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        arr.add_at_index(0, None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    print("Test 13 passed: None rejected")

    
    # ==================================================
    # TEST 14: REMOVE FROM EMPTY ARRAY
    # ==================================================

    arr = DynamicArray()

    try:
        arr.remove_from_front()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    try:
        arr.remove_from_back()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 14 passed: remove from empty")

    
    # ==================================================
    # TEST 15: CLEAR
    # ==================================================

    arr = DynamicArray()

    for i in range(50):
        arr.add_to_back(i)

    # Ensure capacity had actually grown.
    assert len(arr.get_backing_array()) > DynamicArray.INITIAL_CAPACITY

    arr.clear()

    assert arr.sizeOf() == 0
    assert arr.is_empty() is True
    assert len(arr.get_backing_array()) == DynamicArray.INITIAL_CAPACITY

    print("Test 15 passed: clear")

    
    # ==================================================
    # TEST 16: BACKING ARRAY STRUCTURE
    # ==================================================

    arr = DynamicArray()

    arr.add_to_back(10)
    arr.add_to_back(20)
    arr.add_to_back(30)

    backing = arr.get_backing_array()

    assert backing[0] == 10
    assert backing[1] == 20
    assert backing[2] == 30

    for i in range(3, len(backing)):
        assert backing[i] is None

    print("Test 16 passed: backing array structure")

    print()
    print("============================")
    print("ALL TESTS PASSED")
    print("============================")

if __name__ == "__main__":
    main()