from psip import ParseFailed, process_boolean, process_code_block, process_input, op_stack, add_operations
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

class TestAddOpperation:
    """" Test for add operation"""

    def test_add_operation(self):
        process_input("5")
        process_input("3")
        process_input("add")
        result = op_stack.pop()
        assert result == 8

    def test_add_operation_invalid(self):
        process_input("5")
        process_input("add")
        with pytest.raises(Exception):
            op_stack.pop()
##ADD MORE TESTS FOR OTHER PARSERS LIKE NUMBERS AND NAME CONSTANTS##
##ADD SO MANY TESTS SO YOU GET MOST CREDITS POSSIBLE##
##MAKE SURE TO TEST EDGE CASES AND INVALID INPUTS##
