import os
from typing import List

HASH_SIZE = 16
INT_SIZE = 8

BYTE_ORDER = 'big'


class Item:
    def __init__(self, hash: bytes, offset: bytes, child: bytes) -> None:
        self._hash = hash
        self._offset = offset
        self._child = child

    def to_bytes(self) -> bytes:
        return self._hash + self._offset + self._child

    def get_hash(self) -> bytes:
        return self._hash

    def get_offset(self) -> int:
        return int.from_bytes(self._offset, byteorder=BYTE_ORDER)

    def get_child(self) -> int:
        return int.from_bytes(self._child, byteorder=BYTE_ORDER)

    def set_hash(self, hash: bytes) -> None:
        self._hash = hash

    def set_offset(self, offset: int) -> None:
        self._offset = offset.to_bytes(INT_SIZE, byteorder=BYTE_ORDER)

    def set_child(self, child: int) -> None:
        self._child = child.to_bytes(INT_SIZE, byteorder=BYTE_ORDER)

    def __eq__(self, other) -> bool:
        return self._hash == other.get_hash()

    def __gt__(self, other) -> bool:
        return self._hash > other.get_hash()

    def __lt__(self, other) -> bool:
        return self._hash < other.get_hash()


class Table:
    def __init__(self, fd: int) -> None:
        self.fd = fd
        self.size = 0
        self.items: List[Item]

    def insert(self, item: Item) -> None:
        self.items += item

    def search(self) -> Item:
        return self.items[0]


class BTree:
    def __init__(self, file: str) -> None:
        self.file = file
        self.fd = 0
        self.top = 0
        self.free_top = 0

    def open(self):
        self.fd = os.open(self.file, os.O_RDWR |
                          os.O_CREAT | os.O_BINARY, 0o644)
        os.lseek(self.fd, 0, os.SEEK_SET)
        b = os.read(self.fd, INT_SIZE*3)
        # if not init
        if len(b) == 0:
            os.lseek(self.fd, 0, os.SEEK_SET)
            os.write(self.fd, (10).to_bytes(INT_SIZE, byteorder=BYTE_ORDER))
            os.write(self.fd, (11).to_bytes(INT_SIZE, byteorder=BYTE_ORDER))
            os.write(self.fd, (12).to_bytes(INT_SIZE, byteorder=BYTE_ORDER))
        elif len(b) != INT_SIZE*3:
            raise Exception("file is not a btree database")
        else:
            self.top = int.from_bytes(b[:INT_SIZE], byteorder=BYTE_ORDER)

            self.free_top = int.from_bytes(
                b[INT_SIZE:INT_SIZE*2], byteorder=BYTE_ORDER)
            self.alloc = int.from_bytes(
                b[INT_SIZE*2:INT_SIZE*3], byteorder=BYTE_ORDER)

    def close(self):
        os.close(self.fd)

    def table(self) -> Table:
        return Table(self.fd)


if __name__ == '__main__':
    # btree = BTree("test.txt")
    # btree.open()
    # #os.write(btree.fd, '123'.encode(encoding='utf-8'))
    # btree.close()
    a = Item(b'1234567812345678', b'12345678', b'12345678')
    b = Item(b'1234567812345678', b'12345678', b'12345678')
    if a == b:
        print('ok')
    print(a.get_hash())
