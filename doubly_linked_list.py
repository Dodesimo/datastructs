class Node:
    def __init__(self, data):
        """
        Node stored inside the doubly linked list.

        Each node keeps:
        - data
        - reference to previous node
        - reference to next node
        """
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        """
        Construct an empty doubly linked list.

        Requirements:
        - head should start as None
        - tail should start as None
        - size should start at 0
        """
        self.head = None
        self.tail = None
        self.size = 0

    def add_at_index(self, index, data):
        """
        Add data at the specified index.

        Valid indices:
            0 <= index <= size

        Complexity:
            O(1) when index == 0 or index == size
            O(n) otherwise

        Raise:
            IndexError if index < 0 or index > size
            ValueError if data is None
        """
        if index < 0 or index > self.size:
            raise IndexError("out of bounds")
        
        if data is None:
            raise ValueError("data is invalid")
        
        if index == 0:
            return self.add_to_front(data)
        
        if index == self.size:
            return self.add_to_back(data)
        
        temp = None
        if index < self.size // 2:
            temp = self.head
            counter = 0
            while counter < index:
                temp = temp.next
                counter += 1
        else:
            temp = self.tail 
            counter = self.size - 1
            while counter > index:
                temp = temp.prev
                counter -= 1
        
        newNode = Node(data = data)
        prev = temp.prev
        prev.next = newNode
        newNode.prev = prev
        newNode.next = temp
        temp.prev = newNode
        self.size += 1
        return 

    def add_to_front(self, data):
        """
        Add data to the front of the list.

        Complexity:
            O(1)

        Raise:
            ValueError if data is None
        """
        if data is None:
            raise ValueError("invalid data")
        
        node = Node(data = data)

        if self.size == 0:
            self.head = node
            self.tail = node
            self.size += 1
            return 

        node.next = self.head
        self.head.prev = node
        self.head = node
        self.size += 1

    def add_to_back(self, data):
        """
        Add data to the back of the list.

        Complexity:
            O(1)

        Raise:
            ValueError if data is None
        """
        if data is None:
            raise ValueError("invalid data")
        
        node = Node(data = data)

        if self.size == 0:
            self.head = node
            self.tail = node
            self.size += 1
            return 
        
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        self.size += 1
        

    def remove_at_index(self, index):
        """
        Remove and return the element at index.

        Complexity:
            O(1) when index == 0 or index == size - 1
            O(n) otherwise

        Raise:
            IndexError if index < 0 or index >= size
        """
        if index < 0 or index >= self.size:
            raise IndexError("invalid index")

        if index == 0:
            return self.remove_from_front()
        
        if index == self.size - 1:
            return self.remove_from_back()

        prev = None
        curr = self.head
        position = 0 
        
        while position < index:
            prev = curr
            curr = curr.next
            position += 1

        # curr is at the index, prev is the index before
        nextNode = curr.next

        prev.next = nextNode
        nextNode.prev = prev
        self.size -= 1
        return curr.data

    def remove_from_front(self):
        """
        Remove and return the first element.

        Complexity:
            O(1)

        Raise:
            IndexError if the list is empty
        """
        if self.size == 0:
            raise IndexError("empty list")
        
        if self.size == 1:
            item = self.head
            self.head = None
            self.tail = None
            self.size = 0
            return item.data
        
        item = self.head
        self.head = self.head.next
        self.head.prev = None
        self.size -= 1
        return item.data

    def remove_from_back(self):
        """
        Remove and return the last element.

        Complexity:
            O(1)

        Raise:
            IndexError if the list is empty
        """
        if self.size == 0:
            raise IndexError("empty list")
        
        if self.size == 1:
            item = self.head
            self.head = None
            self.tail = None
            self.size = 0
            return item.data
        
        item = self.tail
        self.tail = self.tail.prev
        self.tail.next = None
        self.size -= 1
        return item.data

    def remove_last_occurrence(self, data):
        """
        Remove and return the last occurrence of data.

        You should take advantage of the tail pointer and
        traverse backward.

        Complexity:
            O(n)

        Raise:
            ValueError if data is None
            LookupError if data does not exist
        """
        if data is None:
            raise ValueError("data is none")
        
        if self.size == 1 and self.head.data == data:
            self.head = None
            self.tail = None
            self.size = 0

        curr = self.tail
        nxt =  None
        found = False
        
        while curr:
            if curr.data == data:
                found = True
                break
            nxt = curr
            curr = curr.prev
        
        if not found:
            raise LookupError("not found")
        
        # prev is one before curr, curr is the present, nxt is the value after
        if curr == self.head:
            return remove_from_front()
        if curr == self.tail:
            return remove_from_back()

        prev = curr.prev
        prev.next = nxt
        nxt.prev = prev
        self.size -= 1
        return curr.data

    def get(self, index):
        """
        Return the element at index.

        You should optimize traversal:
        - if index is in the first half, start at head
        - if index is in the second half, start at tail

        Complexity:
            O(n)

        Raise:
            IndexError if index < 0 or index >= size
        """
        if index < 0 or index >= self.size:
            raise IndexError

        midpoint = self.size // 2
        if index < midpoint:
            position = 0
            curr = self.head
            while curr:
                if position == index:
                    return curr.data
                position += 1
                curr = curr.next 
        else:
            position = self.size - 1
            curr = self.tail
            while curr:
                if position == index:
                    return curr.data
                position -= 1
                curr = curr.prev
        return -1

    def is_empty(self):
        """
        Return True if the list is empty.

        Complexity:
            O(1)
        """
        return self.size == 0

    def clear(self):
        """
        Remove all elements.

        After clearing:
        - head is None
        - tail is None
        - size is 0

        Complexity:
            O(1)
        """
        self.head = None
        self.tail = None
        self.size = 0

    def get_size(self):
        """
        Return the number of elements.

        Complexity:
            O(1)
        """
        return self.size

    def get_head(self):
        """
        Return the head node.

        Primarily useful for testing.
        """
        return self.head

    def get_tail(self):
        """
        Return the tail node.

        Primarily useful for testing.
        """
        return self.tail


