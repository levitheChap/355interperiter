import logging

#when you turn it in switch it to this 
#
logging.basicConfig(level = logging.INFO)
#
#so you dont get debug messages 

#logging.basicConfig(level = logging.DEBUG)


STATIC_SCOPEING = False ##global variable to control scoping##

##---------PSDICT----------##
##using self made dictionary so it is easy to manage ##
## when switching from dynamic to static scopes##

class PSDict:
    """" PostScript dictionary"""
    def __init__(self):
        self.dict = {}
        self.parent = None ##for static scoping##

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]
    
    def __contains__(self, key):
        return key in self.dict

    def set_parent(self, parent):
        self.parent = parent

    def __repr(self):
        return f"PSDICT({self.dict})"
    
    def __str__(self):
        return f"PSDICT({self.dict})"



##-----------INTERPRITER CUSTOM EXEPTIONS----------##

class ParseFailed(Exception):
    """"A exeecption indicating that a parser fai to parse the input"""
    def __init__(self, message):
        super().__init__(message)

class TypeMismatch(Exception):
    """"A exeecption indicating that a type mismatch occured during function/operation invocation"""
    def __init__(self, message):
        super().__init__(message)

##---------------------------PARSER----------------------------------##
##these functions try to parse the input into different types##

#Booleaan Parser
def process_boolean(input):
    logging.debug(f"input to process_boolean: {input}")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed("can't parse input into boolean")
    

def process_number(input):
    logging.debug(f"input to process_number: {input}")
    try:
        float_value = float(input)
        if float_value.is_integer(): ##if it is an integer return as int##
            return int(float_value)
        else:##if it is a float return as float##
            return float_value
    except ValueError:
        raise ParseFailed("can't parse input into a number")
    
##--------------Process string constant-------------##
## this function tries to parse the input into a string constant##
## string constant is defined as anything inside paranthesis##
## example: (hello world) --> hello world ##
def process_string_constant(input):
    logging.debug(f"input to process_string_constant: {input}")
    if len(input) >= 2 and input[0] == '(' and input[-1] == ')':##must be true for string constant##
        inner = input[1:-1]##return the inside of the string constant(no paranthesis)##
        return [ord(c) for c in inner]##return list of ascii values##
    else:
        raise ParseFailed("(PSC)can't parse input into a string constant")
    

##supporting user supported variables/constants##

#PNC in debug messages means process name constant##
def process_name_constant(input):
    logging.debug(f"input to process_name_constant: {input}")
    if input.startswith('/'):
        return input
    else:
        raise ParseFailed("(PNC)can't parse input into a name constant")

##----------PROCESS CODE BLOCKS----------##
## makes a list of tokens from inside code block ##
## example { 1 2 add } --> ['1','2','add'] ##
def process_code_block(input):
    logging.debug(f"input to process_code_block is: {input}")
    if len(input) >= 2 and input[0] == '{' and input[-1] == '}':##must be true for code block##
        return input[1:-1].strip().split()##return the inside of the code block(no barces) and 
        ##slits line into tokens(list of strings)##
    else:
        raise ParseFailed("(PCB)can't parse input into a code block")


##do one for process boolean and another for numbers(just like boolean one)##

PARSERS = {
    process_boolean,
    process_number,
    process_name_constant,
    process_code_block,
    process_string_constant
}

##--------------PROCESS CONSTANTS-------------##
## this function tries to parse the input using all available parsers##
def process_constants(input):
    for parser in PARSERS:
        try:
            return parser(input)
        except ParseFailed as e:
            logging.debug(e)
            continue
    raise ParseFailed("could not parse input into any supported constant type"
    " (bool, number, name, code block, or string)")


#Global Stacks
op_stack = []##operation stacks is just a list of lists##
dict_stack = []##dict stacks is just a list of dictionaries.##
dict_stack.append(PSDict())##initialize with one dictionary##


##--------------IN BUILT OPERATIONS-------------##

##ARITHMETIC OPERATIONS##

##add operation##
def add_operations():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            res = op1 + op2
        except TypeError:
            raise TypeMismatch("types of operands don't match for operation 'add'")
        op_stack.append(res)
    else:
        raise TypeMismatch("not enough operands for operation 'add'")
    
