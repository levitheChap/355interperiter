from traceback import print_stack
from psip import (ParseFailed, TypeMismatch, def_operations, process_boolean, process_number, process_name_constant,
    process_constants,process_code_block, process_input, op_stack, 
    add_operations, mul_operations, sub_operations, div_operations, mod_operations,
    pop_print_operations,
    pop_operations, dup_operations, exch_operations, copy_operations, clear_operations, count_operations,
    eq_operations, ne_operation, gt_operation, lt_operation, and_operation, or_operation, not_operation,
    length_operation, get_operation, getinterval_operation, putinterval_operation,
    dict_stack, PSDict, begin_operations, end_operations,
    lookup_in_dictionary, lookup_in_static_dictionary,

)
import psip
import pytest

##tests for parsers and operations##
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

##tests for process_number##
class TestNumberParsing:
    """" Test for number parsing"""

    def test_parse_integer(self):
        result = process_number("42")
        assert result == 42

    def test_parse_negative_integer(self):
        result = process_number("-7")
        assert result == -7

    def test_parse_invalid(self):
        with pytest.raises(ParseFailed):
            process_number("4.2.2")
        with pytest.raises(ParseFailed):
            process_number("notanumber")

## TESTS FOR process_name_constant ##

class TestNameConstantParsing:
    """ Test for name constant parsing"""
    ##valid name constant starts with a slash##
    def test_parse_name_constant_valid(self):
        result = process_name_constant("/x")
        assert result == "/x"
    
    ##invalid name constant does not start with a slash##
    def test_parse_name_constant_invalid(self):
        with pytest.raises(ParseFailed):
            process_name_constant("x")

## TESTS FOR process_constants ##
## 
#  of individual parsers ##
class TestConstantParsing:
    """ Tests for `process_constants` (integration of individual parsers) """
    # happy path tests for each type
    def test_parse_boolean_true_false(self):
        assert process_constants("true") is True
        assert process_constants("false") is False
    
    # happy path tests for numbers
    def test_parse_numbers(self):
        assert process_constants("42") == 42
        assert process_constants("-7") == -7
        assert process_constants("3.5") == 3.5
        # floats that are integer-valued should become int
        assert process_constants("3.0") == 3

    # happy path test for name constant
    def test_parse_name_constant(self):
        assert process_constants("/x") == "/x"

    # happy path test for code block
    def test_parse_code_block(self):
        assert process_constants("{1 2 add}") == ['1', '2', 'add']

    # invalid input
    def test_parse_invalid(self):
        with pytest.raises(ParseFailed):
            process_constants("not_a_token")


##tests for add operation##
class TestAddOperation:
    """" Test for add operation"""

    def test_valid_add_operation(self):
        process_input("5")
        process_input("3")
        process_input("add")
        result = op_stack.pop()
        assert result == 8

    ##invalid test case ex: not enough inputs to do add##
    def test_invalid_add_operation(self):
        process_input("5")
        with pytest.raises(TypeMismatch):
            add_operations()

##TESTS for sub_operations##
## - normal case: push 5 and 3 to op_stack, call sub_operations(), result should be 2
## - fail case: push only 5, call sub_operations(), expect TypeMismatch
## - edge case: push -2 and -3, call sub_operations(), result should be 1
class TestSubOperation:
    def test_valid_sub_operation(self):
        ##happy path##
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        process_input("3")
        process_input("sub")
        result = op_stack.pop()
        assert result == 2

    def test_invalid_sub_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        with pytest.raises(TypeMismatch):
            sub_operations()

    def test_edge_case_sub_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("-2")
        process_input("-3")
        process_input("sub")
        result = op_stack.pop()
        assert result == 1


## TESTS FOR mul_operations ##
## - normal case: push 2 and 3 to op_stack, call mul_operations(), result should be 6
## - type mismatch: push 2 and "abc" and expect TypeMismatch
class TestMulOperation:
    def test_valid_mul_operation(self):
        process_input("2")
        process_input("3")
        process_input("mul")
        result = op_stack.pop()
        assert result == 6
    
    def test_invalid_mul_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("2")
        with pytest.raises(TypeMismatch):
            mul_operations()

