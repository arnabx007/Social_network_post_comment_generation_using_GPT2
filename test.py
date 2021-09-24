import unittest

from demoapp.generate import generate_comment
from demoapp.utils import get_db, get_collection

# Get the database
db, client = get_db(db_name = 'generated_comment_db')
# Get the collection
coll = get_collection(db, 'comments')

# Create your tests here.

post = 'Mr. Anderson has reached New York safely. He will be giving the keynote speech at 10 am sharp.'

class UniqueTestCase(unittest.TestCase):
        
    def test_unique(self):
        comment1 = generate_comment(post)
        comment2 = generate_comment(post)

        data1 = {'post':post, 'comment': comment1}
        data2 = {'post':post, 'comment': comment2}
        
        # Delete these test entries from the database
        coll.delete_one(data1)
        coll.delete_one(data2)

        self.assertNotEqual(comment1, comment2)