##subtract operation##
def sub_operations():
    if len(op_stack) >= 2:
            op1 = op_stack.pop()
            op2 = op_stack.pop()
            try:
                res = op2 - op1
            except TypeError:
                raise TypeMismatch("(sub)types of operands don't match for operation 'sub'")
            op_stack.append(res)
    else:
            raise TypeMismatch("(sub)not enough operands for operation 'sub'")

##multiply operation##
def mul_operations():
    if len(op_stack) >= 2:
            op1 = op_stack.pop()
            op2 = op_stack.pop()
            try:
                res = op1 * op2
            except TypeError:
                raise TypeMismatch("types of operands don't match for operation 'mul'")
            op_stack.append(res)
    else:
            raise TypeMismatch("not enough operands for operation 'mul'")
    
##div operation##
def div_operations():
    if len(op_stack) >= 2:
            op1 = op_stack.pop()
            op2 = op_stack.pop()
            try:
                res = op2 / op1
            except TypeError:
                raise TypeMismatch("types of operands don't match for operation 'div'")
            op_stack.append(res)
    else:
            raise TypeMismatch("not enough operands for operation 'div'")

##mod operation##
def mod_operations():
    if len(op_stack) >= 2:
            op1 = op_stack.pop()
            op2 = op_stack.pop()
            try:
                res = op2 % op1
            except TypeError:
                raise TypeMismatch("types of operands don't match for operation 'mod'")
            op_stack.append(res)
    else:
            raise TypeMismatch("not enough operands for operation 'mod'")


##PRINTING OPERATION##
#print operation##    
def pop_print_operations():
    if len(op_stack) >= 1:
        ##check if top of stack is a list of ints (string constant)##
        if isinstance(op_stack[-1], list) and all(isinstance(i, int) for i in op_stack[-1]):
            op1 = op_stack.pop()
            string_value = ''.join(chr(i) for i in op1)
            print(f"({string_value})")
        else:###normal case##  
            op1 = op_stack.pop()
            print(op1)
    else:
            raise TypeMismatch("not enough operands for operation 'pop_print'")
    
##STACK OPERATIONS##

##pop operation##
##will remove the top element from the operation stack##
def pop_operations():
    if len(op_stack) >= 1:
        op_stack.pop()
    else:
        raise TypeMismatch("not enough operands for operation 'pop'")

##dup operation##
##will duplicate the top element from the operation stack##
def dup_operations():
    if len(op_stack) >= 1:
        op1 = op_stack[-1]
        op_stack.append(op1)
    else:
        raise TypeMismatch("not enough operands for operation 'dup'")

##exch operation##
##will exchange the top two elements from the operation stack##
def exch_operations():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1)
        op_stack.append(op2)
    else:
        raise TypeMismatch("not enough operands for operation 'exch'")

##copy operation##
def copy_operations():
    if len(op_stack) >= 1:
        n = op_stack.pop()
        if isinstance(n, int) and n >= 0:
            if len(op_stack) >= n:
                elements_to_copy = op_stack[-n:]  ##get the top n elements##
                op_stack.extend(elements_to_copy) ##add them to the top of the stack##
            else:
                raise TypeMismatch("not enough operands to copy from operation stack")
        else:
            raise TypeMismatch("operand for 'copy' must be a non-negative integer")
    else:
        raise TypeMismatch("operand stack is empty for operation 'copy'")

##clear operation##
def clear_operations():
    op_stack.clear()

##count operation##
def count_operations():
    op_stack.append(len(op_stack))


##BOOLEAN OPERATIONS##
##equal operation
##pushes weather 2 obkects are equal
def eq_operations():
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op1 == op2)
    else:
        raise TypeMismatch("not enough operands for operation 'eq'")

##notEqual operation
##pushes weather 2 obkects are not equal
def ne_operation():
    # Same structure as eq, but checks inequality
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        op_stack.append(op2 != op1)
    else:
        raise TypeMismatch("ne - not enough operands")
    
