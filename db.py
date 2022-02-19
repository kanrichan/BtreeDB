'''
Author: Kanri
Date: 2022-02-19 15:15:50
LastEditors: Kanri
LastEditTime: 2022-02-19 23:10:40
Description: BtreeDB
'''


from ast import Tuple
from ctypes import sizeof
from hashlib import sha1
import io
import pickle
from turtle import position
from typing import List

from sqlalchemy import table


class Btree:
    def __init__(self, file: str) -> None:
        self.fd = open(file, "r+b")
        self.fd.seek(0)


class Cache:
    def __init__(self, btree: Btree) -> None:
        self.btree = btree
        self.cache = 0
        self.offset = 0
        self.data: bytes
        

class Table:
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

item_size = 32 + 8 + 8





class Item:
    def __init__(self, hash: str, child: int, offset: int) -> None:
        self.__hash = hash
        self.__child = child
        self.__offset = offset
        
    def load_data(self, fd: io.TextIOWrapper) -> bytes:
        fd.seek(self.__offset)
        length = int.from_bytes(fd.read(8), byteorder = 'big')
        fd.seek(self.__offset+8)
        return fd.read(length)
    
    def dump_data(self, fd: io.TextIOWrapper, data: bytes):
        fd.seek(self.__offset)
        fd.write(len(data).to_bytes(8, byteorder='big'))
        fd.seek(self.__offset+8)
        fd.write(data)

    def __eq__(self, other) -> bool:
        return self.__hash == other.__hash

    def __gt__(self, other) -> bool:
        return self.__hash > other.__hash

    def __lt__(self, other) -> bool:
        return self.__hash < other.__hash

class Node:
    def __init__(self, items: List[Item]) -> None:
        self.__items = items
        
    def insert(self, index: int, object: Item):
        self.__items.insert(index, object)
        
    def remove(self, index: int) -> Item:
        item = self.__items[index]
        del self.__items[index]
        
    def pop(self) -> Item:
        self.__items.pop()
        
    def find(self) -> Tuple[Item,bool]:
        self.__items

if __name__ == '__main__':
    btree = Btree("test.btree")
    item = Item(sha1("1".encode("utf-8")).hexdigest(), 0, 0)
    item.dump_data(btree.fd, "hello".encode("utf-8"))
    print(item.load_data(btree.fd))
