import json
import logging
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


logger = logging.getLogger(__name__)


class TestController(unittest.TestCase):
    def initialize_controller(self):
        self.controller = Controller(
            controller_body=MagicMock(),
        )

    @patch("application.io.other_func.controllers.custom_fetch_url")
    def test_response(self, mock_custom_fetch_url):
        self.initialize_controller()
        self.controller.return_value = None
        fetcher_response = []
        inputs = []

        def fetch_generator():
            for item in fetcher_response:
                yield item, {"fetch_dummy_name": 0.0}

        mock_custom_fetch_url.side_effect = fetch_generator()

        # Call the read method
        response = self.controller.read(inputs)


class TestPublicKbSearchControllerAsync(unittest.IsolatedAsyncioTestCase):
    def initialize_controller(self):
        self.controller = Controller(
            controller_body=AsyncMock(),
        )

    @patch("application.io.other_func.controllers.custom_fetch_url")
    async def test_response(self, mock_custom_fetch_url):
        self.initialize_controller()
        self.controller.return_value = None
        mock_response = None
        fetcher_response = []
        inputs = []

        # Mock asynchronous read method
        async def mock_read(*args, **kwargs):
            return mock_response, ("mock_dummy_name", 0.0)

        self.controller.other_func.a_read = AsyncMock(wraps=mock_read)

        fetch_result = [(item, ("fetch_dummy_name", 0.0)) for item in fetcher_response]

        mock_custom_fetch_url.side_effect = fetch_result
        for value in fetch_result:
            mock_custom_fetch_url.return_value = value

        # Call the read method
        response = await self.controller.a_read(inputs)
        print(response.json())
