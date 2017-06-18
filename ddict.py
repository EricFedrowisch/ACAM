"""
Double dictionary that behaves like a list but should be faster to search. It
has indexes like a list but can also search and return all the indexes that
contain a given value.
"""


class DDict:
    def __init__(self):
        # In dict indices; keys must be integer, vals must be hashable
        self.indices = dict()
        # In dict values, keys must be (hashable), vals = set of indices of key
        self.values = dict()
        # Self iteration variable
        self.currentIndex = 0

    def __str__(self):
        s = ''
        for i in sorted(self.indices.keys()):
            # Used variables here to make PEP8 happy(String concat too long)
            ival = str(self.indices[i])
            occurs = str(list(self.values[self.indices[i]]))
            t = '{' + str(i) + ': ' + ival + ': ' + occurs + "}\n"
            s += t
        return s

    def __len__(self):
        return self.len()

    def __repr__(self):
        return self.__str__()

    def __hashable__(self, v):
        """Return bool for whether v is hashable"""
        try:
            hash(v)
        except Exception:
            return False
        return True

    def __validIndex__(self, i):
        """Return bool for whether i is a valid integer index"""
        try:
            int(i)  # Not great here as it would pass floats and prolly others
        except ValueError:
            return False
        return True

    def __prune__(self, i):
        """Remove index i from indicess for value x."""
        v = self.indices[i]
        self.values[v] = self.values[v].difference([i])
        if len(self.values[v]) < 1:  # If there are no indices left..
            del self.values[v]  # Remove value from ddict

    def __shift__(self, a, b):
        """Convenience function. Overwrite values at index a onto b."""
        self.set(b, self.indices[a])  # Overwrite b with a

    def __setitem__(self, i, x):
        # Allows for use of ddict[i] = x syntax.
        self.set(i, x)

    def __getitem__(self, i):
        """Method to allow for ddict[i] syntax."""
        try:
            i = int(i)
            r = self.indices[i]
        except Exception as error:
            raise error
        return r

    def __iter__(self):
        """Allows for iteration of keys of self.indices"""
        return self

    def __delitem__(self, i):
        """Allows for use of del ddict[i] syntax."""
        self.pop(i)

    def next(self):
        """Function for yielding next element."""
        if self.currentIndex < self.len():
            self.currentIndex += 1
            return self.indices[self.currentIndex-1]
        else:
            self.currentIndex = 0
            raise StopIteration

    def len(self):
        """Return int length of indexed values."""
        return len(self.indices)

    def unique(self):
        """Return number of unique values in DDict."""
        return len(self.values)

    def count(self, x):
        """Return number of occurences of a value in DDict."""
        try:  # See if x exists as a value...
            c = len(self.values[x])
        except KeyError:  # If not catch KeyError
            return 0  # If key doesn't exist then count == 0
        return len(self.values[x])  # If no KeyError, give count

    def set(self, i, x):
        """Set value of index i = x, overwriting existing value if any."""
        if self.__validIndex__(i) and self.__hashable__(x):
            i = int(i)
            if i < 0 or i > self.len():
                raise ValueError()  # i out of range
            if i in self.indices:
                self.__prune__(i)  # Remove any old value indices
            self.indices[i] = x  # Add value at index
            # Update value's locational index info
            if x in self.values:  # Set to union of indices
                self.values[x] = set.union(self.values[x], [i])
            else:  # Else if first indice...
                self.values[x] = set([i])  # Create set
        else:  # If either argument is bad...
            raise TypeError  # Throw exception

    def append(self, val):
        """Add an item to the end of the list."""
        self.set(self.len(), val)

    def extend(self, iterable):
        """Extend the DDict by appending all the items from the iterable."""
        try:
            for i in iterable:
                self.append(i)
        except (AttributeError, TypeError) as error:
            raise error

    def index(self, x):
        """Return list of indices of value equal to x (or None)."""
        try:
            r = self.values[x]
        except KeyError:
            return None
        return list(r)

    def insert(self, i, x):
        """Insert x at a given position i, give i in range 0 to len of ddict"""
        if i < 0 or i > self.len():
            raise ValueError
        r = xrange(self.len()-1, i, -1)
        self.append(self.indices[self.len()-1])  # Append last to len + 1
        for i in r:
            self.__shift__(i-1, i)
        self.set(i-1, x)

    def reverse(self):
        """Reverse the value indices."""
        r = xrange(self.len()-1, -1, -1)
        d = DDict()
        for i in r:
            d.append(self[i])
        return d

    def clear(self):
        """Remove all items from the list. Equivalent to del a[:]."""
        self.__init__()  # Idk why you would want this, but here it is.

    def copy(self):
        """Return a shallow copy of the ddict."""
        d = DDict()
        [d.append(self[i]) for i in sorted(self.indices.keys())]
        return d

    def pop(self, i):
        """Remove the item at the given position in the list, and return it.
        Changes the indices of all items gt i."""
        if i < 0 or i > self.len():
            raise ValueError
        x = self[i]
        r = xrange(i, self.len()-1)
        for j in r:
            self.__shift__(j+1, j)
        self.__prune__(self.len()-1)
        del self.indices[self.len()-1]
        return x

    def remove(self, x, All=False):
        """Remove the first item (or optionally all) from the ddict whose
        value is x."""
        if x not in self.values:
            raise ValueError
        if not All:
            i = sorted(list(self.values[x]))[0]
            self.pop(i)
        else:
            while self.count(x) > 0:
                self.pop(list(self.values[x])[0])

    def sort(self, cmp=None, key=None, reverse=False):
        d = DDict()
        for k in sorted(self.values.keys(), cmp, key, reverse):
            for i in xrange(0, len(self.values[k])):
                d.append(k)
        return d

# TODO: Add temporal stamping to indices
if __name__ == "__main__":
    d = DDict()
    d.append('a')
    d.append('a')
    d.append('cba')
    d.append('a')
    d.set(4, 123)
    print d
    print d[0]
    d[0] = 'abc'
    print d
    e = d.sort()
    print e

# Copyright June 11, 2017 by Eric Fedrowisch, All Rights Reserved.
