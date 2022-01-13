class Vertex:
    def __init__(self, value):
        self.data = value
        self.h = 0
        self.e = 0
        self.nextNeighbor = None
        self.next = None
        self.pre = None

def RelabelToFront(vertices, edges, start, end):
    if len(vertices) < 1 or len(edges) < 1:
        return -1

    #initialize
    maxFlow = 0
    #build adjacency list
    vertexNum = len(vertices)
    head = None
    V = []
    for i in range(vertexNum):
        vertex = Vertex(i)
        V.append(vertex)
        if i == start:
            vertex.h = vertexNum
        else:
            vertex.h = 0
        if head == None:
            head = vertex
        else:
            temp = head
            while temp.next != None:
                temp = temp.next
            temp.next = vertex
            vertex.pre = temp

    #define residual network
    adj = [([0]*vertexNum) for i in range(vertexNum)]
    edgeNum = len(edges)
    #create residual network
    for i in range(edgeNum):
        adj[edges[i][0]][edges[i][1]] = edges[i][2]
        #build adjacency list relationship
        temp = V[edges[i][0]]
        while temp.nextNeighbor != None:
            temp = temp.nextNeighbor
        temp.nextNeighbor = Vertex(edges[i][1])

        temp = V[edges[i][1]]
        while temp.nextNeighbor != None:
            temp = temp.nextNeighbor
        temp.nextNeighbor = Vertex(edges[i][0])

        if edges[i][0] == start:
            V[edges[i][1]].e = edges[i][2]
            V[edges[i][0]].e = V[edges[i][0]].e - edges[i][2]
            adj[edges[i][1]][edges[i][0]] = edges[i][2]

    print("Original matrix:")
    for i in adj:
        for j in i:
            print(j, end=' ')
        print('\n')
    #relabel to front
    u = head
    while u != None:
        #u is not source or sink
        if u.data == start or u.data == end:
            u = u.next
            continue

        height = u.h
        temp = u

        while u.e > 0:
            v = temp
            if v == None: #relabel
                V[u.data].h += 1
                temp = u
            elif adj[u.data][v.data] > 0 and (V[u.data].h == V[v.data].h + 1): #push
                delta = min(u.e, adj[u.data][v.data])
                adj[u.data][v.data] = adj[u.data][v.data] - delta
                adj[v.data][u.data] = adj[v.data][u.data] + delta
                if v.data == end:  #flow to sink
                    maxFlow += delta
                V[u.data].e = V[u.data].e - delta
                V[v.data].e = V[v.data].e + delta
            else:
                temp = temp.nextNeighbor

        if u.h > height:
            #move u to the front of list
            if u != head:
                u.pre.next = u.next
                if u.next != None:
                    u.next.pre = u.pre
                u.pre = None
                u.next = head
                head.pre = u
                head = u
        u = u.next

    print("The graph flow matrix is:")
    for i in adj:
        for j in i:
            print(j, end=' ')
        print('\n')

    return maxFlow

def test1():
    vertices = [0, 1, 2, 3, 4]
    edges = [[0,1,12],[0,2,14],[1,2,5],[1,4,16],[2,3,8],[3,4,10],[3,1,7]]
    start, end = 0, 4
    maxFlow = RelabelToFront(vertices, edges, start, end)
    print("The max flow is:", maxFlow)

def test2():
    vertices=[0,1,2,3,4,5]
    edges=[[0,1,16],[0,2,13],[1,3,12],[2,1,4],[2,4,14],[3,2,9],[3,5,20],[4,3,7],[4,5,4]]
    start, end = 0, 5
    maxFlow = RelabelToFront(vertices, edges, start, end)
    print("The max flow is:", maxFlow)

def test3():
    vertices=[0,1,2,3,4,5]
    edges=[[0,1,10],[0,2,10],[1,2,2],[1,3,4],[1,4,8],[2,4,9],[4,3,6],[3,5,10],[4,5,10]]
    start, end = 0, 5
    maxFlow = RelabelToFront(vertices, edges, start, end)
    print("The max flow is:", maxFlow)

def test4():
    vertices=[0,1,2,3,4]
    edges=[[0,1,12],[0,2,14],[1,2,5],[1,4,16],[2,3,8],[3,1,7],[3,4,10]]
    start, end = 0, 4
    maxFlow = RelabelToFront(vertices, edges, start, end)
    print("The max flow is:", maxFlow)
    
if __name__ == '__main__':
    test1()
        
    
