#test flowchart
'''
This file requires pyflowchart to be installed.
after generating the mapping, need to feed to flowchart.js
in order to see the code change.
our goal is to create a simple http server which
generates flowchart from the code in one same HTML page
at every correct syntax checking.

'''
def foo(a, b):
    if a:
        print("a")
    else:
        for i in range(3):
            print("b")
    return a + b
