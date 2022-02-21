'''
Author: Kanri
Date: 2022-02-19 15:15:50
LastEditors: Kanri
LastEditTime: 2022-02-21 20:04:17
Description: BtreeDB
'''

from ctypes import sizeof
from hashlib import sha1
import io
import pickle
from turtle import position
from typing import List, Tuple

from sqlalchemy import table, true


class Cache:
    def __init__(self, btree: Btree) -> None:
        self.btree = btree
        self.cache = 0
        self.offset = 0
        self.data: bytes


class Node:
    def __init__(self, btree: Btree) -> None:
        self.btree = btree
        self.table: Item = []
        self.size = 0

    def get(self, offset: int):
        self.btree.fd.seek(offset)
        for i in self.table:
            self.btree.fd.read()

        self.btree.fd.seek(0)
        pass

    def put(self, offset: int):
        pass





class Item:
    def __init__(self, hash: bytes, child: bytes, offset: bytes) -> None:
        self.hash = hash
        self.child = child
        self.offset = offset

    def get_child(self) -> int:
        return int.from_bytes(self.child, byteorder='big')

    def get_offset(self) -> int:
        return int.from_bytes(self.offset, byteorder='big')

    def set_child(self, child: int) -> None:
        self.child = child.to_bytes(8, byteorder='big')

    def set_offset(self, offset: int) -> None:
        self.offset = offset.to_bytes(8, byteorder='big')

    def __eq__(self, other) -> bool:
        return self.hash == other.hash

    def __gt__(self, other) -> bool:
        return self.hash > other.hash

    def __lt__(self, other) -> bool:
        return self.hash < other.hash


class Table:
    def __init__(self, length: int, items: List[Item]) -> None:
        
        self.length = length
        self.items = items

    def insert(self, index: int, object: Item):
        self.items.insert(index, object)

    def remove(self, index: int) -> Item:
        item = self.items[index]
        del self.items[index]

    def pop(self) -> Item:
        self.items.pop()

    def find(self, hash: bytes) -> Item:
        pass
                
                
page_size = 4096
hash_size = 16
int_size = 8
item_size = hash_size + int_size * 2
table_size = page_size / item_size

def read_table(fd: io.BufferedRandom, offset: int) -> Table:
    fd.seek(offset)
    data = fd.read(table_size * item_size)
    items: List[Item] = []
    length: int = 0
    for i in range(0, table_size):
        item = Item(fd.read(hash_size), fd.read(int_size), fd.read(int_size))
        if item.hash == b'':
            length = i
        items.append(item)
    return Table(length, items)


def write_table(fd: io.BufferedRandom, table: Table, offset: int):
    fd.seek(offset)
    for i in range(0, table_size):
        fd.write(table.items[i].hash)
        fd.write(table.items[i].child)
        fd.write(table.items[i].offset)
    fd.flush()
    

def btree_search(fd: io.BufferedRandom, table: Table, hash: bytes) -> Item:
    left, right = 0, table.length
    while left < right:
        mid = (right-left)>>1 + left
        if table.items[mid] == hash:
            return table.items[mid], True
        elif table.items[mid] > hash:
            right = mid
        else:
            left = mid + 1
    child = table.items[left].child
    if child == 0:
        return None
    child_table = read_table(fd, child)
    return table_search(fd, child_table, hash)

def table_search(table: Table, hash: bytes) -> Tuple(int, bool):
    left, right = 0, table.length
    while left < right:
        mid = (right-left)>>1 + left
        if table.items[mid] == hash:
            return mid, True
        elif table.items[mid] > hash:
            right = mid
        else:
            left = mid + 1
    return left, False


def table_insert(table: Table, item: Item) -> Item:
    index, found = table_search(table, item.hash)
    if found:
        out, table[index] = table[index], item
        return out
    if table.length < table_size:
        table.insert(index, item)
    


class Btree:
    def __init__(self, file: str) -> None:
        self.fd = open(file, "r+b")
        self.fd.seek(0)
        self.root = read_table(self.fd, 0)

    def insert(self, key: bytes, data: bytes) -> None:
        pass

    def delete(self, key: bytes) -> bytes:
        pass

    def select(self, key: bytes) -> bytes:
        pass

    def update(self, key: bytes, data: bytes) -> None:
        pass


if __name__ == '__main__':
    btree = Btree("test.btree")
    item = Item(sha1("1".encode("utf-8")).hexdigest(), 0, 0)
    item.dump_data(btree.fd, b"hello")
    print(item.load_data(btree.fd))
