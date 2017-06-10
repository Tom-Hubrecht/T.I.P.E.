def Init():
    # Global Variables
    global cwd
    global os

    global file_aux

    global funList  # Structure : {funName_funLoc : [funType, {arg : argType}]}
    global varList  # Structure : {varName_varLoc : varType}
    global loc

    # Import Modules
    import os

    # Global Variables Definition
    cwd = os.getcwd()
    funList = {}
    varList = {}
    loc = ['global']

    # Basic Functions Execution


def readInput():
    filename = input("Entrez le nom du fichier :\n>")
    path = os.path.join(cwd, "..", "Input", "") + filename + ".ipt"
    file = open(path, 'r')
    return file, filename


def exprType(sen):
    operators = ['+', '-', '*', '/','^']
    comparators = ['<', '>', '=<', '>=', '=', '!=']
    iterators = []
    for places in loc:
        if places.split('_')[0] == 'for':
            iterators.append(places.split('_')[1])

    # Do not look at {for, while, if}
    i = len(loc) - 1
    while loc[i].split('_')[0] in ['for', 'while', 'if']:
        i -= 1 

    funName = loc[i]
    funLoc = loc[i-1]
    fun = funName + '_' + funLoc
    name = '_'.join([sen[0], funName])    
    argsList = funList[fun][1]

    if name in varList:
        expType = varList[name].split('_')[0]
    elif sen[0] in funList[fun][1]:
        defType = funList[fun][1][sen[0]]
        if not defType:
            funList[fun][1][sen[0]] = exprType(sen[1:])
            expType = funList[fun][1][sen[0]]
        else:
            expType = defType
    elif sen[0].isdigit() or sen[0] in iterators:
        expType = 'int'
    elif sen[0][0] == '"':
        expType = 'str'
    elif sen[0] == 'True' or sen[0] == 'False':
        expType = 'bool'
    elif sen[0] in operators:
        expType = exprType(sen[1:])
    elif sen[0] in comparators:
        expType = exprType(sen[1:])
    else:
        raise NameError("Variable '" + sen[0] + "' not declared")
    for word in sen:
        if word in comparators:
            expType = 'comp'
    if expType == 'comp':
        return 'bool'
    else:
        for word in sen[1:]:
            for fun in funList:
                if word in funList[fun][1]:
                    argType = expType
                    defType = funList[fun][1][word]
                    if not defType:
                        funList[fun][1][word] = argType
                    elif defType != argType:
                        types = defType + ',' + expType
                        raise ValueError("Invalid types: " + types)
                elif word in iterators:
                    expType_temp = 'int'
                    if expType != 'int':
                        types = 'int' + ',' + expType
                        raise ValueError("Invalid types: " + types)
                elif not (word in operators):
                    name = '_'.join([word, loc[-1]])
                    if name in varList:
                        expType_temp = varList[name].split('_')[0]
                    elif word.isdigit():
                        expType_temp = 'int'
                    elif word[0] == '"':
                        expType_temp = 'str'
                    elif word == 'True' or sen[0] == 'False':
                        expType = 'bool'
                    else:
                        raise NameError("Variable '" + word + "' not declared")

                    if expType_temp != expType:
                        types = expType_temp + ',' + expType
                        raise ValueError("Invalid types: " + types)
    return expType

def adapt(sen):
    r = sen.copy()
    n = len(loc) - 1
    while loc[n].split('_')[0] in ['for', 'while', 'if']:
        n -= 1 
    for i in range(len(r)):
        if (exprType(r) == 'str') and (r[i] == '+'):
            r[i] = '^'
    for i in range(len(r)):
        name = '_'.join([r[i],loc[n]])
        if (name in varList) and (len(varList[name].split('_')) > 0) :
            r[i] = '!' + r[i]
    return r


def tabs(sen,inst):
    return t


def type__(var, expr, loc):
    type_ = exprType(expr)
    name = '_'.join([var, loc])

    if name not in varList:
        varList[name] = type_
    else:
        raise NameError("Variable '" + var + "' is already in use")