##greaterthan operation
def gt_operation():
    if len(op_stack) >= 2:
        #checks if op2>op1
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            op_stack.append(op2 > op1)
        except TypeError:
            raise TypeMismatch("gt - incompatable operand types")
    else:
        raise TypeMismatch("gt - not enough operands")


##less_then operation
def lt_operation():
    if len(op_stack) >= 2:
        #checks if op2>op1
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        try:
            op_stack.append(op2 < op1)
        except TypeError:
            raise TypeMismatch("lt - incompatible operand types")
    else:
        raise TypeMismatch("lt - not enough operands")
    

def and_operation():
    
    ##Logical AND of top two boolean operands.
    ##Requires both operands to be bool. Pushes (op2 and op1).
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):##checks if both are bool
            op_stack.append(op2 and op1)
        else:
            raise TypeMismatch("and - operands must be booleans")
    else:
        raise TypeMismatch("and - not enough operands")


def or_operation():
    ##Logical OR of top two boolean operands.
    ##Requires both operands to be bool. Pushes (op2 OR op1).
    if len(op_stack) >= 2:
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        if isinstance(op1, bool) and isinstance(op2, bool):
            op_stack.append(op2 or op1)
        else:
            raise TypeMismatch("or - operands must be booleans")
    else:
        raise TypeMismatch("or - not enough operands")


def not_operation():
    ##Logical not of top two boolean operands.
    ##Requires operand to be bool. Pushes (not op1).
    if op_stack:
        op1 = op_stack.pop()
        if isinstance(op1, bool):
            op_stack.append(not op1)
        else:
            raise TypeMismatch("not - operand must be boolean")
    else:
        raise TypeMismatch("not - operand stack is empty")

##STRING OPERATIONS

def length_operation():  
    # Compute the 'length' of a string or dictionary.
    # For strings (list of ints): number of characters.
    # For PSDict: number of key/value pairs.

    if len(op_stack) >= 1:
        obj = op_stack.pop()
        if isinstance(obj, list) and all(isinstance(i, int) for i in obj):  # our internal string representation
            op_stack.append(len(obj))
        elif isinstance(obj, PSDict):
            op_stack.append(len(obj.dict))
        else:
            raise TypeMismatch("length - unsupported operand type")
    else:
        raise TypeMismatch("length - operand stack is empty")


def get_operation():
    
    # Retrieve an element from a string or dictionary.
    # - If obj is a list (string) and index is int, push obj[index].
    # - If obj is a PSDict and key exists, push dict[key].

    if len(op_stack) < 2:
        raise TypeMismatch("get - not enough operands")
    index_or_key = op_stack.pop()
    obj = op_stack.pop()

    # String (list) case: use integer index
    if isinstance(obj, list) and isinstance(index_or_key, int):
        try:
            op_stack.append(obj[index_or_key])
        except IndexError:
            raise TypeMismatch("get - string index out of range")

    # Dictionary case: PSDict with any hashable key
    elif isinstance(obj, PSDict):
        if index_or_key in obj:
            op_stack.append(obj[index_or_key])
        else:
            # Could use a more specific error type, but spec wants TypeMismatch
            raise TypeMismatch("get - key not found in dictionary")
    else:
        raise TypeMismatch("get - unsupported operand types")


def getinterval_operation():
   
    # Purpose:
    #     Extract a slice (sub-string) from a string.
    #     Takes a string, starting index, and count, then returns a new string.


    # Notes:
    #     - string is a list of ints
    #     - index and count are ints
    #     - result is also a list of ints
    if len(op_stack) < 3:
        raise TypeMismatch("getinterval - not enough operands")
    count = op_stack.pop()
    index = op_stack.pop()
    obj = op_stack.pop()

    if not (isinstance(obj, list) and isinstance(index, int) and isinstance(count, int)):
        raise TypeMismatch("getinterval - types must be (string, int, int)")
    if index < 0 or count < 0 or index + count > len(obj):
        raise TypeMismatch("getinterval - range out of bounds")

    # Slice is a shallow copy of the required portion
    op_stack.append(obj[index:index + count])


