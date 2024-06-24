#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import random
# import Server.server
import camera
import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import server as server


def draw_graph(graph, path=None):
    if True:
        return
    G = nx.Graph()

    for node in graph.nodes.values():
        for neighbor, cost in node.neighbors.items():
            G.add_edge((node.x, node.y), (neighbor.x, neighbor.y), weight=cost)

    pos = {(node.x, node.y): (node.x, node.y) for node in graph.nodes.values()}

    if path is not None:
        print('Path in draw_graph:', path)
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

    # Format the labels of the nodes to remove trailing zeros
    labels = {node: f"({node[0]:g}, {node[1]:g})" for node in pos.keys()}

    nx.draw(G, pos, labels=labels)
    edge_labels = {((node.x, node.y), (neighbor.x, neighbor.y)): cost for node in graph.nodes.values() for
                   neighbor, cost in node.neighbors.items()}

    # Create a new dictionary that only includes one label for each pair of nodes
    single_edge_labels = {}
    for (node1, node2), cost in edge_labels.items():
        if (node2, node1) not in single_edge_labels:
            # Format the cost as a float, but remove trailing zeros
            single_edge_labels[(node1, node2)] = "{:g}".format(cost)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=single_edge_labels, label_pos=0.5, font_color='black',
                                 font_size=12, clip_on=False)

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


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = {}

    def add_neighbor(self, node, cost):
        self.neighbors[node] = cost

    def __str__(self):
        return f'Node({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return id(self) < id(other)


class Graph:

    def __init__(self):
        self.nodes = {}
        self.balls = []  # List to store ball nodes
        self.obstacles = []
        self.robot = self.add_node(*camera.grid.getMidpoint(camera.grid.getRobotBack()))
        self.goal = self.add_node(*camera.grid.getMidpoint(camera.grid.getGoalSmall()))

        # Node outside goal
        if 0 <= self.goal.x <= 100:
            self.goal_offset = self.add_node(self.goal.x + 10, self.goal.y)

        else:
            self.goal_offset = self.add_node(self.goal.x - 10, self.goal.y)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def add_node(self, x, y):
        node = Node(x, y)
        self.nodes[(x, y)] = node
        return node

    def remove_node(self, x, y):
        if (x, y) in self.nodes:
            node = self.nodes.pop((x, y))
            if node in self.balls:
                self.balls.remove(node)
            # Remove the node from its neighbors' lists
            for neighbor in node.neighbors:
                neighbor.neighbors.pop(node)
            print(f'Node at ({x}, {y}) removed.')

    def line_of_sight(self, node1, node2):
        # Generate points on the line between node1 and node2
        x_values = np.linspace(node1.x, node2.x, num=100)
        y_values = np.linspace(node1.y, node2.y, num=100)
        points = zip(x_values, y_values)

        # Check if any point on the line is within an obstacle
        for x, y in points:
            if self.is_node_in_obstacle(Node(x, y)):
                return False  # Return False if any point on the line is within an obstacle

        return True  # Return True if no point on the line is within an obstacle

    def add_edge(self, node1, node2):
        # Only add the edge if there is line of sight between the nodes
        if node1 != node2 and self.line_of_sight(node1, node2):
            # Calculate the Euclidean distance between the two points
            cost = round(math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2), 2)

            node1.add_neighbor(node2, cost)
            node2.add_neighbor(node1, cost)

    def update_edges(self, current_goal, robot):
        for node in self.nodes.values():
            self.add_edge(node, current_goal)
            self.add_edge(node, robot)

    def connect_all_nodes(self):
        for node1 in self.nodes.values():
            for node2 in self.nodes.values():
                if node1 != node2 and self.line_of_sight(node1, node2):
                    self.add_edge(node1, node2)

    def init_vis(self, obstacle, current_goal):

        # print("look here")
        self.add_obstacle(obstacle)
        print(obstacle)
        print(self.obstacles)

        x1, y1 = obstacle[0]
        x2, y2 = obstacle[1]
        offset = (x2 - x1) / 2

        # Create nodes at each corner of the obstacle
        node1 = self.add_node(x1 - offset, y1 + offset)
        node2 = self.add_node(x2 + offset, y1 + offset)
        node3 = self.add_node(x1 - offset, y2 - offset)
        node4 = self.add_node(x2 + offset, y2 - offset)

        print(node1)

        # Add edges from each corner to the current goal
        self.add_edge(node1, current_goal)
        self.add_edge(node2, current_goal)
        self.add_edge(node3, current_goal)
        self.add_edge(node4, current_goal)

    def debug_print_nodes(self):
        for (x, y), node in self.nodes.items():
            print(f'Node at ({x}, {y}):')
            for neighbor, cost in node.neighbors.items():
                print(f'  Neighbor at ({neighbor.x}, {neighbor.y}) with cost {cost}')

    def is_node_in_obstacle(self, node):
        for obstacle in self.obstacles:
            (x1, y1), (x2, y2) = obstacle
            # Test to check line of sight.
            # print(f"Checking node at ({node.x}, {node.y}) against obstacle at (({x1}, {y1}), ({x2}, {y2}))")
            if x1 <= node.x <= x2 and y2 <= node.y <= y1:
                # print("Node is in obstacle")
                return True
        return False

    # Testing function.
    # def add_balls(self, num_nodes):
    #     for i in range(num_nodes):
    #         x = -55 * (i + 1)
    #         y = 100 / (i + 1)
    #         if i == 2:
    #             x = 15
    #             y = 50
    #         # x = random.uniform(0, 15)  # Replace 0 and 10 with the desired range for x
    #         # y = random.uniform(0, 15)  # Replace 0 and 10 with the desired range for y
    #         node = Node(x, y)
    #         self.nodes[(x, y)] = node
    #         self.balls.append(node)  # Add the new node to the balls list
    #         # self.add_node(x, y)
    #         print("adding balls now")
    #         print(node)


