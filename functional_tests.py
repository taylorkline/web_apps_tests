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

base_url = "http://localhost:8080/assignment5/myeavesdrop/projects/"
header = {'Content-Type': 'application/xml'}

class TestPostProject(unittest.TestCase):

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

class TestPutProject(unittest.TestCase):
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
        self.assertTrue(r.status_code == 400 or r.status_code == 404)

    def testBadRequestTwo(self):
        """
        Try to PUT with a bad ID string
        """
        xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
        r = requests.put(base_url + "asdf", data=xml, headers=header)
        self.assertTrue(r.status_code == 400 or r.status_code == 404)

    def testBadRequestThree(self):
        """
        Try to PUT with a empty name
        """
        xml = "<project><name></name><description>Updated solum stuff.</description></project>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

class TestGetProject(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project representing solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        r = requests.get(self.putURL)
        self.assertEqual(r.status_code, 200)
        tree = ElementTree.fromstring(r.content)
        # This schema will be project-specific
        self.assertEqual(tree.find("name").text, "solum")
        self.assertEqual(tree.find("description").text, "Project representing solum")
        self.assertEqual(tree.attrib['id'], self.putURL.split("/")[-1])
        # TODO: You should manually check the full response body
    def testBadRequestOne(self):
        """
        Try GET with a bad ID number
        """
        r = requests.get(base_url + "-1")
        self.assertEqual(r.status_code, 404)

    def testBadRequestTwo(self):
        """
        Try GET with a bad ID string
        """
        r = requests.get(base_url + "asdf")
        self.assertEqual(r.status_code, 404)

class TestDeleteProject(unittest.TestCase):
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
        self.assertEqual(r.status_code, 404)

    def testBadRequestTwo(self):
        """
        Try DELETE with a bad ID string
        """
        r = requests.delete(base_url + "asdf")
        self.assertEqual(r.status_code, 404)

class TestPostMeeting(unittest.TestCase):

    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location'] + "/meetings"

    def testBadRequestOne(self):
        """
        Empty string.
        """
        xml = ""
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestTwo(self):
        """
        Missing closing XML tag.
        """
        xml = "<meeting><name>m1</name><year>2016</year>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestThree(self):
        """
        Plural 'meetings'
        """
        xml = "<meetings><name>m1</name><year>2016</year></meetings>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFour(self):
        """
        Missing name
        """
        xml = "<meeting><name></name><year>2016</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFive(self):
        """
        Missing year
        """
        xml = "<meeting><name>m1</name><year></year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestSix(self):
        """
        Empty name.
        """
        xml = "<meeting><name>    </name><year>2016</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestSeven(self):
        """
        Empty year.
        """
        xml = "<meeting><name>m1</name><year>   </year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestEight(self):
        """
        String for year.
        """
        xml = "<meeting><name>m1</name><year>This is a bad year</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestNine(self):
        """
        Bad project ID
        """
        xml = "<meeting><name>m1</name><year>2016</year></meeting>"
        r = requests.post(base_url + "/projects/0/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 404)

    def testGoodRequestOne(self):
        """
        Direct from assignment page.
        """
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(base_url, r.headers['location'])

class TestPutMeeting(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location'] + "/meetings"
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        """
        Try to update what already exists.
        """
        xml = "<meeting><name>m1</name><year>2016</year></meeting>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertIn(r.status_code, (200, 204))

    def testBadRequestOne(self):
        """
        Try to PUT with a bad ID number
        """
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.put(self.putURL + '9999999999999999999', data=xml, headers=header)
        self.assertIn(r.status_code, (400, 404))

    def testBadRequestTwo(self):
        """
        Try to PUT with a bad ID string
        """
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.put(self.putURL + 'this should not work', data=xml, headers=header)
        self.assertIn(r.status_code, (400, 404))

    def testBadRequestThree(self):
        """
        Try to PUT with a empty name
        """
        xml = "<meeting><name></name><year>2014</year></meeting>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFour(self):
        """
        Try to PUT with a empty year
        """
        xml = "<meeting><name>m1</name><year></year></meeting>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestFive(self):
        """
        Try to PUT with a string year
        """
        xml = "<meeting><name>m1</name><year>This is a bad year</year></meeting>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

    def testBadRequestSix(self):
        """
        Try to PUT with a negative year
        """
        xml = "<meeting><name>m1</name><year>-1</year></meeting>"
        r = requests.put(self.putURL, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

class TestGetMeeting(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location'] + "/meetings"
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
        self.putURL = r.headers['location']

    def testGoodRequestOne(self):
        r = requests.get(self.putURL)
        self.assertEqual(r.status_code, 200)
        tree = ElementTree.fromstring(r.content)
        self.assertEqual(tree.find("name").text, "m1")
        self.assertEqual(tree.find("year").text, "2014")
        self.assertEqual(tree.attrib['id'], self.putURL.split("/")[-1])

    def testBadRequestOne(self):
        """
        Try GET with a bad ID number
        """
        r = requests.get(self.putURL + "99999999999999999")
        self.assertEqual(r.status_code, 404)

    def testBadRequestTwo(self):
        """
        Try GET with a bad ID string
        """
        r = requests.get(self.putURL + "asdf")
        self.assertEqual(r.status_code, 404)

class TestDeleteMeeting(unittest.TestCase):
    def setUp(self):
        """
        This depends on POST.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.putURL = r.headers['location'] + "/meetings"
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(self.putURL, data=xml, headers=header)
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
        r = requests.delete(self.putURL + "-1")
        self.assertEqual(r.status_code, 404)

    def testBadRequestTwo(self):
        """
        Try DELETE with a bad ID string
        """
        r = requests.delete(self.putURL + "asdf")
        self.assertEqual(r.status_code, 404)

if __name__ == '__main__':
    unittest.main()