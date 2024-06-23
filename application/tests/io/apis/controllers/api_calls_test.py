import unittest
from unittest.mock import patch

import openai


class TestAPI(unittest.TestCase):
    context = None


class TestOpenaiConsumer(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_get_response_chat_completion(self, mock_create):
        mock_create.return_value.choices = [{"message": {"content": "Response text"}}]
        obj = OpenaiConsumer(chat_completion=True)
        obj.initialize_template(system_msg="System message", user_msg="User message")
        result = obj.get_response()
        self.assertEqual(result, "Response text")

    @patch("openai.Completion.create")
    def test_get_response_non_chat_completion(self, mock_create):
        mock_create.return_value.choices = [{"text": "Response text"}]
        obj = OpenaiConsumer(chat_completion=False)
        obj.initialize_template(system_msg="System message", user_msg="User message")
        result = obj.get_response()
        self.assertEqual(result, "Response text")


class TestAPIGatewayConsumer(unittest.TestCase):
    @patch("requests.get")
    @patch("requests.post")
    def test_get_response_success(self, mock_post, mock_get):
        mock_get.return_value.status_code = 200

        response_json = {"message": "Response text"}
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = response_json
        obj = APIGatewayConsumer(tenant="tenant")
        obj.initialize_template(system_msg="System", user_msg="Query: {query}")
        result = obj.get_response(query="Request text")
        self.assertEqual(result, "Response text")
        self.assertEqual(
            obj.format_prompt(query="Request text"),
            [
                {"role": "system", "content": "System"},
                {"role": "user", "content": "Query: Request text"},
            ],
        )

    @patch("requests.get")
    @patch("requests.post")
    def test_get_response_error(self, mock_post, mock_get):
        mock_get.return_value.status_code = 200

        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.text = "Error message"
        obj = APIGatewayConsumer(tenant="tenant", use_template=False)
        obj.initialize_template(system_msg="System", user_msg="Query: {query}")
        with self.assertRaises(openai.error.APIError):
            obj.get_response(query="Request text")


if __name__ == "__main__":
    unittest.main()