##TESTS FOR div_operations##
class TestDivOperation:
    ## - normal case: push 6 and 3 to op_stack, call div_operations(), result should be 2
    def test_valid_div_operation(self):
        process_input("6")
        process_input("3")
        process_input("div")
        result = op_stack.pop()
        assert result == 2

    ## - type mismatch: push 6 and expect TypeMismatch
    def test_invalid_div_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("6")
        with pytest.raises(TypeMismatch):
            div_operations()

    ## - edge case: push 5 and 0, expect ZeroDivisionError
    def test_edge_case_div_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        process_input("0")
        with pytest.raises(ZeroDivisionError):
            div_operations()


##TESTS FOR mod_operations##
class TestModOperation:
    ## - normal case: push 5 and 3 to op_stack, call mod_operations(), result should be 2
    def test_valid_mod_operation(self):
        process_input("5")
        process_input("3")
        process_input("mod")
        result = op_stack.pop()
        assert result == 2

    ## - type mismatch: push 5 and expect TypeMismatch
    def test_invalid_mod_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        with pytest.raises(TypeMismatch):
            mod_operations()

    ## - edge case: push 5 and 0, expect ZeroDivisionError
    def test_edge_case_mod_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        process_input("0")
        with pytest.raises(ZeroDivisionError):
            mod_operations()

## TESTS FOR pop_print_operations ##
## - when stack has one element, calling pop_print_operations() should pop it
##   (you can capture stdout with capsys fixture in pytest to check printed value)
## - when stack is empty, calling pop_print_operations() should raise TypeMismatch
class TestPopPrintOperation:
    def test_valid_pop_print_operation(self, capsys):
        process_input("42")
        process_input("=")
        captured = capsys.readouterr()
        assert "42" in captured.out

    def test_invalid_pop_print_operation(self):##fails since stack is empty##
        op_stack.clear()##make sure stack is empty##
        with pytest.raises(TypeMismatch): 
            pop_print_operations()##call


##TEST for pop_operations##
class TestPopOperation:
    def test_valid_pop_operation(self):
        process_input("100")
        pop_operations()
        assert len(op_stack) == 0  # Stack should be empty after pop

    def test_invalid_pop_operation(self):
        op_stack.clear()  # Ensure stack is empty
        with pytest.raises(TypeMismatch):
            pop_operations()


##TEST for dup_operations##
class TestDupOperation:
    def test_valid_dup_operation(self):##should duplicate the top element "100"##
        process_input("100")
        dup_operations()
        assert len(op_stack) == 2  # Stack should have two elements after dup
        assert op_stack[-1] == 100  # Top element should be the duplicated one

    def test_invalid_dup_operation(self):##should raise TypeMismatch since stack is empty##
        op_stack.clear()  # Ensure stack is empty
        with pytest.raises(TypeMismatch):
            dup_operations()

##TESTS FOR exch_operations##
class TestExchOperation:
    ## - valid case: push 1 and 2, call exch_operations(), stack should be [2, 1]
    def test_valid_exch_operation(self):
        process_input("1")
        process_input("2")
        exch_operations()
        assert len(op_stack) == 2
        assert op_stack[-1] == 1
        assert op_stack[-2] == 2

## - invalid case: push only 1, call exch_operations(), expect TypeMismatch
    def test_invalid_exch_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        with pytest.raises(TypeMismatch):
            exch_operations()

