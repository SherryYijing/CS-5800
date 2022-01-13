import re
MAXHASH = 2500

class Node:
    def __init__(self, k, val):
        self.next = None
        self.key = k
        self.value = val

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        newNode = Node(key, value)
        newNode.next = self.head
        self.head = newNode
        self.size += 1

    def remove(self, key):
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size-1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size-1
                return True
            prev = cur
            cur = cur.next
        return False

    def search(self, key):
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def iter(self):
        if not self.head:
            return
        cur = self.head
        print(cur.key, ":", cur.value)
        while cur.next:
            cur = cur.next
            print(cur.key, ":", cur.value)        
        
def hashFunction(key):
    hash_num = 0
    for i in key:
        hash_num += ord(i)
    return hash_num

class HashMap:
    def __init__(self, capacity, function):
        self.buckets = []
        for i in range(capacity):
            self.buckets.append(LinkedList())
        #capacity = the total number of buckets to be crrated in the hash table
        self.maxhash = capacity
        #function = the hash function to use for hashing
        self.hash_function = function
        self.size = 0

    #empties the hash table
    def clear(self):
        self.buckets = []
        for i in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    #update the given key, value in the hash table
    def insert(self, key, value):
        hash_num = self.hash_function(key)
        index = hash_num % self.maxhash
        bucket = self.buckets[index]
        node = bucket.search(key) #check the bucket by key
        if node is not None: #already exist, then update
            node.value = value
            return
        else: #not exist, then add value
            self.buckets[index].add_front(key, value)
            self.size += 1

    #remove and free with given key
    def delete(self, key):
        hash_num = self.hash_function(key)
        index = hash_num % self.maxhash
        bucket = self.buckets[index]
        node = bucket.search(key) #check the bucket by key
        if node is not None: #already exist, then delete
            bucket.remove(key)
            self.size -= 1

    #search a key exists
    def find(self, key):
        hash_num = self.hash_function(key)
        index = hash_num % self.maxhash
        bucket = self.buckets[index]
        node = bucket.search(key) #check the bucket by key
        if node is not None:
            return True
        else:
            return False

    #return the value
    def get(self, key):
        hash_num = self.hash_function(key)
        index = hash_num % self.maxhash
        bucket = self.buckets[index]
        node = bucket.search(key) #check the bucket by key
        if node is not None:
            return node.value
        else:
            return False

    #get how many empty buckets in the table
    def empty_buckets(self):
        num = 0
        for buckets in self.buckets:
            if buckets.head is None:
                num += 1
        return num

    def print_hash(self):
        for i in self.buckets:
            if i.size != 0:
                i.iter()

def test_file(file):
    hash_map = HashMap(MAXHASH, hashFunction)
    rgx = re.compile("(\w[\w']*\w|\w)")
    list_all_keys = set()
    with open(file) as f:
        for line in f:
            words = rgx.findall(line)
            for word in words:
                word = word.lower() #covert to lowercase
                list_all_keys.add(word)
                word_count = hash_map.get(word)
                if word_count is None:
                    hash_map.insert(word, 1)
                else:
                    hash_map.insert(word, word_count+1)
    f.close()

    with open('keys.txt', 'w') as f:
        for word in list_all_keys:
            value = hash_map.get(word)
            f.write(word)
            f.write(":")
            f.write(str(value))
            f.write('\n')
    f.close()

def test():
    hash_map = HashMap(MAXHASH, hashFunction)
    rgx = re.compile("(\w[\w']*\w|\w)")
    line = 'Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do. Once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, "and what is the use of a book," thought Alice, "without pictures or conversations?"'
    words = words = rgx.findall(line)
    #insert key
    for word in words:
        word = word.lower() #covert to lowercase
        #list_all_keys.add(word)
        word_count = hash_map.get(word)
        if word_count is None:
            hash_map.insert(word, 1)
        else:
            hash_map.insert(word, word_count+1)
    hash_map.print_hash()

    #delete key
    hash_map.delete('conversations')
    print("After delete:")
    hash_map.print_hash()

    #find key
    result = hash_map.find('on')
    print(result)

if __name__ == '__main__':
    #test_file('alice_in_wonderland.txt')
    test()


    
