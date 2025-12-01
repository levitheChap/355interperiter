# CPTS 355 – PostScript Interpreter (psip)

This project implements a small PostScript-like interpreter in Python.  
It supports:

- Numbers, booleans, name constants, string constants, and code blocks
- Arithmetic operators: `add`, `sub`, `mul`, `div`, `mod`
- Stack operators: `pop`, `dup`, `exch`, `copy`, `clear`, `count`
- Boolean operators: `eq`, `ne`, `gt`, `lt`, `and`, `or`, `not`
- String operators: `length`, `get`, `getinterval`, `putinterval`
- Dictionary operators: `dict`, `def`, `begin`, `end`
- Flow control operators: `if`, `ifelse`, `repeat`, `for`
- Dynamic and static (lexical) scoping, selectable via a global flag

The interpreter is implemented in `psip.py`.  
All automated tests are located in `psip_test.py`.

--------------------------------------------------------------------

## 1. How to Build and Run

### Prerequisites

- Python 3.10+ (tested with Python 3.13)
- `pytest` for executing the test suite

Install pytest:

    pip install pytest

### Creating a virtual environment (optional)

    python -m venv .venv
    .venv\Scripts\Activate.ps1   # PowerShell
    pip install pytest

--------------------------------------------------------------------

## 2. Running the Interpreter (REPL)

From the project directory:

    python psip.py

You should see:

    REPL>

Example usage:

    REPL> 1 2 add =
    3
    REPL> (hello) =
    (hello)
    REPL> quit

--------------------------------------------------------------------

## 3. Running the Test Suite

Run all unit tests with:

    pytest psip_test.py

This runs parser tests, arithmetic tests, stack operations, boolean tests,
string/dictionary operations, flow-control tests, dynamic/static scoping tests,
and full integration tests for `process_input`.

All tests should pass.

--------------------------------------------------------------------

## 4. Switching Between Dynamic and Static Scoping

Scoping behavior is controlled by the global flag `STATIC_SCOPEING`
defined near the top of `psip.py`.

Set:

    STATIC_SCOPEING = False   # dynamic scoping (default)
    # or
    STATIC_SCOPEING = True    # static (lexical) scoping

### Dynamic Scoping Example

    /x 10 def
    { x } /f exch def
    /x 20 def
    f =      % prints 20 (dynamic scope)

### Static Scoping Example

With STATIC_SCOPEING = True:

    /x 10 def
    { x } /f exch def
    /x 20 def
    f =      % prints 10 (static scope)

Dynamic scoping resolves names based on where functions are **called**.  
Static scoping resolves names based on where functions were **defined**.

--------------------------------------------------------------------

## 5. File Overview

- `psip.py` — full interpreter source code  
- `psip_test.py` — comprehensive test suite  
