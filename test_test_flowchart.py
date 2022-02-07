from pyflowchart import Flowchart
with open('test_flowchart.py') as f:
    code = f.read()

fc = Flowchart.from_code(code)
print(fc.flowchart())
