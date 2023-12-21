import random
import copy


class Node:

    def __init__(self, id, message, isByzantine):
        self.id = id
        self.message = message
        self.bi = set()
        self.isByzantine = isByzantine

    def __str__(self):
        if (self.isByzantine):
            return "| Node " + str(self.id + 1) + " | Byzantine  |"
        else:
            return "| Node " + str(self.id + 1) + " | Honest     |"

    def handleMessages(self, round):
        new_messages = []
        for message in self.message:
            print("   Message:", message, end="")
            temp_message = copy.deepcopy(message)
            if (len(message) == round+1):
                go = True
                for k in range(1, len(message)):
                    if (message[k] == self.id):
                        go = False
                if (go == True):
                    print(" --> Valid message")
                    temp_message.append(self.id)
                    self.bi.add(message[0])
                    if (self.isByzantine == False):
                        new_messages.append(temp_message)
                else:
                    print(" --> Wrong message")
            else:
                print(" --> Wrong message")
        return (new_messages)


def displayNodes(nodes):
    print("\n-----------------------")
    for node in nodes:
        print(node)
    print("-----------------------\n")


if __name__ == '__main__':

    # Initialisation

    auto = input("Auto initialisation ? (Y/n)")

    if auto == "n":
        # Manual initialisation
        print("")
        n = int(input("Number of nodes: "))
        print("")
        byzantine_nodes = int(input("Number of Byzantine nodes: "))
        print("")
        leader_value = int(input("Leader value: "))
    else:
        # Auto initialisation
        n = 8
        byzantine_nodes = 4
        leader_value = 8

    actual_byzantine_nodes = 0

    nodes = []

    print("\n\n\n------------- Initialisation -------------")

    probability = int(n / byzantine_nodes)

    for i in range(n):
        if actual_byzantine_nodes < byzantine_nodes:
            if random.randrange(0, probability) == 1:
                nodes.append(Node(i, [], True))
                actual_byzantine_nodes += 1
            else:
                nodes.append(Node(i, [], False))
        else:
            nodes.append(Node(i, [], False))

    print("\n\n")

    displayNodes(nodes)

    # Leader sending his value to all nodes (leader is node 0)

    for node in nodes:
        if node.id != 0:
            if nodes[0].isByzantine == True:
                # Leader is Byzantine, he sends random values to all nodes
                node.message.append([random.randrange(0, 2), 0])
            else:
                # Leader is not Byzantine, he sends his unique value to all nodes
                node.message.append([leader_value, 0])

    # Nodes sending their values to all nodes

    for i in range(1, byzantine_nodes + 2):
        all_messages = []
        print("\n\n\n----------------- Round " + str(i) + " -----------------")

        # Get all messages from all nodes

        for j in range(1, len(nodes)):
            print("\nChecking messages for Node " + str(nodes[j].id))
            new_node_messages = nodes[j].handleMessages(i)
            print("   [New Node message length : " +
                  str(len(new_node_messages)) + "]")
            for message in new_node_messages:
                all_messages.append(message)
            new_node_messages.clear()
            nodes[j].message.clear()

        # Send all messages to all nodes

        for message in all_messages:
            for j in range(1, len(nodes)):
                if (j != message[len(message)-1]):
                    nodes[j].message.append(message)

    print("\n")

    displayNodes(nodes)

    # Check if the value is valid

    valid = True
    for node in nodes:
        print("Node " + str(node.id) + " has " +
              str(len(node.bi)) + " values in Bi.")
        if (node.id != 0):
            if (len(node.bi) != 1):
                valid = False

    if (valid == True):
        print("\nThe value is " + str(nodes[1].bi) + " and it is valid.")
    else:
        print("\nThe value is not valid.")

    print("\n")
