import unittest
import requests

class Test_staff(unittest.TestCase):
    def test_find_123456786(self):
        result = requests.get('http://127.0.0.1:5000/staff/123456786').json()['staff']
        self.assertEqual(result, 
            {
                "staff_id": 123456786, 
                "fname": "JOHN", 
                "lname":"DOE", 
                "dept": "IT", 
                "email": "john_email@email.com.sg", 
                "phone": "69-6969696969", 
                "biz_address": "address4", 
                "sys_role": "inactive"
            }
        )
    def test_find_123456787(self):
        result = requests.get('http://127.0.0.1:5000/staff/123456787').json()['staff']
        self.assertEqual(result,
            {
                "staff_id": 123456787, 
                "fname": "FAUD", 
                "lname":"NIZAM", 
                "dept": "SALES", 
                "email": "faud_email@email.com.sg", 
                "phone": "60-1234-5678", 
                "biz_address": "address3", 
                "sys_role": "manager"
            }
        )
    def test_cannot_find(self):
        result = requests.get('http://127.0.0.1:5000/staff/696969').json()
        self.assertEqual(result,
            {
                "code": 404,
                "message": "Staff not found."
            }
        )

    def test_find_by_skill(self):
        result = requests.get('http://127.0.0.1:5000/staff/skill/345678914').json()
        self.assertEqual(result,
            {
                "code":200,
                "data": {
                    "staff": [
                                {
                                    "biz_address": "address1",
                                    "dept": "FINANCE",
                                    "email": "tan_ah_gao@all-in-one.com.sg",
                                    "fname": "AH GAO",
                                    "lname": "TAN",
                                    "phone": "65-1234-5678",
                                    "staff_id": 123456789,
                                    "sys_role": "staff"
                                }
                            ]
                }
            }
        )

    def test_find_by_skill(self):
        result = requests.get('http://127.0.0.1:5000/staff/skill/123').json()
        self.assertEqual(result,
            {
                "code": 404,
                "message": "There is no staff."
            }
        )

    def test_find_suitable_candidate1(self):
        result = requests.get("http://127.0.0.1:5000/staff/suitable/234567893").json()
        self.maxDiff = None
        self.assertEqual(result,
            {
                "code": 200,
                "data": [
                    {
                        "biz_address": "address1",
                        "dept": "FINANCE",
                        "email": "tan_ah_gao@all-in-one.com.sg",
                        "fname": "AH GAO",
                        "lname": "TAN",
                        "match": True,
                        "matches": 1,
                        "phone": "65-1234-5678",
                        "staff_id": 123456789,
                        "sys_role": "staff"
                    }
                ]
            }
        )

    def test_find_suitable_candidate2(self):
        result = requests.get("http://127.0.0.1:5000/staff/suitable/234567891").json()
        self.maxDiff = None
        self.assertEqual(result,
            {
                "code": 200,
                "data": []
            }
        )

    
if __name__ == '__main__':
    unittest.main()