# link list node
class Node:
    def __init__(self, data):
        self.data = data # assign data
        self.next = None # initialize next as NULL
        self.head = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, newNode):
        #newNode = Node(newData) # allocate the node and put in data
        if self.head is Node:
            self.head = newNode
            return
        
        last = self.head
        while(last.next):
            last = last.next
        last.next = newNode

    def printList(self):
        temp = self.head
        while(temp):
            print(temp.data)
            temp = temp.next

def TraversalList(node):# how many nodes are in the list
    num = 0
    ptr = node
    while(ptr):
        num += 1
        ptr = ptr.next
    return num

def getIntersection(head1, head2):
    numA = TraversalList(head1)
    numB = TraversalList(head2)

    if numA > numB:
        offset = numA - numB
        return helper(offset, head1, head2)
    else:
        offset = numB - numA
        return helper(offset, head2, head1)

def helper(num, head1, head2):
    ptr1, ptr2 = head1, head2
    for i in range(num):
        if(ptr1 == None):
            return -1
        ptr1 = ptr1.next

    while(ptr1 != None and ptr2 != None):
        if ptr1 is ptr2: # check address is same
            return ptr1.data
        ptr1 = ptr1.next
        ptr2 = ptr2.next

    return -1

if __name__ == '__main__':
    intersection = Node(7) # define intersection

    # frist: 1->3->5->7->9
    listA = LinkedList()
    listA.head = Node(1)
    listA.append(Node(3))
    listA.append(Node(5))
    listA.append(intersection)
    listA.append(Node(9))
    #listA.printList()

    # second: 2->7->12
    listB = LinkedList()
    listB.head = Node(2)
    listB.append(intersection)
    listB.append(Node(12))
    #listB.printList()

    print(getIntersection(listA.head, listB.head))
