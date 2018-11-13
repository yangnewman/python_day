class Stack:

    def __init__(self, max_size):
        self.max_size = max_size

    def push(self, item):
        pass

    def pop(self):
        pass

    def index(self, item):
        pass

    def empty(self):
        pass

    def full(self):
        pass

    def size(self):
        pass

    def get(self, index):
        pass


class Node:

    def __init__(self, value):
        self.value = value
        self.next_node = None

    def set_next_node(self, node):
        self.next_node = node


#链表
class LinkedList:

    def __init__(self, value):
        self.head = None

    def append(self, value):
        pass

    def insert(self, value, index):
        pass

    def delete(self, index):
        pass

    def size(self):
        pass

    def remove(self, value):
        pass

    def index(self, value):
        pass

    def __repr__(self):
        pass



node1 = Node('carmack')
node2 = Node('jon')
node3 = Node('lisa')

head = node1
node1.set_next_node(node2)
node2.set_next_node(node3)

# while(head.next_node):
#     print(head.value)
#     head = head.next_node

while (True):
    print(head.value)
    if not head.next_node:
        break
    head = head.next_node


l = LinkedList()
l.append(4)
l.append(8)
l.append(9)
print(l)