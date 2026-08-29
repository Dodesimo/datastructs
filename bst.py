class Node:
    def __init__(self, key, value):
        """
        Construct a BST node.

        Fields:
        - key: key used for ordering
        - value: value associated with the key
        - left: left child
        - right: right child
        """
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        """
        Construct an empty binary search tree.

        Requirements:
        - root starts as None
        - size starts at 0

        Complexity:
            O(1)
        """
        self.root = None
        self.size = 0

    def put(self, key, value):
        """
        Insert a key-value pair into the BST.

        BST invariant:

            keys in left subtree < node.key
            keys in right subtree > node.key

        Requirements:
        - If the key does not exist, insert a new node.
        - If the key already exists, update its value.
        - Updating an existing key does NOT increase size.
        - Inserting a new key increases size by 1.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        '''
        pointer reinforcement, after doing manipulation on pointers always return the item itself
        '''
        def dfs(node, key, value):
            if not node:
                self.size += 1
                return Node(key = key, value = value)
            if key < node.key:
                node.left = dfs(node.left, key, value)
            elif key > node.key:
                node.right = dfs(node.right, key, value)
            else:
                node.value = value
            return node
        
        self.root = dfs(self.root, key, value)

    def get(self, key):
        """
        Return the value associated with key.

        Requirements:
        - Search according to BST ordering.
        - Raise KeyError if the key does not exist.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        def dfs(node, key):
            if not node:
                return float('-inf')
            if node.key == key:
                return node.value
            if key < node.key:
                return dfs(node.left, key)
            else:
                return dfs(node.right, key)
        
        value = dfs(self.root, key)
        if value != float('-inf'):
            return value
        else:
            raise KeyError("key doesn't exist")
        

    def contains(self, key):
        """
        Return True if key exists in the tree.
        Otherwise return False.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        def dfs(node, key):
            if not node:
                return False
            if node.key == key:
                return True
            if key < node.key:
                return dfs(node.left, key)
            else:
                return dfs(node.right, key)
        
        return dfs(self.root, key)

    def remove(self, key):
        """
        Remove key from the BST and return its value.

        Raise KeyError if key does not exist.

        There are three deletion cases:

        1. Leaf node

               5

           Simply remove it.

        2. Node with one child

               5
                \
                 8

           Replace the node with its child.

        3. Node with two children

               5
              / \
             3   8

           Replace the node's key/value with either:

           - inorder successor:
                 smallest node in right subtree

           OR

           - inorder predecessor:
                 largest node in left subtree

           Then remove that successor/predecessor node.

        Requirements:
        - size decreases by 1 exactly once.
        - BST ordering must remain valid.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        '''
        key idea: pointer reinforcement, alter pointers and return the value itself
        '''
        def dfs(node, key):
            if not node:
                raise KeyError("key doesn't exist")
            if key == node.key:
                value = node.value
                if node.left and node.right:
                    # let's use in order predecessor
                    predecessor = node.left
                    while predecessor.right:
                        predecessor = predecessor.right
                    # deleted the node
                    node.key = predecessor.key
                    node.value = predecessor.value
                    # recursively delete the predecessor (use the function itself)
                    node.left, __ = dfs(node.left, predecessor.key)
                    return node, value
                elif not node.left and not node.right:
                    return None, value # this is a leaf we just delete it
                elif node.left:
                    # no right
                    return node.left, value
                elif node.right:
                    # no left
                    return node.right, value
            elif key < node.key:
                node.left, deleted_value = dfs(node.left, key)
                return node, deleted_value
            else:
                node.right, deleted_value = dfs(node.right, key)
                return node, deleted_value
        
        self.root, item = dfs(self.root, key)
        self.size -= 1
        return item

    def min(self):
        """
        Return the (key, value) pair with the smallest key.

        The minimum node is found by repeatedly
        following left children.

        Raise KeyError if tree is empty.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        if not node:
            raise KeyError("tree empty")
        node = self.root
        while node.left:
            node = node.left
        return (node.key, node.value)

    def max(self):
        """
        Return the (key, value) pair with the largest key.

        The maximum node is found by repeatedly
        following right children.

        Raise KeyError if tree is empty.

        Complexity:
            Average: O(log n)
            Worst:   O(n)
        """
        node = self.root
        while node.right:
            node = node.right
        return (node.key, node.value)

    def inorder(self):
        """
        Return all (key, value) pairs in inorder traversal.

        Inorder:

            left -> node -> right

        Important:
        For a valid BST, this returns keys in sorted order.

        Example:

            Tree:

                    5
                   / \
                  3   8
                 / \
                2   4

            Result:

                [
                    (2, ...),
                    (3, ...),
                    (4, ...),
                    (5, ...),
                    (8, ...)
                ]

        Complexity:
            O(n)
        """
        result = []
        def dfs(node, result):
            if not node:
                return
            dfs(node.left, result)
            result.append((node.key, node.value))
            dfs(node.right, result)
        dfs(self.root, result)
        return result

    def preorder(self):
        """
        Return all (key, value) pairs in preorder traversal.

        Preorder:

            node -> left -> right

        Complexity:
            O(n)
        """
        result = []
        def dfs(node, result):
            if not node:
                return
            result.append((node.key, node.value))
            dfs(node.left, result)
            dfs(node.right, result)
        dfs(self.root, result)
        return result

    def postorder(self):
        """
        Return all (key, value) pairs in postorder traversal.

        Postorder:

            left -> right -> node

        Complexity:
            O(n)
        """
        result = []
        def dfs(node, result):
            if not node:
                return
            dfs(node.left, result)
            dfs(node.right, result)
            result.append((node.key, node.value))
        dfs(self.root, result)
        return result

    def height(self):
        """
        Return the height of the tree.

        Definition used here:

            empty tree     -> -1
            single node    -> 0

        Example:

                5           height = 2
               /
              3
             /
            2

        Complexity:
            O(n)
        """
        def dfs(node):
            if not node:
                return -1
            leftHeight = dfs(node.left)
            rightHeight = dfs(node.right)
            return 1 + max(leftHeight, rightHeight)
        
        return dfs(self.root)

    def is_empty(self):
        """
        Return True if tree contains no nodes.

        Complexity:
            O(1)
        """
        return self.size == 0

    def size_of(self):
        """
        Return number of nodes currently stored.

        Complexity:
            O(1)
        """
        return self.size

    def clear(self):
        """
        Remove all elements from the tree.

        After clearing:
        - root is None
        - size is 0

        Complexity:
            O(1) from the tree's perspective.
            Python garbage collection handles the nodes.
        """
        self.root = None
        self.size = 0


def main():
    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    bst = BinarySearchTree()

    assert bst.root is None
    assert bst.size_of() == 0
    assert bst.is_empty() is True

    print("Initialization tests passed")

    
    # ---------------------------------------------------------
    # Basic insertion
    #
    # Expected tree:
    #
    #              50
    #          30      70
    #        20  40  60  80
    #
    # ---------------------------------------------------------

    bst.put(50, "fifty")
    bst.put(30, "thirty")
    bst.put(70, "seventy")
    bst.put(20, "twenty")
    bst.put(40, "forty")
    bst.put(60, "sixty")
    bst.put(80, "eighty")

    assert bst.size_of() == 7
    assert bst.is_empty() is False
    
    assert bst.root.key == 50
    assert bst.root.left.key == 30
    assert bst.root.right.key == 70
    assert bst.root.left.left.key == 20
    assert bst.root.left.right.key == 40
    assert bst.root.right.left.key == 60
    assert bst.root.right.right.key == 80

    print("Insertion tests passed")

    
    # ---------------------------------------------------------
    # Get
    # ---------------------------------------------------------

    assert bst.get(50) == "fifty"
    assert bst.get(20) == "twenty"
    assert bst.get(80) == "eighty"
    assert bst.get(40) == "forty"

    try:
        bst.get(100)
        assert False
    except KeyError:
        pass

    print("Get tests passed")

    
    # ---------------------------------------------------------
    # Contains
    # ---------------------------------------------------------

    assert bst.contains(50) is True
    assert bst.contains(20) is True
    assert bst.contains(80) is True
    assert bst.contains(100) is False

    print("Contains tests passed")

    
    # ---------------------------------------------------------
    # Updating existing key
    # ---------------------------------------------------------

    old_size = bst.size_of()

    bst.put(30, "UPDATED")

    assert bst.get(30) == "UPDATED"
    assert bst.size_of() == old_size

    print("Update tests passed")

    
    # ---------------------------------------------------------
    # Min / Max
    # ---------------------------------------------------------

    assert bst.min() == (20, "twenty")
    assert bst.max() == (80, "eighty")

    print("Min/max tests passed")

    
    # ---------------------------------------------------------
    # Traversals
    # ---------------------------------------------------------

    assert bst.inorder() == [
        (20, "twenty"),
        (30, "UPDATED"),
        (40, "forty"),
        (50, "fifty"),
        (60, "sixty"),
        (70, "seventy"),
        (80, "eighty"),
    ]

    assert bst.preorder() == [
        (50, "fifty"),
        (30, "UPDATED"),
        (20, "twenty"),
        (40, "forty"),
        (70, "seventy"),
        (60, "sixty"),
        (80, "eighty"),
    ]

    assert bst.postorder() == [
        (20, "twenty"),
        (40, "forty"),
        (30, "UPDATED"),
        (60, "sixty"),
        (80, "eighty"),
        (70, "seventy"),
        (50, "fifty"),
    ]

    print("Traversal tests passed")

    
    # ---------------------------------------------------------
    # Height
    # ---------------------------------------------------------    
    assert bst.height() == 2

    single = BinarySearchTree()

    assert single.height() == -1

    single.put(10, "ten")

    assert single.height() == 0

    single.put(5, "five")

    assert single.height() == 1

    print("Height tests passed")

    
    # ---------------------------------------------------------
    # Delete a leaf
    #
    # Before:
    #
    #              50
    #          30      70
    #        20  40  60  80
    #
    # Remove 20.
    #
    # After:
    #
    #              50
    #          30      70
    #            40  60  80
    #
    # ---------------------------------------------------------

    removed = bst.remove(20)

    assert removed == "twenty"
    assert bst.contains(20) is False
    assert bst.size_of() == 6

    assert bst.inorder() == [
        (30, "UPDATED"),
        (40, "forty"),
        (50, "fifty"),
        (60, "sixty"),
        (70, "seventy"),
        (80, "eighty"),
    ]

    print("Leaf deletion tests passed")

    
    # ---------------------------------------------------------
    # Delete a node with one child
    #
    # Before:
    #
    #              50
    #          30      70
    #            40  60  80
    #
    # Remove 30.
    #
    # After:
    #
    #              50
    #          40      70
    #                60  80
    #
    # ---------------------------------------------------------

    removed = bst.remove(30)

    assert removed == "UPDATED"
    assert bst.contains(30) is False
    assert bst.contains(40) is True
    assert bst.size_of() == 5

    assert bst.inorder() == [
        (40, "forty"),
        (50, "fifty"),
        (60, "sixty"),
        (70, "seventy"),
        (80, "eighty"),
    ]

    print("One-child deletion tests passed")

    
    # ---------------------------------------------------------
    # Delete a node with two children
    #
    # Remove 70.
    #
    # Inorder successor of 70 is 80.
    #
    # ---------------------------------------------------------

    removed = bst.remove(70)
    
    assert removed == "seventy"
    assert bst.contains(70) is False
    assert bst.size_of() == 4

    print(bst.inorder())

    
    assert bst.inorder() == [
        (40, "forty"),
        (50, "fifty"),
        (60, "sixty"),
        (80, "eighty"),
    ]

    print("Two-child deletion tests passed")

    
    # ---------------------------------------------------------
    # Delete root
    # ---------------------------------------------------------

    removed = bst.remove(50)

    assert removed == "fifty"
    assert bst.contains(50) is False
    assert bst.size_of() == 3

    assert bst.inorder() == [
        (40, "forty"),
        (60, "sixty"),
        (80, "eighty"),
    ]

    print("Root deletion tests passed")

    
    # ---------------------------------------------------------
    # Remove nonexistent key
    # ---------------------------------------------------------

    old_size = bst.size_of()

    try:
        bst.remove(999)
        assert False
    except KeyError:
        pass

    assert bst.size_of() == old_size

    print("Invalid deletion tests passed")

    
    # ---------------------------------------------------------
    # Degenerate / unbalanced BST
    #
    # 1
    #   2
    #     3
    #       4
    #         5
    #
    # ---------------------------------------------------------

    skewed = BinarySearchTree()

    for i in range(1, 6):
        skewed.put(i, str(i))

    assert skewed.size_of() == 5
    assert skewed.height() == 4

    assert skewed.inorder() == [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    print("Unbalanced BST tests passed")


    # ---------------------------------------------------------
    # Clear
    # ---------------------------------------------------------

    bst.clear()

    assert bst.root is None
    assert bst.size_of() == 0
    assert bst.is_empty() is True
    assert bst.height() == -1

    print("Clear tests passed")

    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    main()