def putinterval_operation():

    # Purpose:
    #     Overwrite a portion of a destination string with a source string.
    #     No value is pushed back onto the stack (side-effect only).

    # Notes:
    #     - dst and src are both lists of ints (strings)
    #     - index is an int
    #     - mutates 'dst' in place

    if len(op_stack) < 3:
        raise TypeMismatch("putinterval - not enough operands")
    src = op_stack.pop()
    index = op_stack.pop()
    dst = op_stack.pop()

    if not (isinstance(dst, list) and isinstance(src, list) and isinstance(index, int)):
        raise TypeMismatch("putinterval - types must be (string, int, string)")
    if index < 0 or index + len(src) > len(dst):
        raise TypeMismatch("putinterval - range out of bounds")

    # Overwrite indices [index, index + len(src))
    for i, v in enumerate(src):
        dst[index + i] = v
    # PostScript putinterval leaves nothing on the operand stack

##--------------FLOW CONTROL OPERATIONS-------------##
## These functions implement PostScript-style control structures.
## They work on code blocks (lists of tokens) and booleans/numbers
## already on the operand stack, and execute code by calling process_input.

def if_operation():
    # Purpose:
    #   Conditionally execute a single code block.
    #   Implements:  bool  { code }  if
    #
    # Stack behavior:
    #   ... bool code  ->  ...
    if len(op_stack) < 2:
        raise TypeMismatch("if_operation- not enough operands")

    code = op_stack.pop()        # should be a code block (list of tokens)
    condition = op_stack.pop()   # should be a boolean

    if not isinstance(code, list):
        raise TypeMismatch("if_operation- code block must be a list")
    if not isinstance(condition, bool):
        raise TypeMismatch("if_operation- condition must be boolean")

    if condition:
        for token in code:
            process_input(token)


def ifelse_operation():
    # Purpose:
    #   Conditionally execute one of two code blocks.
    #   Implements:  bool  { true_code }  { false_code }  ifelse
    #
    # Stack behavior:
    #   ... bool true_code false_code  ->  ...
    if len(op_stack) < 3:
        raise TypeMismatch("ifelse_operation- not enough operands")

    false_code = op_stack.pop()  # executed if condition is False
    true_code = op_stack.pop()   # executed if condition is True
    condition = op_stack.pop()   # boolean

    if not (isinstance(true_code, list) and isinstance(false_code, list)):
        raise TypeMismatch("ifelse_operation- code blocks must be lists")
    if not isinstance(condition, bool):
        raise TypeMismatch("ifelse_operation- condition must be boolean")

    chosen = true_code if condition else false_code
    for token in chosen:
        process_input(token)


def repeat_operation():
    # Purpose:
    #   Repeat a code block a fixed number of times.
    #   Implements:  count  { code }  repeat
    #
    # Stack behavior:
    #   ... count code  ->  ...
    #
    # Notes:
    #   - count must be a non-negative integer.
    if len(op_stack) < 2:
        raise TypeMismatch("repeat_operation- not enough operands")

    code = op_stack.pop()   # code block (list)
    count = op_stack.pop()  # repeat count

    if not isinstance(code, list):
        raise TypeMismatch("repeat_operation- code block must be a list")
    if not isinstance(count, int) or count < 0:
        raise TypeMismatch("repeat_operation- count must be a non-negative integer")

    for _ in range(count):
        for token in code:
            process_input(token)


def for_operation():
    # Purpose:
    #   Iterate from an initial value to a limit using a given increment,
    #   executing a code block for each value.
    #   Implements:  initial  increment  limit  { code }  for
    #
    # Stack behavior:
    #   ... initial increment limit code  ->  ...
    #
    # Notes:
    #   - initial, increment, and limit must be numbers (int or float).
    #   - increment cannot be zero.
    if len(op_stack) < 4:
        raise TypeMismatch("for_operation- not enough operands")

    code = op_stack.pop()     # code block
    limit = op_stack.pop()    # numeric limit
    increment = op_stack.pop()# numeric increment
    initial = op_stack.pop()  # numeric starting value

    if not isinstance(code, list):
        raise TypeMismatch("for_operation- code block must be a list")
    if not all(isinstance(x, (int, float)) for x in (initial, increment, limit)):
        raise TypeMismatch("for_operation- initial, increment, and limit must be numbers")
    if increment == 0:
        raise TypeMismatch("for_operation- increment must be non-zero")

    current = initial

    # Choose the loop condition based on the sign of increment
    if increment > 0:
        condition = lambda c: c <= limit
    else:
        condition = lambda c: c >= limit

    while condition(current):
        # Each iteration, the current loop index is pushed onto the operand stack,
        # then the code block is executed.
        op_stack.append(current)
        for token in code:
            process_input(token)
        current = current + increment


