import unittest
from api_main import ApiGuiManager, BASE_URL


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
