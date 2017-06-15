def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                (tokens,index,answer) = ePluMin(tokens,index,answer)
            elif tokens[index - 1]['type'] == 'MINUS':
                (tokens,index,answer) = ePluMin(tokens,index,answer)
            else:
                print 'Invalid syntax'
        index += 1
    return answer

def ePluMin(tokens,index,answer):
    n = 0.0
    if tokens[index - 1]['type'] == 'PLUS':
        (tokens,index,n) = eTimDiv(tokens,index,n)
        answer += n
    elif tokens[index - 1]['type'] == 'MINUS':
        (tokens,index,n) = eTimDiv(tokens,index,n)
        answer -= n
    return tokens,index,answer

def eTimDiv(tokens,index,n):
    n += tokens[index]['number']
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if index == len(tokens)-1:
                break;
            if tokens[index+1]['type'] == 'PLUS' or tokens[index+1]['type'] == 'MINUS': 
                break;
            elif tokens[index+1]['type'] == 'TIMES':
                index += 2
                if tokens[index]['type']!='NUMBER':
                    index += 1
                n *= tokens[index]['number']
            elif tokens[index+1]['type'] == 'DIVIDE':
                index += 2
                if tokens[index]['type']!='NUMBER':
                    index +=1
                n /= tokens[index]['number']
        else: index += 1
    return tokens,index,n

def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("1-2",-1)
    test("1*2*3",6)
    test("2+1*1.5",3.5)
    test("1/2",0.5)
    test("1/0.5",2)
    test("6/4+1",2.5)
    test("1+2*1.5*3/3-1",3)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
