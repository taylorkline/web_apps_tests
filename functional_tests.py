import unittest
import requests
from xml.etree import ElementTree

"""
This module uses the Python requests library to test assignment 4.

You should:
    - Have the requests library for Python installed.
    - Have your assignment 4 code running on Tomcat.
    - Run this script with python3.4
"""

base_url = "http://localhost:8080/assignment4/myeavesdrop/projects/"
header = {'Content-Type': 'application/xml'}

class TestPost(unittest.TestCase):

    def testBadRequestOne(self):
        """
        Empty string.
        """
        xml = ""
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestTwo(self):
        """
        Missing closing XML tag.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestThree(self):
        """
        Plural 'projects'
        """
        xml = "<projects><name>solum</name><description>Project respresenting solum</description></projects>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFour(self):
        """
        Missing description
        """
        xml = "<project><name>solum</name></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFive(self):
        """
        Missing name
        """
        xml = "<project><description>solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestSix(self):
        """
        Empty description.
        """
        xml = "<project><name>solum</name><description></description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestSeven(self):
        """
        Empty name.
        """
        xml = "<project><name></name><description>yay</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testGoodRequestOne(self):
        """
        Direct from assignment page.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(base_url, r.headers['location'])

class TestPut(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        """
        Try to update what already exists.
        """
        xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertTrue(r.status_code == 204 or r.status_code == 200)

    def testBadRequestOne(self):
        """
        Try to PUT with a bad ID number
        """
        xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
        r = requests.put(base_url + "-1", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestTwo(self):
        """
        Try to PUT with a bad ID string
        """
        xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
        r = requests.put(base_url + "asdf", data=xml, headers=header)
        self.assertEqual(r.status_code, 404)
        
    def testBadRequestThree(self):
        """
        Try to PUT with a empty name
        """
        xml = "<project><name></name><description>Updated solum stuff.</description></project>"
        r = requests.put(base_url + "1", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

class TestGet(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        r = requests.get(self.putURL)
        self.assertEqual(r.status_code, 200)
        tree = ElementTree.fromstring(r.content)
        self.assertEqual(tree.get("id"), self.putURL.split("/")[-1])
        # TODO: You should manually check the full response body.

    def testBadRequestOne(self):
        """
        Try GET with a bad ID number
        """
        r = requests.get(base_url + "-1")
        self.assertEqual(r.status_code, 404);

    def testBadRequestTwo(self):
        """
        Try GET with a bad ID string
        """
        r = requests.get(base_url + "asdf")
        self.assertEqual(r.status_code, 404);

class TestDelete(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        self.assertEqual(requests.get(self.putURL).status_code, 200)
        r = requests.delete(self.putURL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(requests.get(self.putURL).status_code, 404)

    def testBadRequestOne(self):
        """
        Try DELETE with a bad ID number
        """
        r = requests.delete(base_url + "-1")
        self.assertEqual(r.status_code, 404);

    def testBadRequestTwo(self):
        """
        Try DELETE with a bad ID string
        """
        r = requests.delete(base_url + "asdf")
        self.assertEqual(r.status_code, 404);

if __name__ == '__main__':
    unittest.main()
