class Node:
        def __init__(self, k=None):
            self.p = None
            self.key = k
            self.degree = 0
            self.child = None
            self.sibling = None

class binomialHeap:
    def __init__(self, head=None):
        self.head = head

    def make_heap(self):
        heap = binomialHeap()
        return heap

    def minimum(self):
        y = None
        x = self.head
        mini = float('inf')
        while x != None:
            if x.key < mini:
                mini = x.key
                y = x
            x = x.sibling
        return y
    
    def link(self,y, z):
        y.p = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def heap_merge(self, h1, h2):
        node = None
        p = None
        p1 = h1.head
        p2 = h2.head

        if p1 is None:
            return h2.head
        if p2 is None:
            return h1.head

        if p1.degree < p2.degree:
            p = p1
            p1 = p1.sibling
        else:
            p = p2
            p2 = p2.sibling
        node = p

        while p1 and p2:
            if p1.degree < p2.degree:
                p.sibling = p1
                p1 = p1.sibling
            else:
                p.sibling = p2
                p2 = p2.sibling
            p = p.sibling

        if p2:
            p.sibling = p2
        else:
            p.sibling = p1
        return node

    def union(self, h1, h2):
        h = self.make_heap()
        h.head = self.heap_merge(h1, h2)
        #free the object h1 and h2 but not the lists they point to
        del h1
        del h2
        
        if h.head is None:
            return h

        prev_x = None
        x = h.head
        next_x = x.sibling

        while next_x is not None:
            if (x.degree != next_x.degree) or (next_x.sibling is not None and next_x.sibling.degree == x.degree):
                prev_x = x                      #case 1 and 2
                x = next_x                      #case 1 and 2
            elif x.key <= next_x.key:
                x.sibling = next_x.sibling      #case 3
                h.link(next_x, x)               #case 3
            else:
                if prev_x is None:
                    h.head = next_x             #case 4
                else:
                    prev_x.sibling = next_x     #case 4
                h.link(x, next_x)               #case 4
            next_x = x.sibling                  #case 4
        return h

    def heap_insert(self, x):
        h = self.make_heap()
        x.p = None
        x.child = None
        x.sibling = None
        x.degree = 0
        h.head = x
        heap = self.union(self, h)
        return heap

    def insert(self, key):
        return self.heap_insert(Node(key))

    def extract_min(self):
        #find the root x with the minimum key in the root list of heap
        p = self.head
        x = None
        p_prev, x_prev = None, None

        if p is None:
            return p
        x = p
        mini = p.key
        p_prev = p
        p = p.sibling
        while p is not None:
            if p.key < mini:
                x_prev = p_prev
                x = p
                mini = p.key
            p_prev = p
            p = p.sibling
        if x == self.head:
            self.head = x.sibling
        elif x.sibling is None:
            x_prev.sibling = None
        else:
            x_prev.sibling = x.sibling
        child_x = x.child

        #if the minimum node has no child
        if child_x is not None:
            """if the node has subtree, then insert them into a new heap,
                and union this new heap with old"""     
            h = self.make_heap()
            child_x.p = None
            h.head = child_x
            p = child_x.sibling
            child_x.sibling = None
            while p is not None:
                p_prev = p
                p = p.sibling
                p_prev.sibling = h.head
                h.head = p_prev
                p_prev.p = None
            self = self.union(self, h)
        return self

    def decrease_key(self, x, k):
        if k > x.key:
            print("new key is greater than current key")
            return

        x.key = k
        y = x
        z = y.p

        while z is not None and y.key < z.key:
            #do exchange
            #if y and z have satellite fields, exchange them, too
            y.key = z.key
            z.key = k
            y = z
            z = y.p

    def search(self, k):
        x = self.head
        while x is not None:
            if x.key == k:
                return x
            else:
                if x.key < k and x.child is not None:
                    x = x.child
                elif x.key > k or x.child is None:
                    while x.sibling is None:
                        x = x.p
                        if x is None:
                            return None
                    x = x.sibling
        return None

    def delete(self, x):
        self.decrease_key(x, -float('inf'))
        return self.extract_min()

def test():
    print("Binomial Heap test:\n")
    #1. make heap test
    print("1. make heap test")
    heap = binomialHeap().make_heap()
    if heap:
        print("make heap successfully\n")

    #2. insert test
    print("2. insert test")
    heap = heap.insert(5)
    heap = heap.insert(8)
    heap = heap.insert(2)
    heap = heap.insert(7)
    heap = heap.insert(6)
    heap = heap.insert(9)
    heap = heap.insert(4)
    if heap.head is not None:
        print("insert to heap successfully\n")

    #3. search key test
    print("3. search key test")
    key = 2
    print("find key", key)
    node = heap.search(key)
    if node is not None:
        print(node.key, "is in the binomial heap")
        print("search key successfully\n")
    else:
        print("Cannot find the key", key, "\n")

    #4. minimum key test
    print("4. minimum key test")
    print("The minimum:", heap.minimum().key)
    print("minimum key successfully\n")

    #5. extract-min test
    print("5. extract-min test")
    heap = heap.extract_min()
    print("After extract-min, the minimum:", heap.minimum().key)
    node = heap.search(key)
    if node is None:
        print("After extract-min, the old minimum", key, "is not in the heap")
        print("exctract-min successfully\n")

    #6. decrease key test
    print("6. decrease key test")
    key = 9
    decrease = 2
    print("we are going to decrease the key", key, "to", decrease)
    node = heap.search(key)
    #make sure the key we want to decrease exist
    if node is not None:
        print(node.key, "is in the binomial heap")
        heap.decrease_key(node, decrease)
    else:
        print("Cannot find the key", key)
    #check the update value exist
    node1 = heap.search(key)
    node2 = heap.search(decrease)
    if node1 is None and node2 is not None:
        print("after decrease key,", node2.key, "is in the binomial heap and", key, "is not in the binomial heap")
        print("decrease key successfully\n")
    else:
        print("decrease key is not successfully\n")  

    #7. delete key test
    print("7. delete key test")
    print("before delete:")
    delete = 7
    node = heap.search(delete)
    if node is not None:
        print(delete, "is in the binomial heap")
        heap.delete(node)
    else:
        print(delete, "is not in the binomial heap")
    print("after delete:")
    node = heap.search(delete)
    if node is None:
        print(delete, "is not in the binomial heap")
        print("delete successfully\n")
    else:
        print("delete is not successfully\n")

if __name__ == '__main__':
    test()
    
    
