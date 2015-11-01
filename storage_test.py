import storage
import unittest


class TestStorageCase(unittest.TestCase):
    # check that there is no testing DB present before we test
    @classmethod
    def setUpClass(testclass):
        storage.app.config['TESTING'] = True
        app = storage.app.test_client()
        result = app.get('/__test__/entries')
        if result.status_code != 404:
            print(result.status_code)
            raise Exception("__test__ database already exists, not proceeding")

    def setUp(self):
        storage.app.config['TESTING'] = True
        self.app = storage.app.test_client()

    def tearDown(self):
        pass

    def test_empty_db(self):
        result = self.app.get('/__test__/entries')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
