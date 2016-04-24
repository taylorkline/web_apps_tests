import unittest
import requests
from xml.etree import ElementTree

"""
This module uses the Python requests library to test assignment 5.
You should:
    - Have the requests library for Python installed.
    - Have your assignment 5 code running on Tomcat.
    - Run this script with python3.4
"""

base_url = "http://localhost:8080/assignment5/myeavesdrop/projects/"
header = {'Content-Type': 'application/xml'}

class TestPost(unittest.TestCase):

    def testBadRequests(self):
        """
        Empty string.
        """
        xml = ""
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Missing closing XML tag.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Plural 'projects'
        """
        xml = "<projects><name>solum</name><description>Project respresenting solum</description></projects>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Missing description
        """
        xml = "<project><name>solum</name></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Missing name
        """
        xml = "<project><description>solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Empty description.
        """
        xml = "<project><name>solum</name><description></description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<project><name>solum</name><description>     </description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Empty name.
        """
        xml = "<project><name></name><description>yay</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<project><name>    </name><description>yay</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        """
        Attempt to add valid meeting to missing project.
        """
        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(base_url + "/projects/121313231231/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 404)

        """
        Attempt to add invalid meeting to valid project.
        """
        # Create valid project.
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(base_url, r.headers['location'])
        project_resource = r.headers['location']

        # Attempt to add meeting
        xml = "<meeting><name></name><year>2014</year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<meeting><name>asdf</name><year></year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<meeting><name>   </name><year>2014</year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<meeting><name>hello</name><year>   </year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)

        xml = "<meeting><year>2014</year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 400)


    def testGoodRequests(self):
        """
        Direct from assignment page.
        """
        xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
        r = requests.post(base_url, data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(base_url, r.headers['location'])

        project_resource = r.headers['location']

        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(project_resource + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(project_resource, r.headers['location'])

# class TestPut(unittest.TestCase):
#     def setUp(self):
#         """
#         This depends on POST.
#         """
#         xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
#         r = requests.post(base_url, data=xml, headers=header)
#         self.putURL = r.headers['location']
# 
#     def testGoodRequestOne(self):
#         """
#         Try to update what already exists.
#         """
#         xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
#         r = requests.put(self.putURL, data=xml, headers=header)
#         self.assertTrue(r.status_code == 204 or r.status_code == 200)
# 
#     def testBadRequestOne(self):
#         """
#         Try to PUT with a bad ID number
#         """
#         xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
#         r = requests.put(base_url + "-1", data=xml, headers=header)
#         self.assertTrue(r.status_code == 400 or r.status_code == 404)
# 
#     def testBadRequestTwo(self):
#         """
#         Try to PUT with a bad ID string
#         """
#         xml = "<project><name>solum2</name><description>Updated solum stuff.</description></project>"
#         r = requests.put(base_url + "asdf", data=xml, headers=header)
#         self.assertTrue(r.status_code == 400 or r.status_code == 404)
# 
#     def testBadRequestThree(self):
#         """
#         Try to PUT with a empty name
#         """
#         xml = "<project><name></name><description>Updated solum stuff.</description></project>"
#         r = requests.put(self.putURL, data=xml, headers=header)
#         self.assertEqual(r.status_code, 400)
# 
class TestGet(unittest.TestCase):
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
        self.assertEqual(tree.find("name").text, "solum")
        self.assertEqual(tree.find("description").text, "Project representing solum")
        # ID is apparently required to be an attribute of the  root element, rather than an element itself
        self.assertEqual(tree.attrib['id'], self.putURL.split("/")[-1])

        xml = "<meeting><name>m1</name><year>2014</year></meeting>"
        r = requests.post(self.putURL + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(self.putURL, r.headers['location'])

        r = requests.get(self.putURL)
        tree = ElementTree.fromstring(r.content)
        self.assertTrue(tree.find("meetings") is not None)

        xml = "<meeting><name>m2</name><year>2016</year></meeting>"
        r = requests.post(self.putURL + "/meetings", data=xml, headers=header)
        self.assertEqual(r.status_code, 201)
        self.assertIn(self.putURL, r.headers['location'])

        r = requests.get(self.putURL)
        tree = ElementTree.fromstring(r.content)
        self.assertTrue(tree.find("meetings") is not None)
        # TODO: This needs some improvement. Manual checking required until then.

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

# class TestDelete(unittest.TestCase):
#     def setUp(self):
#         """
#         This depends on POST.
#         """
#         xml = "<project><name>solum</name><description>Project respresenting solum</description></project>"
#         r = requests.post(base_url, data=xml, headers=header)
#         self.putURL = r.headers['location']
# 
#     def testGoodRequestOne(self):
#         self.assertEqual(requests.get(self.putURL).status_code, 200)
#         r = requests.delete(self.putURL)
#         self.assertEqual(r.status_code, 200)
#         self.assertEqual(requests.get(self.putURL).status_code, 404)
# 
#     def testBadRequestOne(self):
#         """
#         Try DELETE with a bad ID number
#         """
#         r = requests.delete(base_url + "-1")
#         self.assertEqual(r.status_code, 404)
# 
#     def testBadRequestTwo(self):
#         """
#         Try DELETE with a bad ID string
#         """
#         r = requests.delete(base_url + "asdf")
#         self.assertEqual(r.status_code, 404)

if __name__ == '__main__':
    unittest.main()