##TEST for copy_operations##
class TestCopyOperation:
    ##valid case: push 1, call copy_operations(), stack should be [1, 1]
    def test_valid_copy_operation(self):
        process_input("1")
        copy_operations()
        assert len(op_stack) == 2
        assert op_stack[-1] == 1
        assert op_stack[-2] == 1

    ##invalid case: push nothing, call copy_operations(), expect TypeMismatch
    def test_invalid_copy_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        with pytest.raises(TypeMismatch):
            copy_operations()
    
    ##edge case: push 3, but stack has only 2 elements, expect TypeMismatch
    def test_edge_case_copy_operation(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        process_input("2")
        process_input("3")
        with pytest.raises(TypeMismatch):
            copy_operations()


##TEST for clear_operations
class TestClearOperation:
    def test_valid_clear_operation(self):
        process_input("1")
        process_input("2")
        clear_operations()
        assert len(op_stack) == 0  # Stack should be empty after clear

    

##TEST for count_operations####
class TestCountOperation:
    def test_valid_count_operation(self):
        process_input("1")
        process_input("2")
        count_operations()
        result = op_stack.pop()
        assert result == 2  # There were 2 elements before count

    def test_edge_case_count_operation(self):
        op_stack.clear()  # Ensure stack is empty
        count_operations()
        result = op_stack.pop()
        assert result == 0  # Stack was empty before count

##BOOLEAN operations tests 
#test for eq 
class TestEqualOperations:
    def test_valid_eq_operation(self):
        process_input("1")
        process_input("1")
        eq_operations()
        result = op_stack.pop()
        assert result == True

    def test_invalid_eqoperation(self):
        process_input("1")
        with pytest.raises(TypeMismatch):
            eq_operations()

#test for ne_operation 
class TestNotEqualOperations:
    def test_valid_ne_operation(self):
        process_input("1")
        process_input("1")
        ne_operation()
        result = op_stack.pop()
        assert result == False

    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        with pytest.raises(TypeMismatch):
            ne_operation()

#test for gt_operation
class TestGreaterThenOperation:
    def testvalidGreaterthen(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("2")
        process_input("1")
        gt_operation()
        result = op_stack.pop()
        assert result == True

    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        with pytest.raises(TypeMismatch):
            gt_operation()

 #test for lt_operation   
class TestLessThenOperation:
    def test_valid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        process_input("2")
        lt_operation()
        result = op_stack.pop()
        assert result == True

    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("1")
        with pytest.raises(TypeMismatch):
            lt_operation()

#test for and_operation
class TestAndOperation:
    def test_valid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("true")
        process_input("true")
        and_operation()
        result = op_stack.pop()
        assert result == True


    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        with pytest.raises(TypeMismatch):
            and_operation()

#test for or_operation
class TestOROperation:
    def test_valid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("false")
        process_input("true")
        or_operation()
        result = op_stack.pop()
        assert result == True


    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        with pytest.raises(TypeMismatch):
            or_operation()

class TestnotOperation:
    def test_valid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("false")
        not_operation()
        result = op_stack.pop()
        assert result == True


    def test_invalid(self):
        op_stack.clear()##need to clear stack because of "lovely" trash from previous tests##
        process_input("5")
        with pytest.raises(TypeMismatch):
            not_operation()


##test for string ops

## TESTS FOR length_operation ##

## - normal string case: list of ints should return correct length
## - normal dict case: PSDict with N key/value pairs should return N
## - invalid type: non-string/non-dict should raise TypeMismatch
class TestLengthOperation:
    def test_valid_length_on_string(self):
        op_stack.clear()  ## ensure clean stack
        # Our "string" representation: list of ASCII codes
        ps_string = [72, 101, 108, 108, 111]  # "Hello"
        op_stack.append(ps_string)

        length_operation()
        result = op_stack.pop()
        assert result == 5

    def test_valid_length_on_dict(self):
        op_stack.clear()
        ps_dict = PSDict()
        ps_dict["x"] = 10
        ps_dict["y"] = 20
        op_stack.append(ps_dict)

        length_operation()
        result = op_stack.pop()
        assert result == 2  # two key/value pairs in the dict

    def test_invalid_length_type(self):
        op_stack.clear()
        op_stack.append(42)  # not a string or PSDict
        with pytest.raises(TypeMismatch):
            length_operation()


## TESTS FOR get_operation ##
## - string case: list and valid index should return correct element
## - dict case: PSDict and existing key should return correct value
## - missing key: PSDict and missing key should raise TypeMismatch
## - invalid types: non-string/non-dict should raise TypeMismatch
## - not enough operands: empty stack should raise TypeMismatch
class TestGetOperation:
    def test_valid_get_from_string(self):
        op_stack.clear()
        ps_string = [65, 66, 67]  # "ABC"
        op_stack.append(ps_string)
        op_stack.append(1)  # index 1 -> 66

        get_operation()
        result = op_stack.pop()
        assert result == 66

    def test_valid_get_from_dict(self):
        op_stack.clear()
        ps_dict = PSDict()
        ps_dict["x"] = 99
        op_stack.append(ps_dict)
        op_stack.append("x")

        get_operation()
        result = op_stack.pop()
        assert result == 99

    def test_get_missing_key_in_dict(self):
        op_stack.clear()
        ps_dict = PSDict()
        ps_dict["x"] = 99
        op_stack.append(ps_dict)
        op_stack.append("y")  # key does not exist

        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_invalid_types(self):
        op_stack.clear()
        op_stack.append(123)   # not a string or PSDict
        op_stack.append(0)
        with pytest.raises(TypeMismatch):
            get_operation()

    def test_get_not_enough_operands(self):
        op_stack.clear()
        with pytest.raises(TypeMismatch):
            get_operation()

## TESTS FOR getinterval_operation ##
## - normal case: valid string, index, count should return substring
## - invalid types: non-string or non-int index/count should raise TypeMismatch
## - out-of-bounds range: should raise TypeMismatch
## - not enough operands: empty stack should raise TypeMismatch
class TestGetIntervalOperation:
    def test_valid_getinterval(self):
        op_stack.clear()
        ps_string = [65, 66, 67, 68, 69]  # "ABCDE"
        op_stack.append(ps_string)
        op_stack.append(1)  # start at 'B'
        op_stack.append(3)  # length 3 -> "BCD"

        getinterval_operation()
        result = op_stack.pop()
        assert result == [66, 67, 68]

    def test_getinterval_invalid_types(self):
        op_stack.clear()
        op_stack.append("not_a_string")  # invalid string type
        op_stack.append(0)
        op_stack.append(1)
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_out_of_bounds(self):
        op_stack.clear()
        ps_string = [65, 66, 67]  # "ABC"
        op_stack.append(ps_string)
        op_stack.append(2)
        op_stack.append(5)  # 2 + 5 > 3 -> out of bounds
        with pytest.raises(TypeMismatch):
            getinterval_operation()

    def test_getinterval_not_enough_operands(self):
        op_stack.clear()
        with pytest.raises(TypeMismatch):
            getinterval_operation()


## TESTS FOR putinterval_operation ##
## - normal case: overwrite part of a destination string with a source string
## - invalid types: dst/src not lists or index not int should raise TypeMismatch
## - out-of-bounds index: should raise TypeMismatch
## - not enough operands: empty stack should raise TypeMismatch
class TestPutIntervalOperation:
    def test_valid_putinterval(self):
        op_stack.clear()
        dst = [65, 66, 67, 68, 69]  # "ABCDE"
        src = [88, 89]              # "XY"
        # Stack behavior for putinterval_operation:
        #   ... dst index src  ->  ...
        op_stack.append(dst)
        op_stack.append(2)   # overwrite starting at index 2 ("C")
        op_stack.append(src)

        putinterval_operation()
        # dst should now be "ABXYE" -> [65, 66, 88, 89, 69]
        assert dst == [65, 66, 88, 89, 69]

    def test_putinterval_invalid_types(self):
        op_stack.clear()
        dst = "not_a_list"   # invalid dst
        src = [88, 89]
        op_stack.append(dst)
        op_stack.append(0)
        op_stack.append(src)
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_out_of_bounds(self):
        op_stack.clear()
        dst = [65, 66, 67]  # "ABC"
        src = [88, 89, 90, 91]  # "WXYZ" (too long for index 2)
        op_stack.append(dst)
        op_stack.append(2)
        op_stack.append(src)
        with pytest.raises(TypeMismatch):
            putinterval_operation()

    def test_putinterval_not_enough_operands(self):
        op_stack.clear()
        with pytest.raises(TypeMismatch):
            putinterval_operation()


## TESTS FOR flow control: if, ifelse, repeat, for ##

class TestIfOperation:
    # valid case: condition true -> code block executes
    def test_if_true_executes_block(self):
        op_stack.clear()
        process_input("true")
        process_input("{ 1 2 add }")
        process_input("if")
        # code block should have run: 1 2 add -> 3
        assert len(op_stack) == 1
        result = op_stack.pop()
        assert result == 3

    # valid case: condition false -> code block skipped
    def test_if_false_skips_block(self):
        op_stack.clear()
        process_input("false")
        process_input("{ 1 2 add }")
        process_input("if")
        # nothing should be pushed
        assert len(op_stack) == 0


class TestIfElseOperation:
    # when condition is true, run true-branch code
    def test_ifelse_true_branch(self):
        op_stack.clear()
        process_input("true")
        process_input("{ 1 2 add }")        # true branch
        process_input("{ 10 20 add }")      # false branch
        process_input("ifelse")
        result = op_stack.pop()
        assert result == 3                  # true branch executed

    # when condition is false, run false-branch code
    def test_ifelse_false_branch(self):
        op_stack.clear()
        process_input("false")
        process_input("{ 1 2 add }")        # true branch
        process_input("{ 10 20 add }")      # false branch
        process_input("ifelse")
        result = op_stack.pop()
        assert result == 30                 # false branch executed


class TestRepeatOperation:
    # repeat 3 { 1 add } starting from 0 -> result should be 3
    def test_repeat_executes_block_n_times(self):
        op_stack.clear()
        process_input("0")                  # initial accumulator
        process_input("3")                  # repeat count
        process_input("{ 1 add }")          # code block
        process_input("repeat")
        result = op_stack.pop()
        assert result == 3

class TestForOperation:
    # for loop: 0 1 1 3 { add } for
    # logic:
    #   accumulator = 0
    #   loop i = 1,2,3
    #   each iter pushes i then "add" -> accumulator accumulates i
    # final result should be 1+2+3 = 6
    def test_for_loop_positive_increment(self):
        op_stack.clear()
        process_input("0")                  # accumulator
        process_input("1")                  # initial
        process_input("1")                  # increment
        process_input("3")                  # limit
        process_input("{ add }")            # code block
        process_input("for")
        result = op_stack.pop()
        assert result == 6

    # negative increment: 0 3 -1 1 { add } for
    # iterate i = 3,2,1; sum should still be 6
    def test_for_loop_negative_increment(self):
        op_stack.clear()
        process_input("0")                  # accumulator
        process_input("3")                  # initial
        process_input("-1")                 # increment
        process_input("1")                  # limit
        process_input("{ add }")            # code block
        process_input("for")
        result = op_stack.pop()
        assert result == 6

###tests for code block parser##
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

## TESTS FOR def_operations ##
class TestDefOperation:
## - happy path:
##   - push value 10
##   - push name constant "/x"
##   - call def_operations()
##   - check that dict_stack[-1]["x"] == 10
    def test_valid_def_operation(self):
        process_input("/x")
        process_input("10")
        process_input("def")
        assert dict_stack[-1]["x"] == 10

## - wrong key type:
##   - push value 10
##   - push "x" (no slash)
##   - call def_operations()
##   - expect TypeMismatch and operands restored to op_stack in same order
    def test_invalid_def_operation_wrong_key_type(self):
        op_stack.append("x") # no slash - invalid key type
        op_stack.append(10)  # value
        with pytest.raises(TypeMismatch):
            def_operations()
        # verify operands were restored to op_stack
        assert op_stack[-2] == "x"
        assert op_stack[-1] == 10

## - not enough operands:
##   - only push "/x", call def_operations(), expect TypeMismatch
    def test_invalid_def_operation_not_enough_operands(self):
        from psip import def_operations
        process_input("/x")
        with pytest.raises(TypeMismatch):
            def_operations()
    

## TESTS FOR dict_operations, begin_operations, end_operations ##
class TestDictOperation:
    """Test for dict_operations"""

    def test_valid_dict_operation(self):
        """Push a new dictionary onto dict_stack"""
        initial_stack_size = len(dict_stack)
        process_input("dict")  # creates new PSDict and pushes to op_stack
        # dict should be on op_stack now
        assert len(op_stack) > 0
        new_dict = op_stack.pop()
        assert isinstance(new_dict, PSDict)


    ##!!!!!!! uncommit later when static scoping is implemented##

    # def test_dict_operation_with_static_scoping(self):
    #     """Test dict_operations with STATIC_SCOPEING enabled"""
    #     from psip import dict_stack, PSDict, STATIC_SCOPEING
    #     import psip
        
    #     # Temporarily enable static scoping
    #     original_scoping = psip.STATIC_SCOPEING
    #     psip.STATIC_SCOPEING = True
        
    #     try:
    #         process_input("dict")
    #         new_dict = op_stack.pop()
    #         assert isinstance(new_dict, PSDict)
    #         # When static scoping is on, parent should be set
    #         assert new_dict.parent is not None
    #         assert new_dict.parent == dict_stack[-1]
    #     finally:
    #         psip.STATIC_SCOPEING = original_scoping
            
class TestBeginOperation:
    """Test for begin_operations"""

    def test_valid_begin_operation(self):
        """Push a PSDict, then call begin_operations to add it to dict_stack"""
        initial_dict_stack_size = len(dict_stack)
        
        # Create and push a new PSDict to op_stack
        new_dict = PSDict()
        op_stack.append(new_dict)
        
        # Call begin_operations - should pop from op_stack and push to dict_stack
        begin_operations()
        
        assert len(dict_stack) == initial_dict_stack_size + 1
        assert dict_stack[-1] is new_dict

    def test_invalid_begin_operation_empty_stack(self):
        """Call begin_operations with empty op_stack - should raise TypeMismatch"""
        with pytest.raises(TypeMismatch):## will fail if op_stack is empty##
            begin_operations()

    def test_invalid_begin_operation_non_dict(self):
        """Call begin_operations with non-PSDict on op_stack - should raise TypeMismatch"""
        with pytest.raises(TypeMismatch):
            begin_operations()
        op_stack.append(42)  # Push a number, not a PSDict
        with pytest.raises(TypeMismatch):## will fail since top of stack is not PSDict##
            begin_operations()

class TestEndOperation:
    """Test for end_operations"""
##valid case: push a PSDict onto dict_stack, call end_operations(), dict_stack size should decrease by 1
    def test_valid_end_operation(self):
        initial_dict_stack_size = len(dict_stack)
        new_dict = PSDict()
        dict_stack.append(new_dict)  # Manually push a PSDict onto dict_stack
        end_operations()
        assert len(dict_stack) == initial_dict_stack_size

##invalid case: call end_operations() when dict_stack has only one dictionary, should raise Index
    def test_invalid_end_operation_single_dict(self):
        # Ensure dict_stack has only one dictionary
        while len(dict_stack) > 1:##THIS WILL CLEAR THE STACK TO 1(THE BUILT-IN DICTIONARY)##
            dict_stack.pop()
        with pytest.raises(TypeMismatch):## will fail since only one dict in stack##
            end_operations()

## TESTS FOR lookup_in_dictionary (dynamic scoping) ##
class TestLookupInDictionary:
##vaid case: push a key that exists in one of the dictionaries in dict_stack, should return correct value
    def test_valid_lookup_in_dictionary(self):
        # Setup: push a dictionary with a known key-value pair onto dict_stack
        test_dict = PSDict()
        test_dict["y"] = 99
        dict_stack.append(test_dict)
        
         # Make sure operand stack is clean before test
        op_stack.clear()

        # Test lookup
        process_input("y")  # should find 'y' in the top dictionary
        assert op_stack[-1] == 99
        
        # Cleanup: remove the test dictionary from dict_stack
        dict_stack.pop()

##invalid case: push a key that does not exist, should raise KeyNotFound
    def test_invalid_lookup_in_dictionary(self):
        # Make sure operand stack is clean before test
        op_stack.clear()
        before_len = len(op_stack)

        # Process input for a key that does not exist
        process_input("nonexistent_key")

        # Assert: operand stack should remain unchanged
        after_len = len(op_stack)
        assert before_len == after_len
## TESTS FOR lookup_in_static_dictionary (static scoping) ##
class TestLookupInStaticDictionary:
    # basic parent-chain lookup should find key in parent
    def test_valid_lookup_uses_parent_chain(self):
        op_stack.clear()
        parent = PSDict()
        child = PSDict()
        child.set_parent(parent)

        parent["x"] = 10
        # child doesn't define "x" -> should find it in parent
        lookup_in_static_dictionary("x", child)
        assert op_stack.pop() == 10

    # child should shadow parent if both define the same key
    def test_child_shadows_parent(self):
        op_stack.clear()
        parent = PSDict()
        child = PSDict()
        child.set_parent(parent)

        parent["x"] = 10
        child["x"] = 20

        lookup_in_static_dictionary("x", child)
        assert op_stack.pop() == 20  # value from child, not parent

    # if key does not exist anywhere in chain, ParseFailed should be raised
    def test_lookup_not_found_raises(self):
        op_stack.clear()
        d = PSDict()
        with pytest.raises(ParseFailed):
            lookup_in_static_dictionary("missing_key", d)
        # stack should remain unchanged
        assert len(op_stack) == 0


## TESTS FOR process_input (integration-style tests) ##
class TestProcessInput:
    # when given "5", it should push 5 onto op_stack
    def test_process_input_push_number(self):
        op_stack.clear()
        process_input("5")
        assert len(op_stack) == 1
        assert op_stack[-1] == 5

    # when given "true", it should push True onto op_stack
    def test_process_input_push_boolean(self):
        op_stack.clear()
        process_input("true")
        assert len(op_stack) == 1
        assert op_stack[-1] is True

    # when given "add", it should call the add operation and modify op_stack
    def test_process_input_add_operation(self):
        op_stack.clear()
        process_input("2")
        process_input("3")
        process_input("add")
        # "add" should have been resolved via the dictionary and executed
        assert len(op_stack) == 1
        assert op_stack[-1] == 5

    # unknown token should leave op_stack unchanged (error is logged)
    def test_process_input_unknown_token_leaves_stack_unchanged(self):
        op_stack.clear()
        process_input("5")
        before = list(op_stack)
        process_input("nonexistent_token")
        after = list(op_stack)
        assert before == after

    # when STATIC_SCOPEING is False, process_input should call lookup_in_dictionary
    def test_process_input_uses_dynamic_lookup_when_static_false(self, monkeypatch):
        op_stack.clear()
        calls = {"dynamic": 0, "static": 0}

        def fake_dynamic(name):
            calls["dynamic"] += 1

        def fake_static(name, current_dict):
            calls["static"] += 1

        # monkeypatch into the psip module (where process_input looks)
        monkeypatch.setattr(psip, "lookup_in_dictionary", fake_dynamic)
        monkeypatch.setattr(psip, "lookup_in_static_dictionary", fake_static)

        original_static = psip.STATIC_SCOPEING
        psip.STATIC_SCOPEING = False
        try:
            process_input("someNameThatIsNotAConstant")
        finally:
            psip.STATIC_SCOPEING = original_static

        assert calls["dynamic"] == 1
        assert calls["static"] == 0

    # when STATIC_SCOPEING is True, process_input should call lookup_in_static_dictionary
    def test_process_input_uses_static_lookup_when_static_true(self, monkeypatch):
        op_stack.clear()
        calls = {"dynamic": 0, "static": 0}

        def fake_dynamic(name):
            calls["dynamic"] += 1

        def fake_static(name, current_dict):
            calls["static"] += 1

        monkeypatch.setattr(psip, "lookup_in_dictionary", fake_dynamic)
        monkeypatch.setattr(psip, "lookup_in_static_dictionary", fake_static)

        original_static = psip.STATIC_SCOPEING
        psip.STATIC_SCOPEING = True
        try:
            process_input("someNameThatIsNotAConstant")
        finally:
            psip.STATIC_SCOPEING = original_static

        assert calls["static"] == 1
        assert calls["dynamic"] == 0

##ADD MORE TESTS FOR OTHER PARSERS LIKE NUMBERS AND NAME CONSTANTS##
##ADD SO MANY TESTS SO YOU GET MOST CREDITS POSSIBLE##
##MAKE SURE TO TEST EDGE CASES AND INVALID INPUTS##