def define__(sen):
    name = sen[0]
    if sen[1].lower() == "as":
        if len(sen) > 3 and ' '.join([sen[2], sen[3]]) == "a function":
            class__ = "fun"
            if sen[4].lower() == "of":
                args = list(' '.join(sen[5:]).split(" and "))  # List arguments
                if not len(args):  # If no arguments are given
                    raise SyntaxError("Arguments expected")
            elif len(sen) > 4:  # If another word is after 'a function'
                raise SyntaxError("'of' expected")
            else:
                args = []
            suffix = 'define__' + name + ',,' + class__ + ',,' + ';'.join(args)
            loc.append(name)
            name = '_'.join([name, loc[-2]])
            # Fill the funList dictionary
            funList[name] = ['', {}]
            for arg in args:
                funList[name][1][arg] = ''
        else:
            class__ = "var"
            expr = sen[2:]
            type__(name, expr, loc[-1])
            suffix = 'define__' + name + ',,' + class__ + ',,' + ' '.join(expr)
    else:
        raise SyntaxError("'as' expected after 'define'")
    file_aux.write(suffix + "\n")


def print__(sen):
    # If only a variable is given
    if sen[0][0] == '"':
        suffix = ' '.join(sen) + ',,str'
    else:
        suffix = ' '.join(adapt(sen)) + ',,' + exprType(sen)
    file_aux.write('print__' + suffix + '\n')



def return__(sen):
    returnType = exprType(sen)
    inFun = False
    for i in range(len(loc)):
        if not(loc[len(loc)-i-1] in ['global','while','for','if']):
            fun = loc[len(loc)-i-1] + '_' + loc[len(loc)-i-2]
            inFun = True
            break
    if inFun:
        funList[fun][0] = returnType
    suffix = ' '.join(adapt(sen)) + ',,' + returnType
    file_aux.write('return__' + suffix + '\n')


def change__(sen):
    n = len(loc) - 1
    while loc[n].split('_')[0] in ['for', 'while', 'if']:
        n -= 1 
    funName = loc[n]
    name = '_'.join([sen[0], funName])
    if name in varList:
        if varList[name].split('_')[-1] != 'ref':
            varList[name] += '_ref'
    else:
        raise NameError("Variable '" + sen[0] + "' not declared")
    if sen[1] == 'to':
        if sen[0] in sen[2:]:
            l = sen[2:]
            l.remove(sen[0])
            if varList[name] == exprType(l) + '_ref':
                suffix = sen[0] + ',,' + ' '.join(adapt(sen[2:]))
            else:
                raise ValueError("Invalid types: " + varList[name] + ',' + exprType(l))
        else:
            if varList[name] == exprType(sen[2:]) + '_ref':
                suffix = sen[0] + ',,' + ' '.join(adapt(sen[2:]))
            else:
                raise ValueError("Invalid types: " + varList[name] + ',' + exprType(sen[2:]))
        file_aux.write('change__' + suffix + "\n")
    else:
        raise SyntaxError("'to' expected after 'change'")


def end__(sen):
    global loc
    if len(sen)>1:
        raise SyntaxError('Only one argument expected after "end"')
    elif sen[0] != loc[-1].split('_')[0]:
        if sen[0] in loc:
            raise SyntaxError(', '.join(loc[loc.index(sen[0])+1:]) + " need to be closed before " + sen[0])
        else:
            raise NameError(sen[0] + " doesn't exist so it couldn't be closed")
    else:
        loc = loc[:-1]
        file_aux.write('end__' + sen[0] + "\n")


def for__(sen):
    name = sen [0]
    print('for--' + str(sen))
    if len(sen) < 5 or (sen[1], sen[3]) != ('from', 'to'):
        raise SyntaxError('Incorrect for, need name from val to val')
    if exprType(sen[2]) != 'int' or exprType(sen[4]) != 'int':
        print(exprType(sen[4]) )
        raise SyntaxError('Integers must be used in start and end values')
    else:
        loc.append('for_' + sen[0])
        suffix = sen[0] + ',,' + sen[2] + ',,' + sen[4]
        file_aux.write('for__' + suffix + "\n")
    

def if__(sen):
#    print(sen)
    if exprType(sen) != 'bool':
        raise SyntaxError('Cannot use non boolean expression in if')
    else:
        loc.append('if')
        suffix = ' '.join(adapt(sen))
        file_aux.write('if__' + suffix + "\n")


def else__(sen):
    if loc[-1] != 'if':
        raise SyntaxError('Need to close ' + loc[-1].split('_'[0]) + ' before elseing')
    else:
        suffix = ' '.join(adapt(sen))
        file_aux.write('else__' + suffix + "\n")


