import unittest
from api_main import ApiGuiManager, ApiHistoryManager, BASE_URL


class TestApiHistoryManager(unittest.TestCase):
    def test_format_history_text_includes_expected_fields(self):
        manager = ApiHistoryManager(db_path="dummy.accdb")
        history = [{
            "ID": 1,
            "Timestamp": "2024-01-01 12:00:00",
            "Command": "GET",
            "Resource": "posts",
            "UserID": "7",
            "ResourceID": "1",
            "Title": "Test title",
            "Body": "Test body",
            "Successful": True,
        }]

        formatted = manager.format_history_text(history)

        self.assertIn("ID: 1", formatted)
        self.assertIn("Method: GET", formatted)
        self.assertIn("Resource: posts", formatted)
        self.assertIn("Successful: True", formatted)


class TestApiGuiManager(unittest.TestCase):
    def test_get_posts_with_user_id(self):
        url, kwargs = ApiGuiManager.build_request_data(
            method="GET",
            resource="posts",
            user_id="1",
            id_="",
            title="",
            body="",
        )

        self.assertEqual(url, f"{BASE_URL}/posts")
        self.assertEqual(kwargs, {"params": {"userId": "1"}})

    def test_post_posts_with_body(self):
        url, kwargs = ApiGuiManager.build_request_data(
            method="POST",
            resource="posts",
            user_id="1",
            id_="",
            title="A Test Post for Testing",
            body="This is a drill.",
        )

        self.assertEqual(url, f"{BASE_URL}/posts")
        self.assertEqual(kwargs, {
            "json": {
                "userId": "1",
                "title": "A Test Post for Testing",
                "body": "This is a drill.",
            }
        })

    def test_put_post_with_id(self):
        url, kwargs = ApiGuiManager.build_request_data(
            method="PUT",
            resource="posts",
            user_id="1",
            id_="1",
            title="Updated Test Title",
            body="New content for a new test!",
        )

        self.assertEqual(url, f"{BASE_URL}/posts/1")
        self.assertEqual(kwargs, {
            "json": {
                "userId": "1",
                "id": "1",
                "title": "Updated Test Title",
                "body": "New content for a new test!",
            }
        })

    def test_patch_post_with_id(self):
        url, kwargs = ApiGuiManager.build_request_data(
            method="PATCH",
            resource="posts",
            user_id="1",
            id_="1",
            title="Only a little bit.",
            body="",
        )

        self.assertEqual(url, f"{BASE_URL}/posts/1")
        self.assertEqual(kwargs, {
            "json": {
                "userId": "1",
                "id": "1",
                "title": "Only a little bit.",
            }
        })

    def test_delete_post(self):
        url, kwargs = ApiGuiManager.build_request_data(
            method="DELETE",
            resource="posts",
            user_id="",
            id_="1",
            title="",
            body="",
        )

        self.assertEqual(url, f"{BASE_URL}/posts/1")
        self.assertEqual(kwargs, {"params": {}})


if __name__ == "__main__":
    unittest.main(verbosity=2)
