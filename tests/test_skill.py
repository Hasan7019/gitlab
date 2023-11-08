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

    def test_lacking_skills1(self):
        result = requests.get("http://127.0.0.1:5001/get-lacking-skills/123456789/123456").json()
        self.assertEqual(result,
            {
                "code": 200,
                "lacking_skills": [
                    {
                        "skill_id": 345678971,
                        "skill_name": "Certified Water Hose",
                        "skill_status": "active"
                    }
                ]
            }
        )

    def test_lacking_skills2(self):
        result = requests.get("http://127.0.0.1:5001/get-lacking-skills/123456788/123456").json()
        self.assertEqual(result,
            {
                "code": 200,
                "lacking_skills": [
                    {
                        "skill_id": 345678971,
                        "skill_name": "Certified Water Hose",
                        "skill_status": "active"
                    }
                ]
            }
        )

    def test_get_skills_by_role1(self):
        result = requests.get("http://127.0.0.1:5001/skills/role/234567893").json()
        self.assertEqual(result,
            {
                "code": 200,
                "skills": [
                    {
                        "skill_id": 345678914,
                        "skill_name": "Certified Scrum Master",
                        "skill_status": "active"
                    }
                ]
            }
        )

    def test_add_role_skill2(self):
        result = requests.post("http://127.0.0.1:5001/role-skill", json={
            "this is a": "negative test case"
        }).json()
        self.assertEqual(result,
            {
                "code": 400,
                "error": "Missing or invalid key in the request body: 'role_id'"
            }
        )

if __name__ == '__main__':
    unittest.main()