def algo():
    time.sleep(20)
    global grid
    start = 1
    graph = Graph()
    robot = graph.robot
    goal = graph.goal

    # Attempt at aligning robot without color sensor.
    # At the start, put the robot so it lines up with the wall as much as possible.

    def allign(self):
        prev_x, prev_y = grid.camera.getRobot()
        server.sendMoveForward(50)
        moving = True
        iteration = 1
        xiteration = 1
        while moving:
            robot.x, robot.y = grid.camera.getRobot()
            if abs(robot.x - prev_x) == 1 and robot.y == prev_y:
                print("Robot has moved one tile horizontally.")
                # We are at a spot we can measure. Note the degrees of the gyro.
                # TODO: Adjust how many tiles is good enough for it to be going straight.
                xiteration = xiteration + 1

                if xiteration == 3:
                    # TODO: Reset gyro so its 0 when its alligned.
                    moving = False
                    # Server.server.sendMoveStop()


            elif abs(robot.y - prev_y) == 1 and robot.x == prev_x:
                print("Robot has moved one tile vertically.")
                if robot.y - prev_y > 0:  # Robot has moved up
                    # TODO: Please make the commands take a parameter as degrees to turn or move forward speed.
                    # Server.server.sendMoveRight(5 / iteration)  # Turn right to go back to the tile.
                    # Each time it loops, the iteration is bigger and the amount it turns is divided by this amount.
                    # 5 can be whatever turn we want.
                    # Server.server.sendMoveForward(10)  # Slows down.
                    iteration = iteration + 1
                    if iteration == 5:
                        moving = False
                else:  # Robot has moved down
                    # Server.server.sendMoveLeft(5 / iteration)  # Turn left to go back to the tile.
                    # Server.server.sendMoveForward(10)  # Slows down.
                    iteration = iteration + 1
                    if iteration == 5:
                        moving = False

    def shortest(graph, start_node, end_node):
        queue = [(0, start_node)]
        distances = {node: float('infinity') for node in graph.nodes.values()}
        distances[start_node] = 0
        shortest_path = {}

        while queue:
            (dist, current) = heapq.heappop(queue)
            for neighbor, cost in current.neighbors.items():
                if neighbor not in distances:
                    distances[neighbor] = float('infinity')

                old_cost = distances[neighbor]
                new_cost = dist + cost
                if new_cost < old_cost:
                    distances[neighbor] = new_cost
                    shortest_path[neighbor] = current
                    heapq.heappush(queue, (new_cost, neighbor))

        # Ensure end_node is in distances dictionary
        if end_node not in distances:
            distances[end_node] = float('infinity')

        # Reconstruct the shortest path
        path = []
        while end_node is not None:
            path.append((end_node.x, end_node.y))  # Append coordinates instead of node
            end_node = shortest_path.get(end_node)
        path.reverse()

        return distances, path

    # TODO: Turn and drive towards said path.
    # TODO: Think the code doesnt keep going until this function is finished.

    #temp orientation
    global orientation
    orientation = 0
    def turn_and_drive_towards_node(current_goal):

        #Calculation of direction vector
        direction_x = current_goal.x - robot.x
        direction_y = current_goal.y - robot.y
        def turn_to_target(target_x, target_y):
            global orientation
            print("look here!!!")
            direction_x = robot.x - target_x
            print(direction_x)
            direction_y = target_y - robot.y
            print(direction_y)
            target_angle = math.degrees(math.atan2(direction_y, direction_x))
            print(target_angle)

            target_angle = target_angle - orientation
            orientation = orientation + target_angle

            if orientation > 180:
                orientation = 0 - (360 - orientation)
            elif orientation < -180:
                orientation = 360 + orientation

            if target_angle < 0:
                server.sendMoveLeft(round(-target_angle))
            else:
                server.sendMoveRight(round(target_angle))

        def move_to_target(target_x, target_y):
            robot = graph.robot
            server.sendSpinForward()
            server.sendMoveForward(50)
            temp = robot
            while not is_robot_on_node(current_goal):
                robot = camera.grid.getMidpoint(camera.grid.getRobotBack())  # Update robot position
                if temp != robot:
                    print(robot)
                    temp = robot
                time.sleep(1)
            server.sendMoveStop()

        # For goal
        print("if current_goal == graph.goal_offset")
        if current_goal == graph.goal_offset:
            turn_to_target(*current_goal)
            move_to_target(current_goal.x, current_goal.y)
            turn_to_target(graph.goal)
            server.sendSpinBackward(50)
            robot.x = current_goal.x
            robot.y = current_goal.y

            # Default update of robot coordinates
            robot.x = current_goal.x
            robot.y = current_goal.y
            return

        # For balls
        else:
            turn_to_target(current_goal.x, current_goal.y)
            move_to_target(current_goal.x, current_goal.y)
            robot.x = current_goal.x
            robot.y = current_goal.y
            # Default update of robot coordinates
            robot.x = current_goal.x
            robot.y = current_goal.y
            if is_robot_on_node(current_goal):
                graph.nodes.pop(current_goal)
            return

    def find_closest_ball(self):
        min_distance = float('inf')
        # graph.connect_all_nodes()
        for node in graph.balls:  # Iterate over ball nodes only
            print("look here 1")
            # Calculate the shortest distance from the robot to the node
            graph.update_edges(node, robot)
            distances, path = shortest(graph, robot, node)
            print(node)
            print(distances[node])

            # If the calculated distance is less than min_distance, update min_distance and closest_node
            if node in distances and distances[node] < min_distance:
                min_distance = distances[node]
                print("look here 2")
                print(node)
                print(distances[node])
                print(current_goal)
                current_goal = node

    def add_balls():
        for ball in camera.grid.getWballs():
            # Get the coordinates of the ball
            x, y = camera.grid.getMidpoint(ball)


            # Create a new node at these coordinates
            node = Node(x, y)
            graph.nodes[(x, y)] = node

            # Add the new node to the balls list
            graph.balls.append(node)
            print("adding balls now")
            print(node)

    def is_robot_on_node(current_goal):
            tolerance = 5  # Define the tolerance range
            robot.x, robot.y = camera.grid.getMidpoint(camera.grid.getRobotBack())
            print("ROBOT X DISTANCE: " + str(abs(robot.x - current_goal.x)) + "ROBOT Y DISTANCE: " + str(abs(robot.y - current_goal.y)))
            if abs(robot.x - current_goal.x) < tolerance and abs(robot.y - current_goal.y) < tolerance:
                return True
            return False
    
    #Hard coded testing stuff.

    # Initialize the graph with nodes for important objects.
    # Hardcoded tests.
    # obstacle = [(3, 4), (5, 2)]
    # robot = graph.add_node(*camera.grid.getMidpoint([(0, 0), (0, 0)]))
    # goal = graph.add_node(*camera.grid.getMidpoint([(5, 10), (6, 10)]))
    # oball = graph.add_node(*camera.grid.getMidpoint([(12, 5), (12, 5)]))

    # Real setters.
    obstacle = camera.grid.getObstacle()
    print("Check here!")
    print("Obstacle", obstacle)
    print("Robot", robot)   
    print("Small goal", goal)
    oball = graph.add_node(*camera.grid.getMidpoint(camera.grid.getOball()))
    print("Oball", oball)

    # oball = graph.add_node(*camera.grid.getMidpoint([camera.grid.getGoalSmall(), camera.grid.getGoalSmall()]))

    # Initialize the four nodes around the obstacle
    current_goal = oball  # Replace with the actual current goal
    graph.init_vis(obstacle, current_goal)
    graph.update_edges(robot, oball)
    # Update the edges based on the current goal
    graph.add_edge(robot, oball)
    graph.add_edge(goal, oball)

    # Display graph graphically
    distances, path = shortest(graph, graph.nodes[(robot.x, robot.y)], current_goal)
    draw_graph(graph, path)

    # graph.debug_print_nodes() # Print the nodes and their neighbors
    graph.debug_print_nodes()

    # prints shortest path from robot to current goal
    print(shortest(graph, graph.nodes[(robot.x, robot.y)], current_goal))

    # Logic.allign()
    # First goal node.
    current_goal = graph.nodes[(current_goal.x, current_goal.y)]
    turn_and_drive_towards_node(current_goal)

    # Second goal node.
    robot = oball
    # graph.remove_node(oball.x,oball.y)
    goal = graph.goal_offset
    current_goal = goal
    graph.update_edges(current_goal, robot)
    distances, path = shortest(graph, robot, current_goal)
    draw_graph(graph, path)
    turn_and_drive_towards_node(current_goal)

    # Third goal node.
    print(camera.grid.getWballs())
    print(len(camera.grid.getWballs()))

    # TODO: When camera.grid.getWballs() is fixed, this should work.
    add_balls()
    print("look here!!!")
    print(graph.goal_offset)
    robot = goal

    # find_closest_ball(graph)
    for node in graph.balls:
        find_closest_ball(graph)
        turn_and_drive_towards_node(current_goal)

    current_goal = goal

    # turn_and_drive_towards_node(current_goal)

    # closest_node is now the closest node to the robot among the randomly generated nodes
    # Pass closest_node to graph.update_edges

    graph.update_edges(current_goal, robot)
    distances, path = shortest(graph, robot, current_goal)
    draw_graph(graph, path)

    # graph.update_edges(current_goal, robot)

    # distances, path = shortest(graph, graph.nodes[(robot.x, robot.y)], current_goal)
    # draw_graph(graph, path)

#Config location is:
#/etc/mosquitto/conf.d

#Use this to read log.
#tail -f /var/log/mosquitto/mosquitto.log
