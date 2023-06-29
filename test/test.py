import unittest
from selenium import webdriver

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.implicitly_wait(100)

    def tearDown(self):
        self.driver.quit()

    def test_index(self):
        self.driver.get('http://127.0.0.1:5000/pojistenec/index.html')
        title = self.driver.find_element_by_tag_name('h1').innerHtml
        self.assertEqual(title, 'Webová aplikace pro evidenci pojistných událostí')

if __name__ == '__main__':
    unittest.main()



