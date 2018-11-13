

import time


class Node(object):

    def __init__(self, value):
        self.value = value
        self.next_node = None
        self.time = time.time()

    def set_next_node(self, node):
        self.next_node = node


# 链表
class LinkedList(object):

    def __init__(self, *args, **kwargs):
        self.head = None
        self.index = -1
        # 传参是否为空
        if args:
            for i in range(len(*args)):
                if i == 0:
                    self.head = Node(args[i])
                    self.index += 1
                else:
                    current_node = Node(args[i])
                    self.head.set_next_node(current_node)
                    self.index += 1
                    self.head = current_node

    def append(self, value):
        # 给最后一个元素建立握手
        end_self = self.find_end()
        # add_link = LinkedList(value)
        add_link = Node(value)
        end_self.set_next_node(add_link)

    def insert(self, value, index):
        pass

    def delete(self, index):
        pass

    def size(self):

        return self.index + 1

    def remove(self, value):
        pass

    def index(self, value):
        pass

    def find_end(self):
        # 获取最后一个元素
        head = self.head
        while True:
            if not head.next_node:
                return head
            head = head.next_node

    def ergodic(self):
        while True:
            print(self.head.value)
            self.head = self.head.next_node
            if not self.head:
                return ''


    def __repr__(self):
        # 遍历
        while True:
            print(self.head.value)
            self.head = self.head.next_node
            if not self.head:
                return ''


a1 = LinkedList()

# a1.append('2')

# a1.append('3')
# print(a1.value)
# a1.append('4')
print(a1.size())








# 堆栈
class Stack(object):

    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = []
        self.top = -1

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

