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
            #Fill the funList dictionary
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


#def returnType():
#       for line in file_aux:
#           if line[:6] == 'define' and line[10:13] == 'fun':


def print__(sen):
    # If only a variable is given
    if len(sen) == 1:
        name = sen[0]
        varName = name + '_' + loc[-1]
        varType = varList[varName]
        suffix = 'print__' + name + ',,' + varType
    elif sen[0][0] == '"':
        suffix = 'print__' + ' '.join(sen) + ',,str'
    else:
        suffix = 'print__' + ' '.join(sen) + ',,' + exprType(sen)

    file_aux.write(suffix + "\n")


def exprType(sen):
    operators = ['+', '-', '*', '/']
    name = '_'.join([sen[0], loc[-1]])
    if name in varList:
        expType = varList[name]
    elif sen[0].isdigit():
        expType = 'int'
    elif sen[0][0] == '"':
        expType = 'str'
    elif sen[0] == 'True' or sen[0] == 'False':
        expType = 'bool'
    else:
        raise NameError("Variable '" + sen[0] + "' not declared")
    for word in sen[1:]:
        for fun in funList:
            if word in funList[fun][1]:
                argType = expType
                defType = funList[fun][1][word]
                if not defType:
                    funList[fun][1][word] = argType
                elif defType != argType:
                    types = defType + expType
                    raise ValueError("Invalid types :" + types)
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
                    types = expType_temp + expType_temp
                    raise ValueError("Invalid types :" + types)
    return expType


#def return__(sen):


def change__(sen):
    name = '_'.join([sen[0], loc[-1]])

    if name in varList:
        varList[name] += '_ref'
    else:
        raise NameError("Variable '" + sen[0] + "' not declared")

    suffix = sen[0] + ' := ' + ' '.join(sen[1:])
    file_aux.write('change__' + suffix + "\n")


def translate(line):
    line_ = line.strip('\n')
    words = line_.split(' ')
    for i in range(len(words)):
        if i == 0:
            start = words[i].lower()
            sen = words[1:]
            # print(start, ' ',sen)
            if start == "define":
                define__(sen)
            elif start == "print":
                print__(sen)
            elif start == "return":
                return__(sen)
            elif start == "change":
                change__(sen)
            else:
                file_aux.write('#__' + line_ + "\n")


def caml(name):
    source = open(name + '.temp', 'rt')
    otp_path = os.path.join(cwd, "..", "Output", "") + name + '.ml'
    try:
        file_caml = open(otp_path, 'xt')
    except:
        os.remove(otp_path)
        file_caml = open(otp_path, 'xt')

    for line in source:
        print('##' + line, end='')
        line_ = line.strip('\n')
        inst, sen = line_.split('__')
        toto = sen.split(',,')
        # Define
        if inst == 'define':
            name_ = toto[0]
            if toto[1] == 'var':
                var = name_ + '_' + loc[-1]
                if varList[var].split('_')[-1] == 'ref':
                    camlLine = 'let ' + name_ + ' = ref ' + toto[2] + ' in '
                else:
                    camlLine = 'let ' + name_ + ' = ' + toto[2] + ' in '
            else:
                args = toto[2].split(';')
                curry = ' '.join(args)
                camlLine = 'let ' + name_ + ' ' + curry + ' = '
        # Print
        elif inst == 'print':
            type_ = toto[-1]
            if type_ == 'str':
                camlLine = 'print_string(' + toto[0] + ');'
            elif type_ == 'int' or type_ == 'int_ref':
                camlLine = 'print_int(' + toto[0] + ');'
            else:  # Should be useless
                camlLine = line_
        else:
            camlLine = line_

        print(camlLine)
        file_caml.write(camlLine + '\n')

    file_caml.close()
    source.close()
    os.remove(name + '.temp')

    print('Output ' + name + '.ml has been created in ../Output')


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