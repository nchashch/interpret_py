class Node(object):
    def __init__(self):
        self.data = None # contains the data
        self.next = None # contains the reference to the next node


class LinkedList:
    def __init__(self):
        self.cur_node = None

    def push(self, data):
        new_node = Node()
        new_node.data = data
        new_node.next = self.cur_node # link the new node to the 'previous' node.
        self.cur_node = new_node #  set the current node to the new one.

    def peek(self):
        if self.cur_node:
            return self.cur_node.data
        else:
            return None

    def get(self, index):
        current_node = self.cur_node
        i = 0
        while current_node and i < index:
            current_node = current_node.next
            i += 1
        if not current_node or i != index:
            return None
        return current_node.data

    def delete(self, index):
        if index == 0:
            data = self.cur_node.data
            self.cur_node = self.cur_node.next
            return data
        prev = None
        current_node = self.cur_node
        i = 0
        while current_node and i < index:
            prev = current_node
            current_node = current_node.next
            i += 1
        if not current_node or i != index:
            return None
        prev.next = current_node.next
        data = current_node.data
        del current_node
        return data

    def __repr__(self):
        node = self.cur_node # cant point to ll!
        result = '['
        while node:
            result += str(node.data) + ', '
            node = node.next
        result += ']'
        return result

def main():
    ll = LinkedList()
    ll.push(10)
    ll.push(20)
    ll.push(30)
    print(ll)
    print(ll.delete(0))
    print(ll)

if __name__ == '__main__':
    main()
