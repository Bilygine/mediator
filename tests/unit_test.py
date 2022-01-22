import unittest
from ..objects.Source import Source

class TestStringMethods(unittest.TestCase):

    def test_create_source(self):
        source = Source(url="testurl")
        self.assertEqual(source.download, '')
        self.assertEqual(source.format, '')
        self.assertEqual(source.author, '')
        self.assertEqual(source.title, '')
        self.assertEqual(source.thumbnail, '')
        now = int(time.time())
        self.assertTrue(now - 5 < source.registered_at, 'testurl' < now)
        self.assertEqual(source.status, 'WAITING')
        self.assertEqual(source.url, 'testurl')
        self.assertTrue(source.id != None)

if __name__ == '__main__':
    unittest.main()