def while__(sen):
    if exprType(sen) != 'bool':
        raise SyntaxError('Cannot use non boolean expression in while')
    else:
        loc.append('while')
        suffix = ' '.join(adapt(sen))
        file_aux.write('while__' + suffix + "\n")


def translate(line):
    line_ = line.strip('\n')
    words = line_.split(' ')
    start = words[0].lower()
    sen = words[1:]
    print(sen)
    if start == "define":
        define__(sen)
    elif start == "print":
        print__(sen)
    elif start == "return":
        return__(sen)
    elif start == "change":
        change__(sen)
    elif start == "end":
        end__(sen)
    elif start == "for":
        for__(sen)
    elif start == "if":
        if__(sen)
    elif start == "else":
        else__(sen)
    elif start == "while":
        while__(sen)
    else:
        file_aux.write('#__' + line_ + "\n")


def caml(name):
    global loc
    source = open(name + '.temp', 'rt')
    otp_path = os.path.join(cwd, "..", "Output", "") + name + '.ml'
    try:
        file_caml = open(otp_path, 'xt')
    except:
        os.remove(otp_path)
        file_caml = open(otp_path, 'xt')

    for line in source:
        t = len(loc)
        line_ = line.strip('\n')
        inst, sen = line_.split('__')
        args = sen.split(',,')
        # Define
        if inst == 'define':
            name_ = args[0]
            if args[1] == 'var':
                var = name_ + '_' + loc[-1]
                if not args[2].isdigit():
                    args[2] = '(' + args[2] + ')'
                if varList[var].split('_')[-1] == 'ref':
                    camlLine = 'let ' + name_ + ' = ref ' + '' + args[2] + ' in '
                else:
                    camlLine = 'let ' + name_ + ' = ' + '' + args[2] + ' in '
            else:
                args = args[2].split(';')
                curry = ' '.join(args)
                camlLine = 'let ' + name_ + ' ' + curry + ' = '
                loc.append(name_)
        # Print
        elif inst == 'print':
            type_ = args[-1]
            if type_ == 'str':
                camlLine = 'print_string(' + args[0] + ');'
            elif type_ == 'int':
                camlLine = 'print_int(' + args[0] + ');'
            elif type_ == 'float':
                camlLine = 'print_float(' + args[0] +');'
            camlLine += '\nprint_newline();'
        # End of
        elif inst == 'end':
            print(loc)
            objName = args[0]
            if objName in ['for','while']:
                camlLine = 'done;'
            elif objName == 'if':
                camlLine = 'end;'
            else:
                camlLine = ';'
            loc = loc[:-1]
            print('#  ' + str(loc))
            if loc == ['global']:
                camlLine += ';'
        # Return
        elif inst == 'return':
            camlLine = args[0]
        # Change
        elif inst == 'change':
            camlLine = args[0] + ' := ' + args[1] + ';'
        # For
        elif inst == 'for':
            loc.append('for')
            if not args[1].isdigit():
                args[1] = '(' + args[1] + ')'
            if not args[2].isdigit():
                args[2] = '(' + args[2] + ')'
            camlLine = 'for ' + args[0] + ' = ' + args[1] + ' to ' + args[2] + ' do'
        # If
        elif inst == 'if':
            loc.append('if')
            camlLine = 'if ' + args[0] + ' then' + '\nbegin'
        # Else
        elif inst == 'else':
            camlLine = 'end\nelse\nbegin'
        # While
        elif inst == 'while':
            loc.append('while')
            camlLine = 'while ' + args[0] + ' do'

        else:
            camlLine = line_
        file_caml.write(camlLine + '\n')

    file_caml.close()
    source.close()
    os.remove(name + '.temp')

    print('\nOutput ' + name + '.ml has been created in ../Output')


def main():
    global file_aux
    Init()
    file_src, src_name = readInput()
    try:
        file_aux = open(src_name + '.temp', 'xt')
    except:
        os.remove(os.path.join(cwd, src_name + '.temp'))
        file_aux = open(src_name + '.temp', 'xt')

    for line in file_src:
        translate(line)

    file_aux.close()
    file_src.close()

    caml(src_name)

# Start the program
main()
