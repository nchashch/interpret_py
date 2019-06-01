from linked_list import LinkedList

class HashMap:
    def __init__(self, capacity):
        self._capacity = capacity
        self._buckets = [LinkedList() for _ in range(capacity)]

    def __setitem__(self, key, value):
        index = hash(key) % self._capacity
        if not self._buckets[index].peek():
            self._buckets[index].push((key, value))
        else:
            bucket = self._buckets[index]
            i = 0
            while bucket.get(i):
                if bucket.get(i)[0] == key:
                    bucket.delete(i)
                    bucket.push((key, value))
                    return
                i += 1
            bucket.push((key, value))

    def __getitem__(self, key):
        index = hash(key) % self._capacity
        bucket = self._buckets[index]
        i = 0
        while bucket.get(i):
            if bucket.get(i)[0] == key:
                return bucket.get(i)[1]
            i += 1
        return None

    def __repr__(self):
        result = '{ '
        for bucket in self._buckets:
            i = 0
            while bucket.get(i):
                key, value = bucket.get(i)
                result += '\'{}\':{}, '.format(key, value)
                i += 1
        result += ' }'
        return result

    def get(self, key):
        return self[key]

if __name__ == '__main__':
    hm = HashMap(10)
    hm[0] = 0;
    hm[100] = 10;
    for i in range(10):
        hm[0] = i
    print(hm)

