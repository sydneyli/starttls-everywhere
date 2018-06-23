""" Tests for update.py """
import unittest
import mock

from starttls_policy import lint

class TestLint(unittest.TestCase):
    """Test Configuration update tool
    """
    def test_lint_contents(self):
        lol = ("{ \"a\": \"b\"\n"
               "  \"c\": 3,\n"
               "  \"d\": \"x\" }\n")
        self.assertRaises(ValueError, update.lint_contents, lol)

    def test_lint_file(self):
        lol = ("{ \"timestamp\": 0, \"expires\": 0 }")
        with mock.patch('starttls_policy.update.open', mock.mock_open(read_data=lol)):
            update.validate("fake_file")

    def test_pretty_print_out_of_bounds(self):
        # pylint: disable=protected-access
        lol = ("{ \"a\": \"b\"\n"
               "  \"c\": 3,\n"
               "  \"d\": \"x\" }\n")
        self.assertEqual("", update._pretty_print_relevant_lines(lol, 4, 4))

    def test_describe_json_decode_malformed(self):
        # pylint: disable=protected-access
        self.assertRaises(ValueError, update._describe_json_decode_error,
            "", ValueError("a different error message"))
        self.assertRaises(ValueError, update._describe_json_decode_error,
            "", ValueError("column line"))
        self.assertRaises(ValueError, update._describe_json_decode_error,
            "", ValueError("line nan column nan"))

if __name__ == '__main__':
    unittest.main()
