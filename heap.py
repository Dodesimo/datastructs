class MinHeap:
    def __init__(self):
        """
        Construct an empty binary min heap.

        Fields:
        - heap: array storing heap elements
        - size: number of elements currently stored

        Heap invariant:
        - Every parent is <= each of its children.

        Array relationships for index i:

            parent = (i - 1) // 2
            left   = 2 * i + 1
            right  = 2 * i + 2

        Complexity:
            O(1)
        """
        self.heap = [None]
        self.size = 0

    # ============================================================
    # Basic helpers
    # ============================================================

    def _parent(self, index):
        """
        Return the parent index of index.

        Formula:

            parent = (index) // 2

        Requirements:
        - Assume index > 0.

        Complexity:
            O(1)
        """
        return index // 2

    def _left_child(self, index):
        """
        Return the left child index.

        Formula:

            left = 2 * index

        Note:
        - The returned index may be outside the heap.
        - This method only calculates the index.

        Complexity:
            O(1)
        """
        return index * 2

    def _right_child(self, index):
        """
        Return the right child index.

        Formula:

            right = 2 * index + 1

        Note:
        - The returned index may be outside the heap.
        - This method only calculates the index.

        Complexity:
            O(1)
        """
        return index * 2 + 1

    # ============================================================
    # Sifting
    # ============================================================

    def _sift_up(self, index):
        """
        Restore the min-heap invariant by moving the element
        at index upward.

        Suggested flow:

        1. While index is not the root:
        2. Find its parent.
        3. If:

               heap[parent] <= heap[index]

           the heap invariant already holds, so stop.

        4. Otherwise:
           - swap parent and child
           - continue from the parent's old index

        Example:

                2
               / \
              5   7
             /
            1

        becomes:

                1
               / \
              2   7
             /
            5

        Complexity:
            O(log n)
        """
        '''
        the parent needs to be smaller than this
        '''
        while index > 1:
            if self.heap[self._parent(index)] <= self.heap[index]:
                break
            newIndex = self._parent(index)
            self.heap[self._parent(index)], self.heap[index] = self.heap[index], self.heap[self._parent(index)]
            index = newIndex

    def _sift_down(self, index):
        """
        Restore the min-heap invariant by moving the element
        at index downward.

        Suggested flow:

        1. Find the left and right child indices.
        2. Determine the smallest value among:
             - current node
             - left child, if it exists
             - right child, if it exists
        3. If current node is already smallest:
             stop.
        4. Otherwise:
             swap current node with the smaller child.
        5. Continue from the child's old index.

        Important:

        Always swap with the SMALLER child.

        Example:

                8
               / \
              3   5

        must become:

                3
               / \
              8   5

        not:

                5
               / \
              3   8

        Complexity:
            O(log n)
        """
        while index < len(self.heap):
            leftChild = self._left_child(index)
            rightChild = self._right_child(index)
            if leftChild < len(self.heap) and rightChild < len(self.heap):
                if self.heap[index] <= self.heap[leftChild] and self.heap[index] <= self.heap[rightChild]:
                    break
                elif self.heap[leftChild] <= self.heap[rightChild]:
                    # the left child is the smallest, so we want it to move to the top
                    self.heap[leftChild], self.heap[index] = self.heap[index], self.heap[leftChild]
                    index = leftChild
                elif self.heap[rightChild] <= self.heap[leftChild]:
                    # same principle as above
                    self.heap[rightChild], self.heap[index] = self.heap[index], self.heap[rightChild]
                    index = rightChild
            elif leftChild < len(self.heap):
                # only left child is in bounds
                if self.heap[index] <= self.heap[leftChild]:
                    break
                else:
                    # swap w/ left
                    self.heap[leftChild], self.heap[index] = self.heap[index], self.heap[leftChild]
                    index = leftChild
            elif rightChild < len(self.heap):
                if self.heap[index] <= self.heap[rightChild]:
                    break
                else:
                    self.heap[rightChild], self.heap[index] = self.heap[index], self.heap[rightChild]
                    index = rightChild
            else:
                break

    # ============================================================
    # Insertion
    # ============================================================

    def push(self, value):
        """
        Insert value into the heap.

        Requirements:
        - Add value to the end of the backing array.
        - Increase size by 1.
        - Restore the min-heap invariant using sift-up.

        Suggested flow:

        1. Append value.
        2. Increase size.
        3. Sift upward from the final index.

        Complexity:
            O(log n)
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)
        self.size += 1

    # ============================================================
    # Minimum
    # ============================================================

    def peek(self):
        """
        Return the minimum value without removing it.

        Raise:
            IndexError if the heap is empty.

        Complexity:
            O(1)
        """
        if self.size == 0:
            raise IndexError("empty heap")
        return self.heap[1]

    # ============================================================
    # Removal
    # ============================================================

    def pop(self):
        """
        Remove and return the minimum value.

        Raise:
            IndexError if the heap is empty.

        Requirements:
        - Save the root value.
        - Move the final element to the root.
        - Remove the final array element.
        - Decrease size by exactly 1.
        - Restore the min-heap invariant using sift-down.
        - Correctly handle the single-element case.

        Suggested flow:

        1. Save heap[0].
        2. Swap or move the last element into index 0.
        3. Remove the final element.
        4. Decrease size.
        5. If the heap is not empty:
             sift down from index 0.
        6. Return the saved minimum.

        Complexity:
            O(log n)
        """
        value = self.heap[1]
        self.heap[1], self.heap[-1] = self.heap[-1], self.heap[1]
        self.heap.pop()
        self.size -= 1
        if self.size > 0:
            self._sift_down(1)
        return value

    # ============================================================
    # Heap construction
    # ============================================================

    def heapify(self, values):
        """
        Replace the current heap with values and transform
        them into a valid min heap.

        Requirements:
        - Copy values into the heap.
        - Do NOT repeatedly call push().
        - Set size correctly.
        - Perform bottom-up heap construction.
        - Start from the last non-leaf node and sift downward
          toward the root.

        Last non-leaf index:

            size // 2 - 1

        Suggested flow:

        1. Copy values.
        2. Set size.
        3. Starting at:

               size // 2 - 1

           iterate backward through index 0.

        4. Call sift-down at each index.

        Complexity:
            O(n)
        """
        self.heap = [None]
        self.heap.extend(values)
        self.size = len(values)
        index = self.size // 2 # this is the last nonleaf nodes 
        while index >= 1:
            self._sift_down(index)
            index -= 1

    # ============================================================
    # Miscellaneous
    # ============================================================

    def size_of(self):
        """
        Return number of elements in the heap.

        Complexity:
            O(1)
        """
        return self.size

    def is_empty(self):
        """
        Return True if the heap is empty.

        Complexity:
            O(1)
        """
        return self.size == 0

    # ============================================================
    # Validation
    # ============================================================

    def is_valid_heap(self):
        """
        Return True if the min-heap invariant holds.

        For every index i:

            heap[i] <= heap[left child]
            heap[i] <= heap[right child]

        whenever those children exist.

        Complexity:
            O(n)
        """
        for i in range(1, len(self.heap) // 2):
            leftChild = i * 2 
            rightChild = i * 2 + 1
            if leftChild < len(self.heap) and self.heap[i] > self.heap[leftChild]:
                return False
            if rightChild < len(self.heap) and self.heap[i] > self.heap[rightChild]:
                return False
        return True

# ================================================================
# Tests
# ================================================================

if __name__ == "__main__":
    heap = MinHeap()

    # ------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------

    assert heap.heap == [None]
    assert heap.size_of() == 0
    assert heap.is_empty()
    assert heap.is_valid_heap()

    print("Initialization tests passed")
    
    # ------------------------------------------------------------
    # Index helpers
    # ------------------------------------------------------------

    assert heap._parent(2) == 1
    assert heap._parent(3) == 1
    assert heap._parent(4) == 2
    assert heap._parent(5) == 2
    assert heap._parent(6) == 3

    assert heap._left_child(1) == 2
    assert heap._left_child(2) == 4
    assert heap._left_child(3) == 6

    assert heap._right_child(1) == 3
    assert heap._right_child(2) == 5
    assert heap._right_child(3) == 7

    print("Index helper tests passed")
    
    # ------------------------------------------------------------
    # Single insertion
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(10)

    assert heap.heap == [None, 10]
    assert heap.peek() == 10
    assert heap.size_of() == 1
    assert not heap.is_empty()
    assert heap.is_valid_heap()

    print("Single insertion tests passed")
    
    # ------------------------------------------------------------
    # Basic insertion
    #
    #        5                2
    #       /       ->       /
    #      2                5
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(5)
    heap.push(2)

    assert heap.heap == [None, 2, 5]
    assert heap.peek() == 2
    assert heap.size_of() == 2
    assert heap.is_valid_heap()

    print("Basic insertion tests passed")
    
    # ------------------------------------------------------------
    # Multiple sift-up
    #
    # Insert:
    #
    #     10, 8, 7, 3, 1
    #
    # Final root should be 1.
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [10, 8, 7, 3, 1]

    for value in values:
        heap.push(value)

    assert heap.peek() == 1
    assert heap.heap[1] == 1
    assert heap.size_of() == 5
    assert heap.is_valid_heap()

    print("Sift-up tests passed")
    
    # ------------------------------------------------------------
    # Duplicate values
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(3)
    heap.push(3)
    heap.push(3)

    assert heap.heap == [None, 3, 3, 3]
    assert heap.peek() == 3
    assert heap.size_of() == 3
    assert heap.is_valid_heap()

    print("Duplicate insertion tests passed")
    
    # ------------------------------------------------------------
    # Negative values
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [5, -2, 8, -10, 0]

    for value in values:
        heap.push(value)

    assert heap.peek() == -10
    assert heap.heap[1] == -10
    assert heap.size_of() == 5
    assert heap.is_valid_heap()

    print("Negative value tests passed")
    
    # ------------------------------------------------------------
    # Peek does not remove
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(4)
    heap.push(2)
    heap.push(7)

    old_size = heap.size_of()

    assert heap.peek() == 2
    assert heap.peek() == 2
    assert heap.size_of() == old_size

    print("Peek tests passed")
    
    # ------------------------------------------------------------
    # Peek on empty heap
    # ------------------------------------------------------------

    heap = MinHeap()

    try:
        heap.peek()
        assert False
    except IndexError:
        pass

    print("Empty peek tests passed")
    
    # ------------------------------------------------------------
    # Pop single element
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(5)

    removed = heap.pop()

    assert removed == 5
    assert heap.heap == [None]
    assert heap.size_of() == 0
    assert heap.is_empty()
    assert heap.is_valid_heap()

    print("Single pop tests passed")
    
    # ------------------------------------------------------------
    # Basic pop
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [5, 3, 8, 1, 4]

    for value in values:
        heap.push(value)

    removed = heap.pop()

    assert removed == 1
    assert heap.peek() == 3
    assert heap.heap[1] == 3
    assert heap.size_of() == 4
    assert heap.is_valid_heap()

    print("Basic pop tests passed")
    
    # ------------------------------------------------------------
    # Sift-down chooses smaller child
    #
    #          8
    #         / \
    #        3   5
    #
    # represented as:
    #
    #     [None, 8, 3, 5]
    #
    # It must swap with 3, not 5.
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.heap = [None, 8, 3, 5]
    heap.size = 3

    heap._sift_down(1)

    assert heap.heap == [None, 3, 8, 5]
    assert heap.is_valid_heap()

    print("Smaller child sift-down tests passed")
    
    # ------------------------------------------------------------
    # Left child only
    #
    #          8
    #         /
    #        3
    #
    # Useful for testing sift-down when no right child exists.
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.heap = [None, 8, 3]
    heap.size = 2

    heap._sift_down(1)

    assert heap.heap == [None, 3, 8]
    assert heap.is_valid_heap()

    print("Single child sift-down tests passed")
    
    # ------------------------------------------------------------
    # Repeated pop produces sorted order
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [7, 2, 9, 1, 6, 3, 8, 4, 5]

    for value in values:
        heap.push(value)

    result = []

    while not heap.is_empty():
        result.append(heap.pop())

    assert result == sorted(values)
    assert heap.heap == [None]
    assert heap.size_of() == 0
    assert heap.is_empty()

    print("Repeated pop tests passed")
    
    # ------------------------------------------------------------
    # Repeated pop with duplicates
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [4, 2, 2, 1, 1, 5]

    for value in values:
        heap.push(value)

    result = []

    while not heap.is_empty():
        result.append(heap.pop())

    assert result == [1, 1, 2, 2, 4, 5]
    assert heap.heap == [None]

    print("Duplicate pop tests passed")
    
    # ------------------------------------------------------------
    # Pop on empty heap
    # ------------------------------------------------------------

    heap = MinHeap()

    try:
        heap.pop()
        assert False
    except IndexError:
        pass

    print("Empty pop tests passed")
    
    # ------------------------------------------------------------
    # Heapify empty
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.heapify([])

    assert heap.heap == [None]
    assert heap.size_of() == 0
    assert heap.is_empty()
    assert heap.is_valid_heap()

    print("Empty heapify tests passed")
    
    # ------------------------------------------------------------
    # Heapify single element
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.heapify([10])

    assert heap.heap == [None, 10]
    assert heap.peek() == 10
    assert heap.size_of() == 1
    assert heap.is_valid_heap()

    print("Single heapify tests passed")
    
    # ------------------------------------------------------------
    # Heapify arbitrary array
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [9, 4, 7, 1, 3, 6, 2]

    heap.heapify(values)

    assert heap.heap[0] is None
    assert heap.peek() == 1
    assert heap.heap[1] == 1
    assert heap.size_of() == len(values)
    assert len(heap.heap) == heap.size_of() + 1
    assert heap.is_valid_heap()

    print("Basic heapify tests passed")
    
    # ------------------------------------------------------------
    # Heapify reverse-sorted array
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    heap.heapify(values)

    assert heap.heap[0] is None
    assert heap.peek() == 1
    assert heap.size_of() == 10
    assert len(heap.heap) == 11
    assert heap.is_valid_heap()

    print("Reverse heapify tests passed")
    
    # ------------------------------------------------------------
    # Heapify already valid heap
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [1, 3, 2, 7, 6, 4, 5]

    heap.heapify(values)

    assert heap.peek() == 1
    assert heap.size_of() == len(values)
    assert heap.is_valid_heap()

    print("Already-valid heapify tests passed")
    
    # ------------------------------------------------------------
    # Heapify does not alias input
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [5, 3, 8, 1]

    heap.heapify(values)

    values.append(-100)

    assert heap.size_of() == 4
    assert -100 not in heap.heap
    assert heap.heap[0] is None
    assert heap.is_valid_heap()

    print("Heapify copy tests passed")
    
    # ------------------------------------------------------------
    # Mixed operations
    # ------------------------------------------------------------

    heap = MinHeap()

    heap.push(5)
    heap.push(2)
    heap.push(8)

    assert heap.pop() == 2

    heap.push(1)
    heap.push(7)

    assert heap.pop() == 1
    assert heap.pop() == 5
    assert heap.pop() == 7
    assert heap.pop() == 8

    assert heap.heap == [None]
    assert heap.is_empty()
    assert heap.size_of() == 0

    print("Mixed operation tests passed")

    # ------------------------------------------------------------
    # Larger sequence
    # ------------------------------------------------------------

    heap = MinHeap()

    values = [
        50, 20, 70, 10, 40,
        60, 80, 5, 15, 30,
        45, 55, 65, 75, 90
    ]

    for value in values:
        heap.push(value)

    assert heap.size_of() == len(values)
    assert len(heap.heap) == len(values) + 1
    assert heap.heap[0] is None
    assert heap.peek() == 5
    assert heap.is_valid_heap()

    result = []

    while not heap.is_empty():
        result.append(heap.pop())

    assert result == sorted(values)
    assert heap.heap == [None]

    print("Large sequence tests passed")

    print("All Min Heap tests passed!")