##DICTIONARY OPERATIONS##
##support def operation##
def def_operations():
    ##print("\ndef operation called\n")
    if len(op_stack) >= 2:
            value = op_stack.pop()
            key = op_stack.pop()
            ##print("\ndef operation if 1 state end\n")
            if isinstance(key, str) and key.startswith('/'):
                key = key[1:]##remove the slash##
                dict_stack[-1][key] = value ##add to the dictionary stack##
                ##print("\ndef operation if 2 state end\n")
            else:
                op_stack.append(key)
                op_stack.append(value)
                ##print("\ndef operation else state end\n")
                raise TypeMismatch("def_operations- unable to define variable and value'")
    else:
            ##print("\ndef operation raise exception\n")
            raise TypeMismatch("def_operations- not enough operands for operation 'mul'")


def dict_operations():
    new_dict = PSDict()##create new dictionary## ##also when scope is set##
    if STATIC_SCOPEING:
        current_dict = dict_stack[-1]
        new_dict.set_parent(current_dict)
    op_stack.append(new_dict)


def begin_operations():
    if len(op_stack) >= 1:
        dict_obj = op_stack.pop()
        if isinstance(dict_obj, PSDict):
            dict_stack.append(dict_obj)
        else:
            raise TypeMismatch("begin_operations- top of opperand stack is not a dictionary")
    else:
        raise TypeMismatch("begin_operations- stack is empty")
    
def end_operations():
    if len(dict_stack) > 1:##prevent popping built in dictionary##
        dict_stack.pop()
    else:
        raise TypeMismatch("end_operations- can't pop the built-in dictionary")

##--------------REGISTER IN BUILT OPERATIONS-------------##
##this checks the last element in the dict stack and does the operations associated with it##

##creat more operations and register them here##

##this works by constantly looking at the last element in the dict stack##
##and if it is a key that matches the input it calls the associated function##

#arithmetic operations - DONE!
dict_stack[-1]["add"] = add_operations
dict_stack[-1]["sub"] = sub_operations
dict_stack[-1]["mul"] = mul_operations
dict_stack[-1]["div"] = div_operations
dict_stack[-1]["mod"] = mod_operations

#print operations - DONE
dict_stack[-1]["="] = pop_print_operations ##= print operation##

#stack operations - DONE
dict_stack[-1]["pop"] = pop_operations
dict_stack[-1]["dup"] = dup_operations
dict_stack[-1]["exch"] = exch_operations
dict_stack[-1]["copy"] = copy_operations
dict_stack[-1]["clear"] = clear_operations
dict_stack[-1]["count"] = count_operations

#boolean operations
dict_stack[-1]["eq"] = eq_operations
dict_stack[-1]["ne"] = ne_operation
dict_stack[-1]["gt"] = gt_operation
dict_stack[-1]["lt"] = lt_operation
dict_stack[-1]["and"] = and_operation
dict_stack[-1]["or"] = or_operation
dict_stack[-1]["not"] = not_operation

#dictionary operations
dict_stack[-1]["def"] = def_operations
dict_stack[-1]["dict"] = dict_operations
dict_stack[-1]["begin"] = begin_operations
dict_stack[-1]["end"] = end_operations

#string operations
dict_stack[-1]["length"] = length_operation
dict_stack[-1]["get"] = get_operation
dict_stack[-1]["getinterval"] = getinterval_operation
dict_stack[-1]["putinterval"] = putinterval_operation

