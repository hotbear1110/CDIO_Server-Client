#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import camera
import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, path=None):
    G = nx.Graph()

    for node in graph.nodes.values():
        for neighbor, cost in node.neighbors.items():
            G.add_edge((node.x, node.y), (neighbor.x, neighbor.y), weight=cost)

    pos = {(node.x, node.y): (node.x, node.y) for node in graph.nodes.values()}
    edge_labels = {((node.x, node.y), (neighbor.x, neighbor.y)): cost for node in graph.nodes.values() for
                   neighbor, cost in node.neighbors.items()}

    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path is not None:
        print('Path in draw_graph:', path)
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

    plt.show()


# This is the Publisher

"""
client = mqtt.Client("publisher")
client.connect("192.168.5.34",1883,60)
client.publish("topic/motor-A/dt", 100)
time.sleep(1)
client.publish("topic/motor-A/dt", 0)
time.sleep(1)

client.publish("topic/motor-A/dt", 100)
time.sleep(1)
client.publish("topic/motor-A/dt", 0)
time.sleep(1)
client.disconnect()
"""

robot = camera.grid.getMidpoint([(0, 0), (0, 0)])


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = {}

    def add_neighbor(self, node, cost):
        self.neighbors[node] = cost

    def __str__(self):
        return f'Node({self.x}, {self.y})'


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, x, y):
        node = Node(x, y)
        self.nodes[(x, y)] = node
        return node

    def add_edge(self, point1, point2):
        if point1 not in self.nodes:
            self.add_node(*point1)
        if point2 not in self.nodes:
            self.add_node(*point2)

        # Calculate the Euclidean distance between the two points
        cost = round(math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2), 2)

        self.nodes[point1].add_neighbor(self.nodes[point2], cost)
        self.nodes[point2].add_neighbor(self.nodes[point1], cost)

    def update_edges(self, current_goal):
        for node in self.nodes.values():
            self.add_edge((node.x, node.y), (current_goal.x, current_goal.y))
            self.add_edge((node.x, node.y), (robot.x, robot.y))

    def init_vis(self, obstacle, current_goal):

        # offset = (obstacle[0][0] + obstacle[1][0]) / 2 # Half of box length.
        offset = 1
        # robot = camera.grid.getRobot()
        # robot_node = self.nodes[robot]
        # goal_node = self.nodes[goal]

        x1 = obstacle[0][0]
        y1 = obstacle[0][1]
        x2 = obstacle[1][0]
        y2 = obstacle[1][1]

        # Create nodes at each corner of the obstacle
        self.add_node(x1 - offset, y1 + offset)
        self.add_node(x2 + offset, y1 + offset)
        self.add_node(x1 - offset, y2 - offset)
        self.add_node(x2 + offset, y2 - offset)

        # Add edges from each corner to the current goal
        self.add_edge((x1 - offset, y1 + offset), (current_goal.x, current_goal.y))
        self.add_edge((x2 + offset, y1 + offset), (current_goal.x, current_goal.y))
        self.add_edge((x1 - offset, y2 - offset), (current_goal.x, current_goal.y))
        self.add_edge((x2 + offset, y2 - offset), (current_goal.x, current_goal.y))

    def debug_print_nodes(self):
        for (x, y), node in self.nodes.items():
            print(f'Node at ({x}, {y}):')
            for neighbor, cost in node.neighbors.items():
                print(f'  Neighbor at ({neighbor.x}, {neighbor.y}) with cost {cost}')


def algo():
    global robot

    start = 1
    graph = Graph()

    def shortest(graph, start_node, end_node):
        queue = [(0, start_node)]
        distances = {node: float('infinity') for node in graph.nodes.values()}
        distances[start_node] = 0
        shortest_path = {}

        while queue:
            (dist, current) = heapq.heappop(queue)
            for neighbor, cost in current.neighbors.items():
                old_cost = distances[neighbor]
                new_cost = dist + cost
                if new_cost < old_cost:
                    distances[neighbor] = new_cost
                    shortest_path[neighbor] = current
                    heapq.heappush(queue, (new_cost, neighbor))

        # Reconstruct the shortest path
        path = []
        while end_node is not None:
            path.append((end_node.x, end_node.y))  # Append coordinates instead of node
            end_node = shortest_path.get(end_node)
        path.reverse()

        # Print shortest path
        print('Shortest path:')
        for node in path:
            print(node)

        return distances, path

    global grid

    # print(grid.obstacle)
    # robot = camera.grid.getRobot()
    # oball = camera.grid.getOball()
    # goal = camera.grid.getGoalSmall()
    goal = camera.grid.getMidpoint([(5, 10), (6, 10)])
    oball = camera.grid.getMidpoint([(12, 5), (12, 5)])
    graph.add_node(oball[0], oball[1])
    graph.add_node(robot[0], robot[1])
    graph.add_node(goal[0], goal[1])

    camera.grid.obstacle = [(3, 4), (5, 2)]


    # Initialize the four nodes around the obstacle
    current_goal = graph.nodes[goal]  # Replace with the actual current goal

    graph.init_vis(camera.grid.obstacle,current_goal)
    graph.update_edges(robot)
    # Update the edges based on the current goal

    # graph.add_node(current_goal[0], current_goal[1])


    obstacle = camera.grid.getObstacle()
    print(camera.grid.getMidpoint(obstacle))

    graph.add_edge(robot, oball)
    graph.add_edge(goal, oball)

    # Display graph.
    distances, path = shortest(graph, graph.nodes[robot], current_goal)
    draw_graph(graph, path)

    graph.debug_print_nodes()

    print(shortest(graph, graph.nodes[robot], current_goal))

    # print(camera.grid.obstacle)

    # while True:
    #     for y in range(len(camera.grid.boxes[0])):
    #         for x in range(len(camera.grid.boxes)):
    #             if camera.grid.boxes[x][y].getName() == "WBall":
    #                print("W", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "OBall":
    #                 print("O", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "Egg":
    #                 print("E", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "robot":
    #                 print("R", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "robotFront":
    #                 print("F", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "robotBack":
    #                 print("B", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "Goal-Small-":
    #                 print("S", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "Goal-Large-":
    #                 print("G", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "Obstacle":
    #                 print("|", end=" ")
    #             elif camera.grid.boxes[x][y].getName() == "Wall":
    #                 print("|", end=" ")
    #             else:
    #                 print(" ", end=" ")
    #         print("")
    #     time.sleep(1)

#Config location is:
#/etc/mosquitto/conf.d

#Use this to read log.
#tail -f /var/log/mosquitto/mosquitto.log
