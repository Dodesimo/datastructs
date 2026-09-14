class Node:
    def __init__(self, key, value):
        """
        Construct an AVL tree node.

        Fields:
        - key: key used for BST ordering
        - value: value associated with the key
        - left: left child
        - right: right child
        - height: height of this node

        Convention:
        - Leaf node height = 1
        - None height = 0
        """
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        """
        Construct an empty AVL tree.

        Fields:
        - root: root node
        - size: number of key-value pairs

        Complexity:
            O(1)
        """
        self.root = None
        self.size = 0

    # ============================================================
    # Basic helpers
    # ============================================================

    def _height(self, node):
        """
        Return the height of node.

        Requirements:
        - None has height 0.

        Complexity:
            O(1)
        """
        if node is None:
            return 0
        return node.height

    def _update_height(self, node):
        """
        Recalculate node.height based on its children.

        Formula:

            node.height =
                1 + max(height(node.left), height(node.right))

        Complexity:
            O(1)
        """
        if not node:
            return 0
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """
        Return the balance factor of node.

        Convention:

            balance_factor =
                height(left subtree) - height(right subtree)

        AVL invariant:

            -1 <= balance_factor <= 1

        Complexity:
            O(1)
        """
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    # ============================================================
    # Rotations
    # ============================================================

    def _rotate_left(self, node):
        """
        Perform a left rotation.

              x                       y
             / \\                     / \\
            A   y        ->         x   C
               / \\                 / \\
              B   C               A   B

        Requirements:
        - Return the new root of this subtree.
        - Update heights in the correct order.

        Complexity:
            O(1)
        """
        '''
        the new root is node.right
        node.right.left stores the old node
        the old node.right.left becomes node.right of o
        '''
        new_root = node.right 
        new_right_child = node.right.left

        new_root.left = node
        node.right = new_right_child

        self._update_height(node.right)
        self._update_height(node.left)
        self._update_height(node)
        self._update_height(new_root.right)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node):
        """
        Perform a right rotation.

                  y                 x
                 / \\               / \\
                x   C     ->      A   y
               / \\                   / \\
              A   B                 B   C

        Requirements:
        - Return the new root of this subtree.
        - Update heights in the correct order.

        Complexity:
            O(1)
        """
        new_root = node.left
        new_left_child = node.left.right

        new_root.right = node
        node.left = new_left_child

        self._update_height(node.left)
        self._update_height(node.right)
        self._update_height(new_root.left)
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    # ============================================================
    # Rebalancing
    # ============================================================

    def _rebalance(self, node):
        """
        Restore the AVL invariant at node.

        Cases:

        1. Left-Left
        2. Left-Right
        3. Right-Right
        4. Right-Left

        Requirements:
        - Update node's height first.
        - Determine the balance factor.
        - Apply the appropriate rotation(s).
        - Return the root of the balanced subtree.

        Complexity:
            O(1)
        """
        self._update_height(node)
        root_balance_factor = self._balance_factor(node)    
        right_balance_factor = self._balance_factor(node.right)
        left_balance_factor = self._balance_factor(node.left)
        if not -1 <= root_balance_factor <= 1:
            # left - left, left heavy, so rotate right
            if root_balance_factor > 0 and left_balance_factor >= 0:
                return self._rotate_right(node)
            # right - right, right heavy (so both positive)
            elif root_balance_factor < 0 and right_balance_factor <= 0:
                return self._rotate_left(node)
            # left - right, imbalance to the left and then the right (node (positive), and then left child (negative))
            elif root_balance_factor > 0 and left_balance_factor < 0:
                # left rotation for left child
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            # right-left, imbalance to the right and then the left (node is negative, right child positive)
            elif root_balance_factor < 0 and right_balance_factor > 0:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        return node

    # ============================================================
    # Insertion
    # ============================================================

    def put(self, key, value):
        """
        Insert or update a key-value pair.

        Requirements:
        - Maintain the BST invariant.
        - Maintain the AVL balance invariant.
        - If key already exists:
            update its value.
        - Updating an existing key does NOT increase size.
        - Inserting a new key increases size by 1.

        Complexity:
            O(log n)
        """
        self.root = self._put(self.root, key, value)

    def _put(self, node, key, value):
        """
        Recursive insertion helper.

        Suggested flow:

        1. Perform normal BST insertion.
        2. Update height.
        3. Rebalance.
        4. Return the subtree root.

        Complexity:
            O(log n)
        """
        if not node:
            self.size += 1
            return Node(key = key, value = value)
        elif key > node.key:
            # go right
            node.right = self._put(node.right, key, value)
        elif key < node.key:
            node.left = self._put(node.left, key, value)
        else:
            node.value = value
        self._update_height(node)
        return self._rebalance(node)

    # ============================================================
    # Search
    # ============================================================

    def get(self, key):
        """
        Return the value associated with key.

        Raise:
            KeyError if the key does not exist.

        Complexity:
            O(log n)
        """
        def dfs(node, key):
            if not node:
                raise KeyError("does not exist")
            elif node.key == key:
                return node.value
            elif node.key < key:
                # go right
                return dfs(node.right, key)
            else:
                return dfs(node.left, key)
        
        return dfs(self.root, key)

    def contains(self, key):
        """
        Return True if key exists, otherwise False.

        Complexity:
            O(log n)
        """
        def dfs(node, key):
            if not node:
                return False
            elif node.key == key:
                return True
            elif node.key < key:
                # go right
                return dfs(node.right, key)
            else:
                return dfs(node.left, key)
        
        return dfs(self.root, key)

    # ============================================================
    # Removal
    # ============================================================

    def remove(self, key):
        """
        Remove key from the AVL tree and return its value.

        Raise:
            KeyError if key does not exist.

        Requirements:
        - Handle normal BST deletion cases:
            1. Leaf
            2. One child
            3. Two children
        - Restore AVL balance after deletion.
        - Decrease size exactly once.

        Complexity:
            O(log n)
        """
        self.root, item = self._remove(self.root, key)
        self.size -= 1
        return item

    def _remove(self, node, key):
        """
        Recursive removal helper.

        Suggested flow:

        1. Perform normal BST deletion.
        2. Update height while recursion unwinds.
        3. Rebalance.
        4. Return the new subtree root.

        Complexity:
            O(log n)
        """
        if not node:
            raise KeyError("not found")
        elif node.key == key:
            item = node.value
            if not node.left and not node.right:
                # leaf node, return None
                return None, item
            elif not node.right:
                return node.left, item
            elif not node.left:
                return node.right, item
            else:
                # two children, so find the successor
                successor = self._min_node(node)
                node.key = successor.key
                node.value = successor.value
                # delete the successor
                node.right, _ = self._remove(node.right, successor.key)
        elif node.key < key:
            # go right
            node.right, item = self._remove(node.right, key)
        else:
            # go left
            node.left, item = self._remove(node.left, key)
        
        self._update_height(node)
        new_root = self._rebalance(node)
        return new_root, item

    def _min_node(self, node):
        """
        Return the node containing the minimum key
        in this subtree.

        Useful for finding the inorder successor.

        Complexity:
            O(log n)
        """
        start = node.right
        while start.left:
            start = start.left
        return start

    # ============================================================
    # Miscellaneous
    # ============================================================

    def min_key(self):
        """
        Return the minimum key.

        Raise:
            KeyError if tree is empty.

        Complexity:
            O(log n)
        """
        if self.root is None:
            raise KeyError("empty tree")
        start = self.root
        while start.left:
            start = start.left
        return start.key

    def max_key(self):
        """
        Return the maximum key.

        Raise:
            KeyError if tree is empty.

        Complexity:
            O(log n)
        """
        if self.root is None:
            raise KeyError("empty tree")
        start = self.root
        while start.right:
            start = start.right
        return start.key

    def size_of(self):
        """
        Return number of nodes.

        Complexity:
            O(1)
        """
        return self.size

    def is_empty(self):
        """
        Return True if tree is empty.

        Complexity:
            O(1)
        """
        return self.size == 0

    # ============================================================
    # Traversals
    # ============================================================

    def inorder(self):
        """
        Return keys in sorted order.

        Example:

            [10, 20, 30, 40]

        Complexity:
            O(n)
        """
        def dfs(root, result):
            if not root:
                return 
            dfs(root.left, result)
            result.append(root.key)
            dfs(root.right, result)
        
        result = []
        dfs(self.root, result)
        return result 

    def preorder(self):
        """
        Return keys in preorder.

        Complexity:
            O(n)
        """
        def dfs(root, result):
            if not root:
                return 
            result.append(root.key)
            dfs(root.left, result)
            dfs(root.right, result)
        
        result = []
        dfs(self.root, result)
        return result 

    # ============================================================
    # Validation
    # ============================================================

    def is_valid_bst(self):
        """
        Return True if the BST ordering invariant holds.

        Complexity:
            O(n)
        """
        def dfs(node, left, right):
            if not node:
                return True
            if node.key <= left or node.key >= right:
                return False
            return dfs(node.left, left, node.key) and dfs(node.right, node.key, right)
        
        return dfs(self.root, float('-inf'), float('inf'))

    def is_valid_avl(self):
        """
        Return True if:

        1. Every node has the correct stored height.
        2. Every node has balance factor -1, 0, or 1.

        Complexity:
            O(n)
        """
        result = True
        def dfs(root):
            nonlocal result
            if not root:    
                return 0
            leftHeight = dfs(root.left)
            rightHeight = dfs(root.right)
            if max(leftHeight, rightHeight) + 1 != root.height:
                result = False
            if not -1 <= leftHeight - rightHeight <= 1:
                result = False
            return max(leftHeight, rightHeight) + 1
        dfs(self.root)
        return result
            

