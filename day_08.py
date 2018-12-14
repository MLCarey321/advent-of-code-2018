#!/usr/bin/python3

import sys


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata


def get_metadata(node, array):
    metadata = 0
    num_children = array[node]
    num_meta = array[node+1]
    next_node = node+2
    for child in range(num_children):
        result = get_metadata(next_node, array)
        next_node = result[0]
        metadata += result[1]
    for meta in range(num_meta):
        metadata += array[next_node]
        next_node += 1
    return next_node, metadata


def get_part_two(node, array):
    num_children = array[node]
    num_meta = array[node+1]
    next_node = node+2
    if num_children == 0:
        metadata = []
        for meta in range(num_meta):
            metadata.append(array[next_node])
            next_node += 1
        result = Node(None, metadata)
    else:
        children = []
        for i in range(num_children):
            child_result = get_part_two(next_node, array)
            next_node = child_result[0]
            children.append(child_result[1])
        metadata = []
        for meta in range(num_meta):
            metadata.append(array[next_node])
            next_node += 1
        result = Node(children, metadata)
    return next_node, result


def get_value(node):
    if not node.children:
        return sum(node.metadata)
    value = 0
    for meta in node.metadata:
        if meta <= len(node.children):
            value += get_value(node.children[meta-1])
    return value


puzzle = list(map(int, sys.stdin.readline().split()))
print "Part One:", get_metadata(0, puzzle)[1]
root_node = get_part_two(0, puzzle)[1]
print "Part Two:", get_value(root_node)
