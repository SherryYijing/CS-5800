class RBTree_node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'black'

class RBTree:
    def __init__(self):
        self.nil = RBTree_node(0)
        self.root = self.nil

#class Function:
    def inorder_tree_walk(self, x):
        if x != None:
            self.inorder_tree_walk(x.left)
            if x.key != 0:
                print('key: ', x.key, 'parent: ', x.parent.key, 'color: ', x.color)
            self.inorder_tree_walk(x.right)

    def left_rotate(self, T, x):
        y = x.right          #set y
        x.right = y.left     #turn y's left subtree into x's right subtree
        if y.left != T.nil:
            y.left.parent = x
        y.parent = x.parent  #link x's parent to y
        if x.parent == T.nil:
            T.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x           #put x on y's left
        x.parent = y

    def right_rotate(self, T, x):
        y = x.left
        x.left = y.right
        if y.right != T.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == T.nil:
            T.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def RBInsert(self, T, z):
        z.left = z.right = z.parent = T.nil

        y = T.nil
        x = T.root
        while x != T.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == T.nil:
            T.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = T.nil
        z.right = T.nil
        z.color = 'red'
        self.RBInsert_fixup(T, z)

    def RBInsert_fixup(self, T, z):
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = 'black'                #case 1
                    y.color = 'black'                       #case 1
                    z.parent.parent.color = 'red'           #case 1
                    z = z.parent.parent                     #case 1
                else:
                    if z == z.parent.right:
                        z = z.parent                        #case 2
                        self.left_rotate(T, z)              #case 2
                    z.parent.color = 'black'                #case 3
                    z.parent.parent.color = 'red'           #case 3
                    self.right_rotate(T, z.parent.parent)   #case 3
            else: #same as then clause with 'right' and 'left' exchange
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(T, z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(T, z.parent.parent)
        T.root.color = 'black'

    def transplant(self, T, u, v):
        if u.parent == T.nil:
            T.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def RBDelete_fixup(self, T, x):
        while x != T.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'                   #case 1
                    x.parent.color = 'red'              #case 1
                    self.left_rotate(T, x.parent)       #case 1
                    w = x.parent.right                  #case 1
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color == 'red'                    #case 2
                    x = x.parent                        #case 2
                else:
                    if w.right.color == 'black':
                        w.left.color == 'black'         #case 3
                        w.color = 'red'                 #case 3
                        self.right_rotate(T, x)         #case 3
                    w.color = x.parent.color            #case 4
                    x.parent.color = 'black'            #case 4
                    w.right.color = 'black'             #case 4
                    self.left_rotate(T, x.parent)       #case 4
                    x = T.root                          #case 4
            else:  #same as then clause with 'right' and 'left' exchanged
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(T, x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(T, w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(T, x.parent)
                    x = T.root
        x.color = 'black'

    def RBDelete(self, T, z):
        y = z
        y_original_color = y.color
        if z.left == T.nil:
            x = z.right
            self.transplant(T, z, z.right)
        elif z.right == T.nil:
            x = z.left
            self.transplant(T, z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(T, y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(T, z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'black':
            self.RBDelete_fixup(T, x)
                    
    def tree_minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def tree_maximum(self, x):
        while x.right != self.nil:
            x = x.right
        return x

    def tree_successor(self, x):
        if x.right != self.nil:
            return self.tree_minimum(x.right)
        y = x.parent
        while y != self.nil and x == y.right:
            x = y
            y = y.parent
        return y

    def tree_predecessor(self, x):
        if x.left != self.nil:
            return self.tree_maximum(x.left)
        y = x.parent
        while y != self.nil and x == y.left:
            x = y
            y = y.parent
        return y
    
    def iterative_tree_search(self, x, k):
        while x != self.nil:
            if k == x.key:
                return x
            elif k < x.key:
                x = x.left
            else:
                x = x.right
        return None

    def tree_depth(self, T) -> int:
        if T is None:
            return 0
        return max(self.tree_depth(T.left), self.tree_depth(T.right))+1

def test():
    nodes = [11,2,14,1,7,15,5,8,4]
    T = RBTree()
    #x = Function()
    for node in nodes:
        T.RBInsert(T, RBTree_node(node))

    T.inorder_tree_walk(T.root)
    h = T.tree_depth(T.root)
    print("The height of RB tree is:", h-1)

    #search node's key if it in the RB tree
    value = 7
    y = T.iterative_tree_search(T.root, value)
    if y != None:
        print(y.key, "is in the tree")
    else:
        print(value, "is not in the tree")

    #find node's predecessor
    if y != None:
        temp = T.tree_predecessor(y)
        print("The predecessor of", y.key, "is", temp.key)
        temp = T.tree_successor(y)
        print("The successor of", y.key, "is", temp.key)

    #insert new key to RB tree
    T.RBInsert(T, RBTree_node(10))
    print("After insert node:")
    T.inorder_tree_walk(T.root)

    #delete node
    delete = 14
    T.RBDelete(T, T.iterative_tree_search(T.root, delete))
    print("After delete node:")
    T.inorder_tree_walk(T.root)

if __name__ == '__main__':
    test()
    
