import storage
import json
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

    @classmethod
    def tearDownClass(testclass):
        app = storage.app.test_client()
        result = app.delete('/_databases/__test__')
        if result.status_code != 200:
            print(result.status_code)
            raise Exception("__test__ database could not be destroyed")

    def test_db_00_missing(self):
        result = self.app.get('/_databases')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, 'application/json')

        data = json.loads(result.get_data())
        self.assertIn('databases', data)
        self.assertNotIn('__test__', data['databases'])

    def test_db_01_create(self):
        result = self.app.post(
            '/_databases',
            content_type='application/json',
            data=json.dumps({'database': '__test__'})
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, 'application/json')
        self.assertDictEqual({
            "database": "__test__"
        }, json.loads(result.get_data()))

    def test_db_02_created(self):
        result = self.app.get('/_databases')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, 'application/json')

        data = json.loads(result.get_data())
        self.assertIn('databases', data)
        self.assertIn('__test__', data['databases'])

if __name__ == '__main__':
    unittest.main()
