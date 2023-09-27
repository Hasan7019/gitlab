import unittest
import requests

class Test_skill(unittest.TestCase):
    def test_find_by_skill_id(self):
        result = requests.get('http://127.0.0.1:5001/skills/345678969').json()['skill']
        self.assertEqual(result,
            {
                "skill_id": 345678969,
                "skill_name": "Certified Freak",
                "skill_status": "inactive"
            }
        )
    
    def test_find_by_skill_id2(self):
        result = requests.get('http://127.0.0.1:5001/skills/345678970').json()
        self.assertEqual(result,
            {
                "code": 200,
                "skill": {
                    "skill_id": 345678970,
                    "skill_name": "Java Programming",
                    "skill_status": "active"
                }
            }
        )

if __name__ == '__main__':
    unittest.main()