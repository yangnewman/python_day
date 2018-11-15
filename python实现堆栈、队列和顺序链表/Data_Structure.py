

class Node(object):

    def __init__(self, value):
        self.value = value
        self.next_node = None

    def set_next_node(self, node):
        self.next_node = node

# 顺序链表
class LinkedList(object):

    def __init__(self, *args, **kwargs):
        self.head = None
        self.index = -1
        self.node = None
        # 传参是否为空
        if args:
            # head01 = self.head
            for i in range(len(args)):
                if i == 0:
                    self.head = Node(args[i])
                    self.index += 1
                    self.node = self.head
                else:
                    current_node = Node(args[i])
                    self.node.set_next_node(current_node)
                    self.index += 1
                    self.node = current_node
        self.size = self.index + 1

    def append(self, value):
        # 给最后一个元素建立握手
        end_self = self.find_end()

        # 表为空时d
        if not end_self:
            self.head = Node(value)
            self.index += 1
            self.node = self.head
        else:
            # add_link = LinkedList(value)
            add_link = Node(value)
            end_self.set_next_node(add_link)
            self.index += 1
        self.size = self.index + 1

    def insert(self, value, position):
        if isinstance(position, int):
            insert_obj = self.head
            # 当表为空时插入头
            if not self.head:
                self.head = Node(value)
                self.node = self.head
            # 当表不为空
            # 当下标左越界时插入第一个
            elif position <= 0:
                ins_node = Node(value)
                ins_node.next_node = insert_obj
                self.head = ins_node

            # 当下标右越界时插入最后
            elif position > self.index:
                node_end = self.find_end()
                node_end.set_next_node(Node(value))

            # 当下标等于界值时
            elif position == self.index:
                n_node = Node(value)
                u_node = self.find_current(position-1)
                c_node = self.find_current(position)
                u_node.next_node = n_node
                n_node.next_node = c_node

            # 当下标在中间时
            elif 0 < position < self.index:
                now_node = Node(value)
                up_node = self.find_current(position-1)
                node_current = self.find_current(position)
                up_node.next_node = now_node
                now_node.next_node = node_current
            self.index += 1
            self.size = self.index + 1
        else:
            return "下标参数不是int"

    def delete(self, position):
        current_obj = self.head
        if not current_obj:
            print("表已为空，不能删除")
            return
        if isinstance(position, int):
            len_list = self.index + 1
            if position < 0 :
                print("delete方法下标不能为负")
                return

            elif position == 0:
                self.head = self.head.next_node
                self.index -= 1
                self.size = self.index + 1
                return

            # 当下标无越界，就前一个节点链接到后一个节点
            elif self.index > position > 0 :
                current_node = self.find_current(position)
                previous_node = self.find_current(position-1)

                previous_node.next_node = current_node.next_node
                # current_node = None
                self.index -= 1
                self.size = self.index + 1
                pass

            # 当下标等于右边界，删除最后一个，就将倒数第二个节点断开与最后一个的链接
            elif position == self.index:
                previous_node = self.find_current(position-1)
                # print(node.value)
                previous_node.next_node = None
                self.index -= 1
                self.size = self.index + 1

            # 当右越界时
            elif position > self.index:
                pos = self.index
                node = self.find_current(pos-1)
                # print(node.value)
                node.next_node = None
                self.index -= 1
                self.size = self.index + 1
        else:
            print ('您输入的position不是int类型')
            return

    def remove(self, value):
        remove_obj = self.head
        if not remove_obj:
            print("表已为空，不能删除")
            return
        index01 = self.get_index(value)
        if isinstance(index01, int):
            self.delete(index01)

    def get_index(self, value):
        """
        当值为第一个时返回0
        当值为中间值时 返回对应下标
        当值为第最后时返回self.index
        当值不在其中抛出异常
        """
        flag = 0
        first_node = self.head
        for _ in range(self.size):
            if first_node.value == value:
                return flag
            first_node = first_node.next_node
            flag += 1

        if flag == self.size:
            print('value不在表中')
            return

    def get_value(self, position):
        """
        通过下标获取值
        :param position:
        :return:
        """
        get_value_node = self.head
        if not get_value_node:
            print("表为空，value不在表中")
            return
        if isinstance(position, int):
            # 当下标右越界时，返回最后一个
            if position >= self.index:
                f_node = self.find_end()
                print(f_node.value)
                return f_node.value
            # 当下标左越界时，返回第一个
            elif position <= 0:
                print(get_value_node.value)
                return get_value_node.value
            # 当下标处于中间时
            elif 0 < position < self.index:
                for m in range(position):
                    get_value_node = get_value_node.next_node
                print(get_value_node.value)
                return get_value_node.value
        else:
            print ('您输入的position不是int类型')
            return

    def find_current(self, position):
        """
        获取当前要选择的元素
        :return: 
        """
        current_head = self.head
        # 当下标为0时
        if not position:
            return current_head
        for j in range(position):
            # 当下一个节点不为空时获取下一个节点
            if current_head.next_node:
                current_head = current_head.next_node

        return current_head

    def find_end(self):
        """
        获取最后一个元素
        :return: 
        """
        head = self.head
        # 当表为空时
        if not head:
            return head
        # 当表不为空时
        while True:
            if not head.next_node:
                return head
            head = head.next_node

    def __repr__(self):
        # 遍历
        if not self.head:
            return '[]'
        a = '['
        b = ']'
        # heads = self.head
        while True:
            a += str(self.head.value)
            # print(self.head.value)
            self.head = self.head.next_node
            if not self.head:
                a += b
                return a
            a += ', '

# a1 = LinkedList('www', 'eee', 'rrr', 'uuu', 'dss')
a1 = LinkedList()
# print(a1.index)
# print(a1.size)
# a1.get_value(7)
# a1.remove('o')
# a1.delete(0)
a1.insert(111, 0)
a1.insert(2333, 0)
# a1.delete(4)
a1.insert('sss', 4)
a1.insert('ssa', 4)
# a1.find_current(1)
# a1.get_index('eee')
# print(a1.get_index('qwe'))
print(a1)
print(a1.size)


# 堆栈 先进后出
class Stack(object):

    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = []
        self.top = -1

    def push(self, item):
        if self.full():
            raise ('stack is full')
        else:
            self.stack.append(item)
            self.top += 1

    def pop(self):
        if self.empty():
            raise ('stack is empty')
        else:
            self.stack.pop()
            self.top -= 1

    def index(self, item):
        return self.stack.index(item)

    def empty(self):
        return self.top == -1

    def full(self):
        return self.top + 1 == self.max_size

    def size(self):
        self.max_size = len(self.stack)

    def show_stack(self):
        print(self.stack)

    def get(self, index):
        return self.stack[index]


# 队列 先进先出
class Queue(object):

    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []
        self.top = -1

    def push(self, item):
        if self.full():
            raise ('queue is full')
        else:
            self.queue.insert(0, item)
            self.top += 1

    def pop(self):
        if self.empty():
            raise ('queue is empty')
        else:
            self.queue.pop()
            self.top -= 1

    def index(self, item):
        return self.queue.index(item)

    def empty(self):
        return self.top == -1

    def full(self):
        return self.top + 1 == self.max_size

    def size(self):
        self.max_size = len(self.queue)

    def show_queue(self):
        print(self.queue)

    def get(self, index):
        return self.queue[index]

