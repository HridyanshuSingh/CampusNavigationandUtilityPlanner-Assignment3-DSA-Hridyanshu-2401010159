import heapq

# ---------------------------
# Building
# ---------------------------
class Building:
    def __init__(self, id, name, detail):
        self.id = id
        self.name = name
        self.detail = detail

    def __repr__(self):
        return f"({self.id}:{self.name})"


# ---------------------------
# BST
# ---------------------------
class BSTNode:
    def __init__(self, b):
        self.b = b
        self.l = None
        self.r = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, x):
        if self.root is None:
            self.root = BSTNode(x)
            return
        c = self.root
        while True:
            if x.id < c.b.id:
                if c.l is None:
                    c.l = BSTNode(x)
                    return
                c = c.l
            elif x.id > c.b.id:
                if c.r is None:
                    c.r = BSTNode(x)
                    return
                c = c.r
            else:
                c.b = x
                return

    def inorder(self, n, a):
        if n:
            self.inorder(n.l, a)
            a.append(n.b)
            self.inorder(n.r, a)

    def height(self, n):
        return 0 if n is None else 1 + max(self.height(n.l), self.height(n.r))


# ---------------------------
# AVL
# ---------------------------
class AVLNode:
    def __init__(self, b):
        self.b = b
        self.l = None
        self.r = None
        self.h = 1


class AVL:
    def __init__(self):
        self.root = None

    def height(self, n):
        return 0 if n is None else n.h

    def update(self, n):
        n.h = 1 + max(self.height(n.l), self.height(n.r))

    def balance(self, n):
        return self.height(n.l) - self.height(n.r)

    def rotate_right(self, y):
        x = y.l
        t = x.r
        x.r = y
        y.l = t
        self.update(y)
        self.update(x)
        return x

    def rotate_left(self, x):
        y = x.r
        t = y.l
        y.l = x
        x.r = t
        self.update(x)
        self.update(y)
        return y

    def insert_node(self, n, x):
        if n is None:
            return AVLNode(x)

        if x.id < n.b.id:
            n.l = self.insert_node(n.l, x)
        elif x.id > n.b.id:
            n.r = self.insert_node(n.r, x)
        else:
            n.b = x
            return n

        self.update(n)
        d = self.balance(n)

        # Left heavy
        if d > 1:
            if x.id < n.l.b.id:
                return self.rotate_right(n)
            n.l = self.rotate_left(n.l)
            return self.rotate_right(n)

        # Right heavy
        if d < -1:
            if x.id > n.r.b.id:
                return self.rotate_left(n)
            n.r = self.rotate_right(n.r)
            return self.rotate_left(n)

        return n

    def insert(self, x):
        self.root = self.insert_node(self.root, x)

    def inorder(self, n, a):
        if n:
            self.inorder(n.l, a)
            a.append(n.b)
            self.inorder(n.r, a)


# ---------------------------
# Graph
# ---------------------------
class Graph:
    def __init__(self):
        self.nodes = {}
        self.adj = {}

    def add(self, b):
        self.nodes[b.id] = b
        self.adj.setdefault(b.id, [])

    def edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def matrix(self):
        n = max(self.nodes.keys()) + 1
        m = [[0] * n for _ in range(n)]
        for u in self.adj:
            for v, w in self.adj[u]:
                m[u][v] = w
        return m

    def bfs(self, s):
        out = []
        q = [s]
        vis = {s}

        while q:
            u = q.pop(0)
            out.append(self.nodes[u])
            for v, w in self.adj[u]:
                if v not in vis:
                    vis.add(v)
                    q.append(v)
        return out

    def dfs(self, s):
        out = []
        st = [s]
        vis = set()

        while st:
            u = st.pop()
            if u in vis:
                continue
            vis.add(u)
            out.append(self.nodes[u])
            for v, w in self.adj[u]:
                st.append(v)
        return out

    def dijkstra(self, s):
        INF = 999999
        dist = {x: INF for x in self.nodes}
        dist[s] = 0

        pq = [(0, s)]
        while pq:
            du, u = heapq.heappop(pq)
            for v, w in self.adj[u]:
                if du + w < dist[v]:
                    dist[v] = du + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    def find(self, x, parent):
        if parent[x] != x:
            parent[x] = self.find(parent[x], parent)
        return parent[x]

    def kruskal(self):
        edges = []
        for u in self.adj:
            for v, w in self.adj[u]:
                if u < v:
                    edges.append((u, v, w))

        edges.sort(key=lambda x: x[2])

        parent = {x: x for x in self.nodes}
        rank = {x: 0 for x in self.nodes}

        mst = []

        for u, v, w in edges:
            pu = self.find(u, parent)
            pv = self.find(v, parent)
            if pu != pv:
                mst.append((u, v, w))
                if rank[pu] < rank[pv]:
                    parent[pu] = pv
                elif rank[pu] > rank[pv]:
                    parent[pv] = pu
                else:
                    parent[pv] = pu
                    rank[pu] += 1

        return mst


# ---------------------------
# Expression Tree
# ---------------------------
class ExprNode:
    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None


class ExprTree:
    def build(self, tokens):
        st = []
        for x in tokens:
            if x in "+-*/":
                r = st.pop()
                l = st.pop()
                n = ExprNode(x)
                n.l = l
                n.r = r
                st.append(n)
            else:
                st.append(ExprNode(x))
        return st.pop()

    def eval(self, n):
        if n.l is None:
            return float(n.v)
        a = self.eval(n.l)
        b = self.eval(n.r)
        if n.v == "+": return a + b
        if n.v == "-": return a - b
        if n.v == "*": return a * b
        return a / b


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    b = [
        Building(0, "Admin", "A"),
        Building(1, "Lib", "B"),
        Building(2, "CSE", "C"),
        Building(3, "DS", "D"),
        Building(4, "Hostel", "E"),
        Building(5, "Cafe", "F"),
        Building(6, "Gym", "G")
    ]

    # BST
    bst = BST()
    avl = AVL()
    for x in b:
        bst.insert(x)
        avl.insert(x)

    ino = []
    bst.inorder(bst.root, ino)
    print("BST Inorder:", ino)
    print("BST Height:", bst.height(bst.root))

    ain = []
    avl.inorder(avl.root, ain)
    print("AVL Inorder:", ain)
    print("AVL Height:", avl.height(avl.root))

    # Graph
    g = Graph()
    for x in b:
        g.add(x)
    E = [
        (0, 1, 4), (0, 2, 2), (1, 2, 1),
        (2, 3, 3), (3, 4, 2), (4, 6, 6),
        (1, 5, 7), (5, 6, 5)
    ]
    for u, v, w in E:
        g.edge(u, v, w)

    print("Adj List:", g.adj)

    m = g.matrix()
    print("Adj Matrix:")
    for row in m:
        print(row)

    print("BFS:", g.bfs(0))
    print("DFS:", g.dfs(0))
    print("Dijkstra:", g.dijkstra(0))
    print("MST:", g.kruskal())

    et = ExprTree()
    root = et.build(["3", "4", "5", "*", "6", "-", "+"])
    print("Expr Value:", et.eval(root))
