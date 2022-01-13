import random
#random number has biggest limitation
maxLevel = 16
#random level, select random number between 1 to maxRand
randLevel = random.randint(1, maxLevel)

class SkipNode:
    def __init__(self, val):
        self.value = val
        self.right = None
        self.down = None

class SkipList:
    def __init__(self):
        #initialize header and sentinel to infinity
        header = [SkipNode(-float('inf')) for i in range(maxLevel)]
        sentinel = [SkipNode(float('inf')) for i in range(maxLevel)]

        #connect them together
        for i in range(maxLevel - 1):
            header[i].right = sentinel[i]
            header[i].down = header[i+1]
            sentinel[i].down = sentinel[i+1]
        #the last layer of header don't have "down" option
        header[-1].right = sentinel[-1]
        #skiplist initial pointer is header's first element
        self.head = header[0]

    #search begin with initial pointer
    def search(self, target:int) -> bool:
        node = self.head
        while node:
            if node.right.value > target:
                node = node.down
            elif node.right.value < target:
                node = node.right
            else:
                return True
        return False

    def add(self, num:int) -> None:
        #use prev array to store skpilist pointer before jump down
        prev = []
        node = self.head
        while node:
            if node.right.value >= num:
                prev.append(node)
                node = node.down
            else:
                node = node.right

        #arr is the array of pointer to be inserted, randomly in length
        arr = [SkipNode(num) for i in range(randLevel)]
        temp = SkipNode(None)
        for i,j in zip(prev[maxLevel - len(arr):], arr):
            j.right = i.right
            i.right = j
            temp.down = j
            temp = j

    def earse(self, num:int) -> bool:
        ans = False
        node = self.head
        while node:
            if node.right.value > num:
                node = node.down
            elif node.right.value < num:
                node = node.right
            else:
                ans = True
                node.right = node.right.right
                node = node.down
        return ans

def test():
    sl = SkipList()
    sl.add(20)
    sl.add(40)
    sl.add(10)
    sl.add(20)
    sl.add(5)
    sl.add(80)
    sl.earse(20)
    sl.add(100)
    sl.add(20)
    sl.add(30)
    sl.earse(5)
    sl.add(50)
    print(sl.search(80))
    sl.earse(10)
    print(sl.search(10))
    
if __name__ == '__main__':
    test()