# ================================================================
# Tests
# ================================================================

if __name__ == "__main__":
    tree = AVLTree()

    # ------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------

    assert tree.root is None
    assert tree.size_of() == 0
    assert tree.is_empty()

    print("Initialization tests passed")
    
    # ------------------------------------------------------------
    # Basic insertion
    # ------------------------------------------------------------

    tree.put(20, "twenty")
    tree.put(10, "ten")
    tree.put(30, "thirty")

    assert tree.size_of() == 3
    assert tree.get(20) == "twenty"
    assert tree.get(10) == "ten"
    assert tree.get(30) == "thirty"

    assert tree.inorder() == [10, 20, 30]

    print("Basic insertion tests passed")
    
    # ------------------------------------------------------------
    # Update existing key
    # ------------------------------------------------------------

    old_size = tree.size_of()

    tree.put(20, "TWENTY")
    print(tree.get(20))
    #assert tree.get(20) == "TWENTY"
    assert tree.size_of() == old_size

    print("Update tests passed")
    
    # ------------------------------------------------------------
    # Left-Left rotation
    #
    #       30              20
    #      /               /  \
    #     20      ->      10   30
    #    /
    #   10
    # ------------------------------------------------------------

    tree = AVLTree()

    tree.put(30, 30)
    tree.put(20, 20)
    tree.put(10, 10)

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.is_valid_avl()

    print("LL rotation tests passed")
    
    # ------------------------------------------------------------
    # Right-Right rotation
    #
    #   10                    20
    #     \                  /  \
    #      20      ->       10   30
    #        \
    #         30
    # ------------------------------------------------------------

    tree = AVLTree()

    tree.put(10, 10)
    tree.put(20, 20)
    tree.put(30, 30)

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.is_valid_avl()

    print("RR rotation tests passed")
    
    # ------------------------------------------------------------
    # Left-Right rotation
    #
    #       30               20
    #      /                /  \
    #     10       ->      10   30
    #       \
    #        20
    # ------------------------------------------------------------

    tree = AVLTree()

    tree.put(30, 30)
    tree.put(10, 10)
    tree.put(20, 20)

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.is_valid_avl()

    print("LR rotation tests passed")
    
    # ------------------------------------------------------------
    # Right-Left rotation
    #
    #   10                   20
    #     \                 /  \
    #      30      ->      10   30
    #     /
    #    20
    # ------------------------------------------------------------

    tree = AVLTree()

    tree.put(10, 10)
    tree.put(30, 30)
    tree.put(20, 20)

    assert tree.root.key == 20
    assert tree.root.left.key == 10
    assert tree.root.right.key == 30
    assert tree.is_valid_avl()

    print("RL rotation tests passed")
    
    # ------------------------------------------------------------
    # Larger insertion sequence
    # ------------------------------------------------------------

    tree = AVLTree()

    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    for value in values:
        tree.put(value, value)

    assert tree.inorder() == sorted(values)
    assert tree.is_valid_bst()
    assert tree.is_valid_avl()

    print("Large insertion tests passed")
    
    # ------------------------------------------------------------
    # Contains
    # ------------------------------------------------------------

    assert tree.contains(40)
    assert tree.contains(80)
    assert not tree.contains(999)

    print("Contains tests passed")
    
    # ------------------------------------------------------------
    # Min / max
    # ------------------------------------------------------------

    assert tree.min_key() == 10
    assert tree.max_key() == 80

    print("Min/max tests passed")
    
    # ------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------

    old_size = tree.size_of()

    removed = tree.remove(20)

    assert removed == 20
    assert not tree.contains(20)
    assert tree.size_of() == old_size - 1

    assert tree.is_valid_bst()
    assert tree.is_valid_avl()

    print("Removal tests passed")

    print("All AVL Tree tests passed!")