def main():

    # ==================================================
    # TEST 1: INITIALIZATION
    # ==================================================

    dll = DoublyLinkedList()

    assert dll.get_size() == 0
    assert dll.is_empty() is True
    assert dll.get_head() is None
    assert dll.get_tail() is None

    print("Test 1 passed: initialization")

    
    # ==================================================
    # TEST 2: ADD TO FRONT
    # ==================================================

    dll.add_to_front(30)
    dll.add_to_front(20)
    dll.add_to_front(10)

    
    assert dll.get_size() == 3
    assert dll.get(0) == 10
    assert dll.get(1) == 20
    assert dll.get(2) == 30

    assert dll.get_head().data == 10
    assert dll.get_tail().data == 30

    print("Test 2 passed: add_to_front")

    
    # ==================================================
    # TEST 3: ADD TO BACK
    # ==================================================

    dll = DoublyLinkedList()

    dll.add_to_back(10)
    dll.add_to_back(20)
    dll.add_to_back(30)

    assert dll.get_size() == 3
    assert dll.get(0) == 10
    assert dll.get(1) == 20
    assert dll.get(2) == 30

    assert dll.get_head().data == 10
    assert dll.get_tail().data == 30

    print("Test 3 passed: add_to_back")

    
    # ==================================================
    # TEST 4: HEAD / TAIL POINTERS
    # ==================================================

    head = dll.get_head()
    tail = dll.get_tail()

    assert head.prev is None
    assert tail.next is None

    assert head.next.data == 20
    assert head.next.prev is head

    assert tail.prev.data == 20
    assert tail.prev.next is tail

    print("Test 4 passed: head/tail pointers")

    
    # ==================================================
    # TEST 5: ADD AT INDEX
    # ==================================================

    dll = DoublyLinkedList()

    dll.add_to_back(10)
    dll.add_to_back(30)
    dll.add_to_back(40)

    dll.add_at_index(1, 20)

    assert dll.get_size() == 4

    assert dll.get(0) == 10
    assert dll.get(1) == 20
    assert dll.get(2) == 30
    assert dll.get(3) == 40

    print("Test 5 passed: add_at_index")

    
    # ==================================================
    # TEST 6: ADD AT BOUNDARIES
    # ==================================================

    dll.add_at_index(0, 0)
    dll.add_at_index(dll.get_size(), 50)

    assert dll.get_size() == 6

    assert dll.get(0) == 0
    assert dll.get(5) == 50

    assert dll.get_head().data == 0
    assert dll.get_tail().data == 50

    print("Test 6 passed: boundary insertion")

    
    # ==================================================
    # TEST 7: FORWARD LINK STRUCTURE
    # ==================================================

    current = dll.get_head()
    values = []

    while current is not None:
        values.append(current.data)
        current = current.next

    assert values == [0, 10, 20, 30, 40, 50]

    print("Test 7 passed: forward links")

    
    # ==================================================
    # TEST 8: BACKWARD LINK STRUCTURE
    # ==================================================

    current = dll.get_tail()
    values = []

    while current is not None:
        values.append(current.data)
        current = current.prev

    assert values == [50, 40, 30, 20, 10, 0]

    print("Test 8 passed: backward links")

    
    # ==================================================
    # TEST 9: REMOVE FROM FRONT
    # ==================================================

    removed = dll.remove_from_front()
    
    assert removed == 0
    assert dll.get_size() == 5
    assert dll.get_head().data == 10
    assert dll.get_head().prev is None

    print("Test 9 passed: remove_from_front")

    
    # ==================================================
    # TEST 10: REMOVE FROM BACK
    # ==================================================

    removed = dll.remove_from_back()

    assert removed == 50
    assert dll.get_size() == 4
    assert dll.get_tail().data == 40
    assert dll.get_tail().next is None

    print("Test 10 passed: remove_from_back")

    
    # ==================================================
    # TEST 11: REMOVE AT INDEX
    # ==================================================

    # Current:
    # 10 <-> 20 <-> 30 <-> 40

    removed = dll.remove_at_index(1)

    assert removed == 20
    assert dll.get_size() == 3

    assert dll.get(0) == 10
    assert dll.get(1) == 30
    assert dll.get(2) == 40

    print("Test 11 passed: remove_at_index")

    
    # ==================================================
    # TEST 12: POINTERS AFTER REMOVAL
    # ==================================================

    head = dll.get_head()

    assert head.data == 10
    assert head.next.data == 30
    assert head.next.prev is head

    assert head.next.next.data == 40
    assert head.next.next.prev is head.next

    print("Test 12 passed: pointers after removal")

    
    # ==================================================
    # TEST 13: REMOVE LAST OCCURRENCE
    # ==================================================

    dll = DoublyLinkedList()

    for value in [10, 20, 30, 20, 40]:
        dll.add_to_back(value)

    removed = dll.remove_last_occurrence(20)
    
    assert removed == 20
    assert dll.get_size() == 4

    assert dll.get(0) == 10
    assert dll.get(1) == 20
    assert dll.get(2) == 30
    assert dll.get(3) == 40

    print("Test 13 passed: remove_last_occurrence")

    
    # ==================================================
    # TEST 14: SINGLE ELEMENT REMOVAL
    # ==================================================

    dll = DoublyLinkedList()

    dll.add_to_back(10)

    assert dll.get_head() is dll.get_tail()

    removed = dll.remove_from_front()

    assert removed == 10
    assert dll.get_size() == 0
    assert dll.get_head() is None
    assert dll.get_tail() is None

    print("Test 14 passed: single element removal")

    
    # ==================================================
    # TEST 15: INVALID GET
    # ==================================================

    dll = DoublyLinkedList()

    dll.add_to_back(10)

    try:
        dll.get(-1)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    try:
        dll.get(1)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 15 passed: invalid get")

    
    # ==================================================
    # TEST 16: INVALID ADD INDEX
    # ==================================================

    dll = DoublyLinkedList()

    try:
        dll.add_at_index(-1, 10)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    try:
        dll.add_at_index(1, 10)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 16 passed: invalid add index")

    
    # ==================================================
    # TEST 17: NONE DATA
    # ==================================================

    dll = DoublyLinkedList()

    try:
        dll.add_to_front(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        dll.add_to_back(None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        dll.add_at_index(0, None)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    print("Test 17 passed: None rejected")

    
    # ==================================================
    # TEST 18: REMOVE FROM EMPTY
    # ==================================================

    dll = DoublyLinkedList()

    try:
        dll.remove_from_front()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    try:
        dll.remove_from_back()
        assert False, "Expected IndexError"
    except IndexError:
        pass

    print("Test 18 passed: empty removal")

    
    # ==================================================
    # TEST 19: CLEAR
    # ==================================================

    dll = DoublyLinkedList()

    for i in range(100):
        dll.add_to_back(i)

    dll.clear()

    assert dll.get_size() == 0
    assert dll.is_empty() is True
    assert dll.get_head() is None
    assert dll.get_tail() is None

    print("Test 19 passed: clear")

    # ==================================================
    # TEST 20: LARGE LIST
    # ==================================================

    dll = DoublyLinkedList()

    for i in range(1000):
        dll.add_to_back(i)

    assert dll.get_size() == 1000

    for i in range(1000):
        assert dll.get(i) == i

    print("Test 20 passed: large list")


    print()
    print("============================")
    print("ALL TESTS PASSED")
    print("============================") 

if __name__ == "__main__":
    main()