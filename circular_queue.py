class CircularQueue:
    INITIAL_CAPACITY = 9

    def __init__(self):
        """
        Construct an empty circular queue.

        Requirements:
        - backing_array has length INITIAL_CAPACITY
        - front stores the index of the first element
        - size stores the number of elements
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.front = 0
        self.back = 0
        self.size = 0
        
    def enqueue(self, data):
        """
        Add data to the back of the queue.

        Complexity:
            Amortized O(1)

        Requirements:
        - If the backing array is full, resize first
        - Use circular indexing to determine where the new
          element belongs

        Raise:
            ValueError if data is None
        """
        if data is None:
            raise ValueError("data invalid")

        if self.size == len(self.backing_array):
            self._resize()
        
        self.backing_array[self.back]  = data
        self.back = (self.back + 1) % len(self.backing_array)
        self.size += 1

    def dequeue(self):
        """
        Remove and return the element at the front.

        Complexity:
            O(1)

        Requirements:
        - Clear the removed position
        - Move front forward using circular indexing

        Raise:
            IndexError if the queue is empty
        """
        if self.size == 0:
            raise IndexError("empty")
        
        item = self.backing_array[self.front] 
        self.backing_array[self.front] = None
        self.front = (self.front + 1) % len(self.backing_array)
        self.size -= 1
        return item
        
    def peek(self):
        """
        Return the front element without removing it.

        Complexity:
            O(1)

        Raise:
            IndexError if the queue is empty
        """
        if self.size == 0:
            raise IndexError("invalid, queue is empty")
        return self.backing_array[self.front]
        

    def is_empty(self):
        """
        Return True if the queue is empty.

        Complexity:
            O(1)
        """
        return self.size == 0

    def get_size(self):
        """
        Return the number of elements currently stored.

        Complexity:
            O(1)
        """
        return self.size
        

    def clear(self):
        """
        Reset the queue.

        Requirements:
        - backing_array returns to INITIAL_CAPACITY
        - front resets appropriately
        - size becomes 0

        Complexity:
            O(1)
        """
        self.backing_array = [None] * self.INITIAL_CAPACITY
        self.front = 0
        self.back = 0
        self.size = 0
        

    def get_backing_array(self):
        """
        Return the backing array.

        Useful for testing the internal representation.
        """
        return self.backing_array

    def get_front_index(self):
        """
        Return the current front index.

        Useful for testing.
        """
        return self.front

    def _resize(self):
        """
        Double the capacity of the backing array.

        Important:
        Elements in a circular queue may currently look like:

            [40, 50, None, None, 10, 20, 30]
             ^                  ^
                               front

        When resizing, copy the elements into logical order:

            [10, 20, 30, 40, 50, None, None, ...]

        After resizing:
            front = 0

        Complexity:
            O(n)
        """
        new_array = [None] * (2 * len(self.backing_array))
        position = 0
        while position < self.size:
            new_array[position] = self.backing_array[(self.front + position) % len(self.backing_array)]
            position += 1
        
        self.backing_array = new_array
        self.front = 0
        self.back = position
    
def main():

    # ==================================================
    # TEST 1: INITIALIZATION
    # ==================================================

    queue = CircularQueue()

    assert queue.get_size() == 0
    assert queue.is_empty() is True
    assert queue.get_front_index() == 0
    assert len(queue.get_backing_array()) == 9

    print("Test 1 passed: initialization")

    
    # ==================================================
    # TEST 2: ENQUEUE
    # ==================================================

    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    
    assert queue.get_size() == 3
    assert queue.peek() == 10

    assert queue.get_backing_array()[0] == 10
    assert queue.get_backing_array()[1] == 20
    assert queue.get_backing_array()[2] == 30

    print("Test 2 passed: enqueue")

    
    # ==================================================
    # TEST 3: DEQUEUE
    # ==================================================

    removed = queue.dequeue()
    
    assert removed == 10
    assert queue.get_size() == 2
    assert queue.peek() == 20

    assert queue.get_front_index() == 1
    assert queue.get_backing_array()[0] is None

    print("Test 3 passed: dequeue")

    
    # ==================================================
    # TEST 4: FIFO ORDER
    # ==================================================

    queue = CircularQueue()

    for value in [10, 20, 30, 40, 50]:
        queue.enqueue(value)

    assert queue.dequeue() == 10
    assert queue.dequeue() == 20
    assert queue.dequeue() == 30
    assert queue.dequeue() == 40
    assert queue.dequeue() == 50

    assert queue.get_size() == 0
    assert queue.is_empty() is True

    print("Test 4 passed: FIFO ordering")

    
    # ==================================================
    # TEST 5: WRAPAROUND
    # ==================================================

    queue = CircularQueue()

    # Fill the entire backing array.
    for i in range(9):
        queue.enqueue(i)

    # Remove several elements from the front.
    assert queue.dequeue() == 0
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3

    assert queue.get_size() == 5
    assert queue.get_front_index() == 4

    # These should wrap around to indices 0, 1, 2, 3.
    queue.enqueue(9)
    queue.enqueue(10)
    queue.enqueue(11)
    queue.enqueue(12)

    assert queue.get_size() == 9

    # Logical queue should now be:
    #
    # 4, 5, 6, 7, 8, 9, 10, 11, 12

    expected = [4, 5, 6, 7, 8, 9, 10, 11, 12]

    for value in expected:
        assert queue.dequeue() == value

    print("Test 5 passed: wraparound")

    
    # ==================================================
    # TEST 6: INTERNAL WRAPAROUND STRUCTURE
    # ==================================================

    queue = CircularQueue()

    for i in range(9):
        queue.enqueue(i)

    for _ in range(4):
        queue.dequeue()

    queue.enqueue(9)
    queue.enqueue(10)
    queue.enqueue(11)
    queue.enqueue(12)

    backing = queue.get_backing_array()

    # Physical representation:
    #
    # index:  0   1   2   3   4  5  6  7  8
    #
    #        [9, 10, 11, 12, 4, 5, 6, 7, 8]
    #                     ^
    #                   front

    assert backing == [9, 10, 11, 12, 4, 5, 6, 7, 8]
    assert queue.get_front_index() == 4

    print("Test 6 passed: internal wraparound structure")

    
    # ==================================================
    # TEST 7: RESIZE WITHOUT WRAPAROUND
    # ==================================================

    queue = CircularQueue()

    for i in range(9):
        queue.enqueue(i)

    assert len(queue.get_backing_array()) == 9

    # Should trigger resize.
    queue.enqueue(9)

    assert queue.get_size() == 10
    assert len(queue.get_backing_array()) == 18 
    assert queue.get_front_index() == 0

    for i in range(10):
        assert queue.dequeue() == i

    print("Test 7 passed: normal resize")

    # ==================================================
    # TEST 8: RESIZE AFTER WRAPAROUND
    # ==================================================

    queue = CircularQueue()

    for i in range(9):
        queue.enqueue(i)

    # Remove:
    # 0, 1, 2, 3
    for i in range(4):
        assert queue.dequeue() == i

    # Queue currently:
    #
    # 4, 5, 6, 7, 8

    # Fill wrapped positions.
    for i in range(9, 13):
        queue.enqueue(i)

    # Queue is full again:
    #
    # 4,5,6,7,8,9,10,11,12

    # This triggers resize WHILE wrapped.
    queue.enqueue(13)

    assert len(queue.get_backing_array()) == 18
    assert queue.get_size() == 10

    # Your resize should normalize the queue.
    assert queue.get_front_index() == 0

    expected = [
        4, 5, 6, 7, 8,
        9, 10, 11, 12, 13
    ]

    for value in expected:
        assert queue.dequeue() == value

    print("Test 8 passed: wrapped resize")

    
    # ==================================================
    # TEST 9: MULTIPLE WRAPAROUNDS
    # ==================================================

    queue = CircularQueue()

    for i in range(6):
        queue.enqueue(i)

    for i in range(4):
        assert queue.dequeue() == i

    for i in range(6, 12):
        queue.enqueue(i)

    expected = list(range(4, 12))

    for value in expected:
        assert queue.dequeue() == value

    print("Test 9 passed: multiple wraparounds")
    
    
    # ==================================================
    # TEST 10: PEEK DOES NOT REMOVE
    # ==================================================

    queue = CircularQueue()

    queue.enqueue(10)
    queue.enqueue(20)

    assert queue.peek() == 10
    assert queue.peek() == 10
    assert queue.get_size() == 2

    print("Test 10 passed: peek")

    
    # ==================================================
    # TEST 11: NONE VALUES
    # ==================================================

    queue = CircularQueue()

    try:
        queue.enqueue(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    print("Test 11 passed: None rejected")


    # ==================================================
    # TEST 12: DEQUEUE EMPTY
    # ==================================================

    queue = CircularQueue()

    try:
        queue.dequeue()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 12 passed: empty dequeue")


    # ==================================================
    # TEST 13: PEEK EMPTY
    # ==================================================

    queue = CircularQueue()

    try:
        queue.peek()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 13 passed: empty peek")


    # ==================================================
    # TEST 14: SINGLE ELEMENT
    # ==================================================

    queue = CircularQueue()

    queue.enqueue(100)

    assert queue.peek() == 100
    assert queue.dequeue() == 100

    assert queue.get_size() == 0
    assert queue.is_empty() is True

    print("Test 14 passed: single element")


    # ==================================================
    # TEST 15: CLEAR
    # ==================================================

    queue = CircularQueue()

    for i in range(30):
        queue.enqueue(i)

    assert len(queue.get_backing_array()) > 9

    queue.clear()

    assert queue.get_size() == 0
    assert queue.is_empty() is True
    assert queue.get_front_index() == 0
    assert len(queue.get_backing_array()) == 9

    print("Test 15 passed: clear")


    # ==================================================
    # TEST 16: LARGE QUEUE
    # ==================================================

    queue = CircularQueue()

    for i in range(1000):
        queue.enqueue(i)

    assert queue.get_size() == 1000

    for i in range(1000):
        assert queue.dequeue() == i

    assert queue.is_empty()

    print("Test 16 passed: large queue")


    print()
    print("============================")
    print("ALL TESTS PASSED")
    print("============================")
    
if __name__ == "__main__":
    main()