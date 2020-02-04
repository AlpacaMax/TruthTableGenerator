'''
    Filename: truthTableGen.py
    Author: AlpacaMax
    Purpose: Generate latex code of a truth table according to the user input
'''

priority = {
    'and' : 0,
    'or' : 0,
    'not' : 1,
    '->' : 1,
}

def to_postfix(expr):
    expression = expr.replace("\\wedge", "and").replace("\\vee", "or").replace("\\neg", "not").replace("\\rightarrow", "->").split()
    token_stack = []
    result = ""

    for token in expression:
        if (token in priority):
            #print(token)
            if (len(token_stack) > 0 and token_stack[-1] not in '()' and priority[token] <= priority[token_stack[-1]]):
                result += token_stack.pop() + ' '
            token_stack.append(token)
        elif (token == '('):
            token_stack.append(token)
        elif (token == ')'):
            while (token_stack[-1] != '('):
                result += token_stack.pop() + ' '
            token_stack.pop()
        else:
            result += token + ' '
    
    while (len(token_stack) > 0):
        result += token_stack.pop() + ' '

    return result

def evaluate(postfix_expr, values):
    for key in values:
        postfix_expr = postfix_expr.replace(key, values[key])

    expression = postfix_expr.split()

    stack = []
    for token in expression:
        if (token == "and"):
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = int(arg1) and int(arg2)
            stack.append(str(result))

        elif (token == "or"):
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = int(arg1) or int(arg2)
            stack.append(str(result))
        
        elif (token == "not"):
            arg = stack.pop()
            result = not int(arg)
            result = result * 1
            stack.append(str(result))
        
        elif (token == "->"):
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = (not int(arg1)) or int(arg2)
            result = result * 1
            stack.append(str(result))
        
        else:
            stack.append(token)
    
    return bool(int(stack.pop()))

def permutation(bool_vars, values):
    def helper(bool_vars, values, index):
        if (index >= len(bool_vars)):
            yield None
        else:
            per_gen = helper(bool_vars, values, index + 1)
            values[bool_vars[index]] = "1"
            for i in per_gen:
                yield i

            per_gen = helper(bool_vars, values, index + 1)
            values[bool_vars[index]] = "0"
            for i in per_gen:
                yield i
    
    return helper(bool_vars, values, 0)

def get_truth_table(bool_vars, expressions):
    postfix_exprs = [to_postfix(expr) for expr in expressions]
    values = {}
    result = []

    for i in permutation(bool_vars, values):
        line = [bool(int(values[key])) for key in values]

        for expr in postfix_exprs:
            single_result = evaluate(expr, values)
            line.append(single_result)

        result.append(line)

    return result

def to_string(bool_vars, result):
    for i in range(len(result)):
        for j in range(len(result[i])):
            if (result[i][j]):
                result[i][j] = 'T'
            else:
                result[i][j] = 'F'

    header = bool_vars + expressions
    for i in range(len(header)):
        header[i] = '$' + header[i] + '$'
    
    full_table = result
    full_table.insert(0, header)

    for i in range(len(full_table)):
        full_table[i] = ' & '.join(full_table[i]) + "\\\\\n"
    
    full_table = "\\[\n\\begin{tabular}{" \
                + 'c'.join(['|'] * (len(header) + 1)) \
                + '}\n\\hline\n' \
                + '\\hline\n'.join(full_table) \
                + "\\hline\n\\end{tabular}\n\\]"

    return full_table

if __name__ == '__main__':
    '''
    expressions = [
        "\\neg x",
        "\\neg y",
        "x \\vee y",
        "x \\vee \\neg y",
        "( x \\vee y ) \\wedge ( x \\vee \\neg y ) \\wedge \\neg x"
    ]
    bool_vars = ['x','y']
    '''
    bool_vars = input("Enter all the boolean variables separated with spaces: ").split()
    expressions = []
    while (True):
        ask = input("Enter boolean expression, enter 'stop' to stop the query: ")
        if (ask == "stop"):
            break

        expressions.append(ask)

    result = get_truth_table(bool_vars, expressions)

    table = to_string(bool_vars, result)
    
    print()
    print(table)