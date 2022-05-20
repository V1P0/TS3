import random
from time import sleep


class Node:
    def __init__(self, name, pos, start):
        self.name = name
        self.pos = pos
        self.collisions = 0
        self.wait_time = start
        self.sending = False
        self.collision_detected = False

    def wait(self, length):
        self.collisions += 1
        self.wait_time = random.randrange(0, 2 ** min(self.collisions, 10))*length

    def get_state(self):
        if self.sending:
            return "Collided" if self.collision_detected else "Active"
        else:
            return "Waiting"


class Message:
    def __init__(self, node: Node, direction: int):
        self.node = node
        self.direction = direction
        self.jam_signal = node.collision_detected

    def __str__(self):
        if self.jam_signal:
            return "#"
        else:
            return self.node.name


class Wire:
    def __init__(self, length: int):
        self.nodes = {i: None for i in range(length)}
        self.length = length
        self.messages = [[] for _ in range(length)]
        self.iter = 0

    def add_node(self, name, pos: int, start: int):
        self.nodes[pos] = Node(name, pos, start)

    def next(self):
        self.iter += 1
        next_frame = [[] for _ in range(self.length)]
        for i, segment in enumerate(self.messages):
            for message in segment:
                if message.direction == -1:
                    if i > 0:
                        next_frame[i - 1].append(message)
                elif message.direction == 1:
                    if i < self.length - 1:
                        next_frame[i + 1].append(message)
                else:
                    if i > 0:
                        next_frame[i - 1].append(Message(message.node, -1))
                    if i < self.length - 1:
                        next_frame[i + 1].append(Message(message.node, 1))
        self.messages = next_frame
        for node in self.nodes.values():
            if node is None:
                continue
            if not node.sending:
                if node.wait_time == 0:
                    if not self.messages[node.pos]:
                        node.sending = True
                        self.messages[node.pos].append(Message(node, 0))
                        node.wait_time = 2 * self.length
                else:
                    node.wait_time -= 1
            else:
                if node.wait_time == 0:
                    node.sending = False
                    if node.collision_detected:
                        node.collision_detected = False
                        node.wait(self.length * 2)
                    else:
                        node.collisions = 0
                else:
                    if (not node.collision_detected) and len(self.messages[node.pos]) > 0:
                        node.collision_detected = True
                        node.wait_time = 2 * self.length
                    self.messages[node.pos].append(Message(node, 0))
                    node.wait_time -= 1

    def __str__(self):
        full_message = ' |'
        for i in range(self.length):
            message_val = ''
            for message in self.messages[i]:
                message_val += str(message)
            for _ in range(3 - len(message_val)):
                message_val += ' '
            message_val += '|'
            full_message += message_val
        full_message += ' states> '
        for node in self.nodes.values():
            if node is None:
                continue
            full_message += f'{node.name}: {node.get_state()}[{node.wait_time}], '
        return full_message


if __name__ == "__main__":
    wire = Wire(15)
    wire.add_node("A", 0, 0)
    wire.add_node("B", 5, 10)
    wire.add_node("C", 14, 30)
    with open('history.txt', 'w') as f:
        while True:
            wire.next()
            print('\r' + str(wire), end='')
            f.write(str(wire) + '\n')
            sleep(0.1)
