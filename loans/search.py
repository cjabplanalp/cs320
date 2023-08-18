class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left.values)
        if self.right != None:
            size += len(self.right.values)
        return size
    
    def lookup(self, key):
        if self.key == key:
            return self.values
        
        if key < self.key:
            if self.left != None: 
                return self.left.lookup(key)
            else:
                return []
        elif key > self.key:
            if self.right != None:
                return self.right.lookup(key)
            else:
                return []
            
    #cited from Joe James on YouTube
    def height(self):
        if self.left and self.right:
            return 1 + max(self.left.height(), self.right.height())
        elif self.left:
            return 1 + self.left.height()
        elif self.right:
            return 1 + self.right.height()
        else:
            return 1
        
    #cited from Joe James on YouTube
    def nodecount(self):
        if self.left and self.right:
            return 1 + self.left.nodecount() + self.right.nodecount()
        elif self.left:
            return 1 + self.left.nodecount()
        elif self.right:
            return 1 + self.right.nodecount()
        else:
            return 1
        
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        # SORTED ALPHABETICALLY DESCENDING
        self.__dump(node.left)             # 3
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)            # 1

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, target):
        return self.root.lookup(target)
    
    #cited from Joe James on YouTube    
    def height(self):
        if self.root:
            return self.root.height()
        else:
            return 0
        
    #cited from Joe James on YouTube    
    def nodecount(self):
        if self.root:
            return self.root.nodecount()
        else:
            return 0