import unittest
from LinkedTimestampChain import LinkedTimestampChain
from Record import Record

class TestLinkedTimestampChain(unittest.TestCase):
    def test_hash_of_first_record_is_always_the_same(self):
        chain = LinkedTimestampChain()
        chain.add_content('first')
        previous_hash_value = chain.get_chain()[0].get_previous_hash()

        chain_1 = LinkedTimestampChain()
        chain_1.add_content('second')
        previous_hash_value_on_second_chain = chain_1.get_chain()[0].get_previous_hash()
        
        self.assertEqual(previous_hash_value, previous_hash_value_on_second_chain, 'Hash are not equal')
    
    def test_once_added_one_content_chain_contains_one_element(self):
        chain = LinkedTimestampChain()
        chain.add_content('first')
        records = chain.get_chain()
        
        self.assertEqual(1, len(records), 'Chain does not contain one element')

    def test_if_content_of_an_existing_record_is_changed_verify_fails(self):
        record = Record('a')
        record._Record__content = 'b'
        self.assertFalse(record.verify(), 'Change should have been detected')

    def test_content_not_modified_verifies_ok(self):
        record = Record('a')
        self.assertTrue(record.verify(), 'Verify must go ok since content has not changed')

    def test_changing_record_in_a_chain_fires_link_verification_error(self):
        chain = LinkedTimestampChain()
        chain.add_content('first')
        chain.add_content('second')

        record_intrusion = Record('intrusion')
        records = chain.get_chain()
        records[0] = record_intrusion

        chain = LinkedTimestampChain()
        chain.add_records(records)

        self.assertFalse(chain.verify(), 'Intrusion should have been detected')
        self.assertTrue('chain' in chain.get_error().lower(), 'Error message must be about a change in the chain')

    def test_changing_record_content_in_a_chain_fires_verification_error(self):
        chain = LinkedTimestampChain()
        chain.add_content('first')
        chain.add_content('second')

        records = chain.get_chain()
        records[0]._Record__content = 'intrusion'

        self.assertFalse(chain.verify(), 'Change should have been detected')
        self.assertTrue('content' in chain.get_error().lower(), 'Error message must be about a change of the content')

if __name__ == '__main__':
    unittest.main()