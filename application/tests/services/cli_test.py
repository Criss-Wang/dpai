import unittest


class TestImport(unittest.TestCase):
    def test_import_run_rag_service_rest(self):
        try:
            from application.services.cli import run_rest
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == "__main__":
    unittest.main()
