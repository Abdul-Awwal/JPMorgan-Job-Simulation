"""
The goal of this coding activity is to design a system that limits the number of active roles that any given person has. A role gives the user access to some thing, whether it be a piece of data or an internal system. The system achieves this requirement by keeping track of the last k roles that a person has used. If a new role is used, the oldest role is removed if there are already k active roles for that person. Each role has a name and a message which contains details about its use by the person. You only need to store the last message for a role invocation.

Implement the constructor, get, and set methods of RolesCache. Each instance of the RolesCache corresponds to a single person.

Finally, fill out the runtime complexity for get and set and the overall space used. Use Big O notation, i.e. O(1), O(N), etc. For a refresher on Big O notation, please review https://danielmiessler.com/study/big-o-notation/.

"""

"""
The goal of this coding activity is to design a system that limits the number of active roles that any given person has. A role gives the user access to some thing, whether it be a piece of data or an internal system. The system achieves this requirement by keeping track of the last k roles that a person has used. If a new role is used, the oldest role is removed if there are already k active roles for that person. Each role has a name and a message which contains details about its use by the person. You only need to store the last message for a role invocation.

Implement the constructor, get, and set methods of RolesCache. Each instance of the RolesCache corresponds to a single person.

Finally, fill out the runtime complexity for get and set and the overall space used. Use Big O notation, i.e. O(1), O(N), etc. For a refresher on Big O notation, please review https://danielmiessler.com/study/big-o-notation/.

"""
import unittest
class Node:
    def __init__(self, role, message):
        self.role = role
        self.message = message
        self.prev = None
        self.next = None

class RolesCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(None, None)  # Dummy head
        self.tail = Node(None, None)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove a node from the linked list."""
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def _add_to_head(self, node):
        """Add a node right after the head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, role):
        if role in self.cache:
            node = self.cache[role]
            self._remove(node)
            self._add_to_head(node)
            return node.message
        return None

    def set(self, role, message):
        if role in self.cache:
            node = self.cache[role]
            node.message = message
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove the oldest node
                oldest = self.tail.prev
                self._remove(oldest)
                del self.cache[oldest.role]
            # Add the new node
            new_node = Node(role, message)
            self.cache[role] = new_node
            self._add_to_head(new_node)

    def _complexity(self):
        return {
            'get': 'O(1)',
            'set': 'O(1)',
            'space': 'O(N)'
        }



class TestRolesCache(unittest.TestCase):

    def test_set_and_get_role(self):
        cache = RolesCache(2)
        cache.set('admin', 'admin message')
        self.assertEqual(cache.get('admin'), 'admin message')
        cache.set('user', 'user message')
        self.assertEqual(cache.get('user'), 'user message')
        self.assertEqual(cache.get('admin'), 'admin message')

    def test_update_role_message(self):
        cache = RolesCache(2)
        cache.set('admin', 'admin message')
        cache.set('admin', 'updated admin message')
        self.assertEqual(cache.get('admin'), 'updated admin message')

    def test_eviction(self):
        cache = RolesCache(2)
        cache.set('admin', 'admin message')
        cache.set('user', 'user message')
        cache.set('guest', 'guest message')  # This should evict 'admin'
        self.assertIsNone(cache.get('admin'))
        self.assertEqual(cache.get('user'), 'user message')
        self.assertEqual(cache.get('guest'), 'guest message')

    def test_reorder_on_get(self):
        cache = RolesCache(2)
        cache.set('admin', 'admin message')
        cache.set('user', 'user message')
        cache.get('admin')  # Access 'admin' to make it the most recently used
        cache.set('guest', 'guest message')  # This should evict 'user'
        self.assertEqual(cache.get('admin'), 'admin message')
        self.assertIsNone(cache.get('user'))
        self.assertEqual(cache.get('guest'), 'guest message')

    def test_cache_size_one(self):
        cache = RolesCache(1)
        cache.set('admin', 'admin message')
        self.assertEqual(cache.get('admin'), 'admin message')
        cache.set('user', 'user message')  # This should evict 'admin'
        self.assertIsNone(cache.get('admin'))
        self.assertEqual(cache.get('user'), 'user message')

    def test_nonexistent_role(self):
        cache = RolesCache(2)
        self.assertIsNone(cache.get('nonexistent'))
        cache.set('admin', 'admin message')
        self.assertIsNone(cache.get('nonexistent'))

if __name__ == '__main__':
    unittest.main()
