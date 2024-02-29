import sys
import argparse 

pairs = []

seperators = ['$', ',', '{', '}', ';', '(', ')', '[', ']']
keywords = ['if', 'real', 'else', 'true', 'endwhile', 'integer', 'boolean', 'while', 'endif', 'print', 'return', 'scan', 'false', 'function']
operators = ['==', '!=', '>', '<', '<=', '=>', '+', '-', '*', '/', '=', '!']

def idFism(i, char):
    token = ""
    lexeme = ""
    determiner = True
    
    while determiner:
        ## l(l|d|_)*
        if char.isalpha() or char.isdigit() or char == '_':
            lexeme += char
            i += 1
            if i < len(content):
                char = content[i]
            else:
                if lexeme in keywords:
                    token = "Keyword"
                else:
                    token = "Identifier"
            
                pairs.append((lexeme, token))
            
                lexeme = ""
                token = ""
                determiner = False  # End of file reached
                
        ## this elif will make sure this FISM continues and does not end after
        ## just reading one word, only terminate if no more id or keywords are
        ## identified 
        elif char.isspace():
            # Check if the next character after whitespace is an alphabet,
            # then continue this ID FiSM
            if lexeme in keywords:
                token = "Keyword"
            else:
                token = "Identifier"
            
            pairs.append((lexeme, token))
            
            lexeme = ""
            token = ""
            
            ## continuing
            if i < len(content) and content[i].isalpha():
                char = content[i]  # Update char to next non-whitespace character
            else:
                determiner = False  # No more characters to process
        
        else:
            ## this is to handle cases where there is a seperator but no space
            ## ex) fahr) or return; etc etc 
            if char in seperators:
                if lexeme in keywords:
                    token = "Keyword"
                else:
                    token = "Identifier" 
                pairs.append((lexeme, token))
                return i-1
            ## this is an error handling, show the user the entire wrong syntax
            ## end when you read the entire string or word 
            while i < len(content) and content[i].isspace() != True:
                lexeme += content[i]
                i += 1    
            print("Wrong syntax found in " + lexeme) ## for the user to debug 
            determiner = False
    return i

def realDigitFism(i, char):
    lexeme = ""
    determiner = True
    
    while determiner:
        if char.isdigit() or char == '.':
            if content[i-1] == '-':
                lexeme += '-'
            if content[i-1] == '.' and content[i-2].isspace():
                lexeme += char
                while i + 1 < len(content) and content[i+1].isdigit():
                    i += 1
                    char = content[i]
                    lexeme += char
                print("Wrong syntax found in " + "." + lexeme)
                return i
            lexeme += char
            i += 1
            if i < len(content):
                char = content[i]
            else:
                if '.' in lexeme:
                    token = 'real'
                else:
                    token = 'digit'
                pairs.append((lexeme, token))
                determiner = False
        
        elif char.isspace():
            if '.' in lexeme:
                token = 'real'
            else:
                token = 'digit'
            pairs.append((lexeme, token))

            #this will handle the wrong syntax (nodigit.digit)
            if content[i+1] == '.':
                lexeme = ""
                i += 1
                
                while i + 1 < len(content) and content[i+1].isdigit():
                    i += 1
                    char = content[i]
                    lexeme += char
                print("Wrong syntax found in " + "." + lexeme)
                
            lexeme = ""
            if i + 1 < len(content) and (content[i + 1].isdigit() or content[i + 1] == '.'):
                determiner = True
                i += 1
                char = content[i]
            else:
                determiner = False
        else:            
            if char in seperators:
                if '.' in lexeme:
                    token = 'real'
                else:
                    token = 'digit'
                pairs.append((lexeme, token))
                return i-1
            while i < len(content) and content[i].isspace() != True:
                lexeme += content[i]
                i += 1
            print("Wrong syntax found in " + lexeme)
            determiner = False
    return i

def main():
    global content 
    global token
    global lexeme
    global i 
    
    comment = False
    i = 0
    
    ## use -h when running program to understand how to run 
    description = '''
    python3 la.py <file.txt>
    '''
    parser = argparse.ArgumentParser(description=description)
   
    parser.add_argument('<txt file>', help='a file that contains the text you to tokenize, such as a txt')
    args = parser.parse_args()
   
    filename = sys.argv[1]
    
    with open(filename,'r') as file:
        content = file.read()

    ##this is techincally the lexer() 
    while i < len(content):
        x = content[i]

        if x.isalpha():
           i = idFism(i, x)
        
        elif x.isdigit():
            i = realDigitFism(i, x)
            
        elif x in seperators:
            ##this if block ignores comments
            if x == '[' and content[i+1] == '*':
                comment = True
                while(comment):
                    i += 1
                    if content[i] == '*' and content[i+1] == ']':
                        comment = False
                        i += 1
            else:
                token = "Seperator"
                lexeme = x
                pairs.append((lexeme,token))
    
        elif x in operators:
            if x == '=':
                if content[i + 1] == '=':
                    lexeme = '=='
                    i += 1
                    token = "Operator"
                    pairs.append((lexeme, token))
                elif content[i+1].isspace():
                    lexeme = '='
                    i += 1
                    token = "Operator"
                    pairs.append((lexeme, token))
                elif content[i+1] == '>':
                    lexeme = '=>'
                    i += 1
                    token = "Operator"
                    pairs.append((lexeme, token))
                else:
                    print("invalid syntax at " + x + " " + content[i + 1])
                    i += 1
            elif x == '-' and content[i+1].isdigit():
                i += 1
                x = content[i]
                i = realDigitFism(i, x) 
            elif x == '!':
                if content[i + 1] == '=':
                    lexeme = '!='
                    i += 1
                    token = "Operator"
                    pairs.append((lexeme, token))
                else:
                    print("invalid syntax at " + x + " " + content[i + 1])
                    i += 1
            elif x == '<' and content[i+1] == '=':
                lexeme = '<='
                i += 1
                token = "Operator"
                pairs.append((lexeme, token))
            else:
                lexeme = x
                token = "Operator"
                pairs.append((lexeme, token))
        
        elif x == '.' and content[i+1].isdigit():
            i += 1
            x = content[i]
            i = realDigitFism(i, x) 
        
        elif not x.isspace():
            print("invalid syntax, try again " + x)
            break
        
        i += 1
    
    # final touches, write the results into a file called output.txt     
    with open(filename[:-4] + 'result.txt', 'w') as file:
        file.write("token\t\t\t\tlexeme\n")
        file.write("======================================\n")
        for x,y in pairs:
            file.write(y + "\t\t\t" + x + '\n')

if __name__ == "__main__":
    main()
