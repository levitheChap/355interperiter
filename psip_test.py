from psip import ParseFailed, process_boolean, process_code_block
import pytest

class TestBooleanParsing:
    """" Test for boolean parsing"""

    def test_parse_true(self):
        result = process_boolean("true")
        assert result is True

    def test_parse_false(self):
        result = process_boolean("false")
        assert result is False

    def test_parse_invalid(self):
        with pytest.raises(ParseFailed):
            process_boolean("something")


class TestCodeBlockParsing:
    """" Test for code block parsing"""

    def test_parse_codeBlock(self):
        result = process_code_block("{ 1 add}")
        #assert len(result) == 2 #teacher result
        assert result == ['1', 'add'] #AI test result
        result = process_code_block("{1 2 add}")
        assert result == ['1', '2', 'add']

    def test_parse_invalid(self):
        with pytest.raises(ParseFailed):
            process_code_block("1 add}")
        with pytest.raises(ParseFailed):
            process_code_block("{1 add")
        with pytest.raises(ParseFailed):
            process_code_block("1 add")

##ADD MORE TESTS FOR OTHER PARSERS LIKE NUMBERS AND NAME CONSTANTS##
##ADD SO MANY TESTS SO YOU GET MOST CREDITS POSSIBLE##
