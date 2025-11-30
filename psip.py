import logging

#when you turn it in switch it to this 
#
#logging.basicConfig(level = logging.INFO)
#
#so you dont get debug messages 

logging.basicConfig(level = logging.DEBUG)


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

##----------Parsers----------##

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
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        raise ParseFailed("can't parse input into a number")
    
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
    process_code_block
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
    raise ParseFailed("could not parse (input) input into bool or number")#will expand later##


#Global Stacks
op_stack = []##operation stacks is just a list of lists##
dict_stack = []##dict stacks is just a list of dictionaries.##
dict_stack.append(PSDict())##initialize with one dictionary##


##--------------IN BUILT OPERATIONS-------------##
##TO-DO  build in operations for the interpreiter##

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
    
    
def pop_print_operations():
    if len(op_stack) >= 1:
        op1 = op_stack.pop()
        print(op1)
    else:
            raise TypeMismatch("not enough operands for operation 'mul'")
    
##support def operation##
def def_operations():
    ##print("\ndef operation called\n")
    if len(op_stack) >= 2:
            value = op_stack.pop()
            key = op_stack.pop()
            ##print("\ndef operation if 1 state end\n")
            if isinstance(key, str) and key.startswith('/'):
                ##print("\ndef operation if 2 state start\n")
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

dict_stack[-1]["add"] = add_operations
dict_stack[-1]["mul"] = mul_operations
dict_stack[-1]["="] = pop_print_operations ##= print operation##
dict_stack[-1]["def"] = def_operations
dict_stack[-1]["dict"] = dict_operations
dict_stack[-1]["begin"] = begin_operations
dict_stack[-1]["end"] = end_operations



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
    pass
## instead of itterating through dict_stack one dictionary at a time##
## you need to use the parent chain i.e. if a dictionary dons not ##
## have the key you are looking for you have to look in the parrent ##
## and continue until you find it or reach the built in dictionary ##


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

##the way the REPL works is that if the input starts with { it is treated as a code block
##otherwise it is split into tokens and each token is processed individually##

#REPL
def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.strip().startswith('{'):##this is for code blocks##
            process_input(user_input)##it is alright to process code blocks one at a time##
        else:
            tokens = user_input.split()
            for token in tokens:
                if token.lower() == 'quit':
                    return
                process_input(token)
        logging.debug(f"Operation Stack: {op_stack}")

if __name__ == "__main__":
    repl()

