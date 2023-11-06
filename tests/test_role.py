import unittest
import requests
from classes import *

class Test_staff(unittest.TestCase):

    def test_find_role_by_id1(self):
        result = requests.get('http://127.0.0.1:5002/roles/234567891').json()
        self.assertEqual(result,
            {
                "code": 200,
                "role": {
                    "role_description": "The Head, Talent Attraction is responsible for strategic workforce planning to support the organisation's growth strategies through establishing talent sourcing strategies, determining the philosophy for the selection and securing of candidates and overseeing the onboarding and integration of new hires into the organisation. He/She develops various approaches to meet workforce requirements and designs employer branding strategies. He oversees the selection processes and collaborates with business stakeholders for the hiring of key leadership roles. As a department head, he is responsible for setting the direction and articulating goals and objectives for the team, and driving the integration of Skills Frameworks across the organisation's talent attraction plans.\n\nThe Head, Talent Attraction is an influential and inspiring leader who adopts a broad perspective in the decisions he makes. He is articulate and displays a genuine passion for motivating and developing his team.",
                    "role_id": 234567891,
                    "role_name": "Head, Talent Attraction",
                    "role_status": "inactive"
                }
            }
        )
    
    def test_find_role_by_id_2(self):
        result = requests.get('http://127.0.0.1:5002/roles/69696969').json()
        self.assertEqual(result,
            {
                "code": 404,
                "message": "Role not found."
            }
        )

    # def test_create_role_1(self):
    #     result = requests.post("http://127.0.0.1:5002/roles", json={
    #         "role_id" = 1,
    #         "role_name" = "test role 1",
    #         "role_description" = "testing role 1",
    #         "role_status" = "active"
    #     }).json()
    #     new_role = Role(
    #         role_id=1,
    #         role_name="test role 1",
    #         role_description="testing role 1",
    #         role_status="active"
    #     )
    #     self.assertEqual(result,
    #         {
    #             "code": 201,
    #             "message": "Role added successfully",
    #             "role": new_role.json()
    #         }
    #     )

    def test_create_role_2(self):
        result = requests.post("http://127.0.0.1:5002/roles", json={
            "role_id" : 7,
            "role_name" : "test role 2",
            "role_description" : "testing role 2",
        }).json()

        self.assertEqual(result,
                {
                "code": 400,
                "error": "Missing or invalid key in the request body: " + str(e)
            }
        )

    def test_get_listing_by_id1(self):
        result = requests.get("http://127.0.0.1:5002/role-listings/123457").json()
        self.assertEqual(result,
            {
                "code": 200,
                "listing": {
                    "role_id": 234567891,
                    "role_listing_close": "Thu, 30 Nov 2023 00:00:00 GMT",
                    "role_listing_creator": 123456788,
                    "role_listing_desc": "Looking for new head of Talent Attraction!",
                    "role_listing_id": 123457,
                    "role_listing_open": "Wed, 20 Sep 2023 00:00:00 GMT",
                    "role_listing_source": 123456787,
                    "role_listing_ts_create": "Wed, 20 Sep 2023 00:00:00 GMT",
                    "role_listing_ts_update": "Wed, 20 Sep 2023 00:00:00 GMT",
                    "role_listing_updater": 123456788
                }
            }
        )

    def test_get_listing_by_id2(self):
        result = requests.get("http://127.0.0.1:5002/role-listings/696969").json()
        self.assertEqual(result,
            {
                "code": 404,
                "message": "Role listing not found."
            }
        )

    # def test_update_role_listing1(self):
    #     result = requests.put("http://127.0.0.1:5002/role-listings/123458", json={
    #         "role_id": 234567892,
    #         "role_listing_close": "Wed, 20 Dec 2023 00:00:00 GMT",
    #         "role_listing_creator": 123456788,
    #         "role_listing_desc": "Test change",
    #         "role_listing_id": 123458,
    #         "role_listing_open": "Wed, 20 Sep 2023 00:00:00 GMT",
    #         "role_listing_source": 123456789,
    #         "role_listing_ts_create": "Wed, 20 Sep 2023 00:00:00 GMT",
    #         "role_listing_ts_update": "Wed, 20 Sep 2023 00:00:00 GMT",
    #         "role_listing_updater": 123456788
    #     }).json()
    #     listing = Role_listing(
    #         role_id= 234567892,
    #         role_listing_close= "Wed, 20 Dec 2023 00:00:00 GMT",
    #         role_listing_creator= 123456788,
    #         role_listing_desc= "Test Change",
    #         role_listing_id= 123458,
    #         role_listing_open= "Wed, 20 Sep 2023 00:00:00 GMT",
    #         role_listing_source= 123456789,
    #         role_listing_ts_create= "Wed, 20 Sep 2023 00:00:00 GMT",
    #         role_listing_ts_update= "Wed, 20 Sep 2023 00:00:00 GMT",
    #         role_listing_updater= 123456788
    #     )
    #     self.assertEqual(result,
    #         {
    #             "code": 200,
    #             "message": "Role listing updated successfully", 
    #             "role_listing": listing.json()
    #         }
    #     )
    
    def test_update_role_listing2(self):
        result = requests.put("http://127.0.0.1:5002/role-listings/123458", json={
            "this is a": "negative test case"
        }).json()
        self.assertEqual(result,
            {
                "code": 400,
                "error": "Missing or invalid key in the request body: " + str(e)
            }
        )
    
    def test_filter_role_listing_by_skill1(self):
        result = requests.get("http://127.0.0.1:5002/filter-role-listings-by-skills?skill_ids=345678913,345678970").json()
        self.assertEqual(result,
            {
                "code": 200,
                "filtered_role_listings": [
                    {
                        "role_id": 234567891,
                        "role_listing_close": "Thu, 30 Nov 2023 00:00:00 GMT",
                        "role_listing_creator": 123456788,
                        "role_listing_desc": "Looking for new head of Talent Attraction!",
                        "role_listing_id": 123457,
                        "role_listing_open": "Wed, 20 Sep 2023 00:00:00 GMT",
                        "role_listing_source": 123456787,
                        "role_listing_ts_create": "Wed, 20 Sep 2023 00:00:00 GMT",
                        "role_listing_ts_update": "Wed, 20 Sep 2023 00:00:00 GMT",
                        "role_listing_updater": 123456788
                    },
                    {
                        "role_id": 234567895,
                        "role_listing_close": "Mon, 30 Oct 2023 00:00:00 GMT",
                        "role_listing_creator": 123456788,
                        "role_listing_desc": "Listing Desc",
                        "role_listing_id": 123460,
                        "role_listing_open": "Fri, 27 Oct 2023 00:00:00 GMT",
                        "role_listing_source": 123456786,
                        "role_listing_ts_create": "Wed, 25 Oct 2023 00:00:00 GMT",
                        "role_listing_ts_update": "Wed, 25 Oct 2023 00:00:00 GMT",
                        "role_listing_updater": 123456788
                    }
                ]
            }
        )

    def test_filter_role_listing_by_skill2(self):
        result = requests.get("http://127.0.0.1:5002/filter-role-listings-by-skills").json()
        self.assertEqual(result,
            {
                "code": 400,
                "error": "No skill_ids provided in query parameters"
            }
        )

    # def test_create_role_application1(self):
    #     new_role_application = Role_application(
    #         role_listing_id=123459,
    #         staff_id=123456786,
    #         role_app_status="withdrawn",
    #         role_app_ts_create="9999-01-01"
    #     )
    #     result = requests.post("http://127.0.0.1:5002/role-applications", json=new_role_application.json())
    #     self.assertEqual(result,
    #         {
    #             "code": 201,
    #             "message": "Role application added successfully",
    #             "role_application": new_role_application.json()
    #         }
    #     )

    def test_create_role_application1(self):
        result = requests.post("http://127.0.0.1:5002/role-applications", json={
            "this is a" : "negative test case"
        })
        self.assertEqual(result,
            {
                "code": 400,
                "error": "Missing or invalid key in the request body: 'role_listing_id'"
            }
        )

if __name__ == '__main__':
    unittest.main()