#flow control operations
dict_stack[-1]["if"] = if_operation
dict_stack[-1]["ifelse"] = ifelse_operation
dict_stack[-1]["repeat"] = repeat_operation
dict_stack[-1]["for"] = for_operation


##--------------LOOKUP IN DICTIONARY-------------##
##this function looks up the input in the dictionary stack##

def lookup_in_dictionary(input):
    ##print("\nlookup_in_dictionary called &&&&&&&&&&&\n")
    for current_dict in reversed(dict_stack):##this is a loop that starts at end and walks backwards through list##
        logging.debug(current_dict)
        if input in current_dict:##looks through each dictionary for specidic key(input)##
            value = current_dict[input]##if found then get the value##
            if callable(value):##if it is a function ---> call it##
                value()
            
            elif isinstance(value, list): ##if it is a code block push it to the op stack##
                for item in value:
                    process_input(item)
                
            else:##if it is a single thing push it to the op stack##
                op_stack.append(value)
            return
    raise ParseFailed(f"(LiD)could not find {input} in the dictionary")
        

def lookup_in_static_dictionary(input, current_dict):
    ## instead of iterating through dict_stack one dictionary at a time##
    ## we follow the parent chain for static (lexical) scoping.        ##
    ##
    ## what should happen:
    ##   - Start in current_dict.
    ##   - If key is not found, move to current_dict.parent.
    ##   - Continue until key is found or parent is None.
    ##   - When found:
    ##       * If value is a callable, call it.
    ##       * If value is a code block (list), execute each token.
    ##       * Otherwise, push the value onto op_stack.
    ##   - If key is not found in any dictionary, raise ParseFailed.

    d = current_dict
    while d is not None:
        logging.debug(f"(Static-LiD) searching {d} for {input}")
        if input in d:
            value = d[input]

            # Built-in or user-defined function
            if callable(value):
                value()

            # Code block: list of tokens to be processed
            elif isinstance(value, list):
                for item in value:
                    process_input(item)

            # Constant value: push onto operand stack
            else:
                op_stack.append(value)
            return

        # Move up one lexical level
        d = d.parent

    # If not found in the parent chain, report failure
    raise ParseFailed(f"(Static-LiD)could not find {input} in static scope")



#--------------PROCESS INPUT-------------##
##this function process a single input##
def process_input(user_input):
    try:
        res = process_constants(user_input) ##try to parse input as constant(number,boolean)##
        op_stack.append(res)##if so add to stack## 
    except ParseFailed as e:##since it failed to parse as constant try to look it up in dictionary##
        logging.debug(e)
        try:
            if STATIC_SCOPEING:
                lookup_in_static_dictionary(user_input, dict_stack[-1])
            else:
                lookup_in_dictionary(user_input)
        except Exception as e:
            logging.error(f"(PD)could not find {user_input} in any dictionary: {e}")


##helper function that takes a list of ints(strings) and turns them into a string
##inside the Operation stack##
##ex: [104, 101, 108, 108, 111] --> "hello"##

def list_of_ints_to_string(int_list):
    logging.debug(f"(IntList->String) - input to list_of_ints_to_string: {int_list}")
    if isinstance(int_list, list) and all(isinstance(i, int) for i in int_list):
        try:
            s = ''.join(chr(i) for i in int_list)
            return f"({s})"
        except ValueError:
            return "Error: List contains invalid ASCII values."
    else:
        return "Error: Input is not a list of integers."
##the way the REPL works is that if the input starts with { it is treated as a code block
##otherwise it is split into tokens and each token is processed individually##

#REPL
def repl():
    while True:
        user_input = input("REPL> ")
        
        if user_input.strip().startswith('{'):##this is for code blocks##
            process_input(user_input)##it is alright to process code blocks one at a time##
        
        else:###normal case: split into tokens and process each one##
            tokens = user_input.split()
            for token in tokens:
                if token.lower() == 'quit':
                    return
                process_input(token)
        
        logging.debug(
            "Operation Stack: [" +
            ', '.join(
                list_of_ints_to_string(item) if isinstance(item, list) and all(isinstance(i, int) for i in item) else str(item)
                for item in op_stack
            ) + "]"
        )

if __name__ == "__main__":
    repl()

