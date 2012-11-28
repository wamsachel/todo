#!/usr/bin/env python

import sys
import os

#TODO fix -c so that you can not add multiple checks
#TODO create a -h help message

USAGE = """Usage: todo [-lacurb] [-h help] <todo file> [options]
	-l [l]ist items will print the items in <todo file>
	-a [a]dd item(s), (e.g. todo <todo file> "Walk the dog")
        -c [c]heck item off of the <todo file>, needs item no. (e.g todo <todo file> 1)
	-u [u]ncheck item off the <todo file>, needs item no. (similar to -c option)
	-r [r]emove item off the <todo file>, neets item no. (similar to -c option)
	-b [b]uild todo list, in this case an infile is read in place of <todo file>, 
	   this file is scanned for lines containing the word TODO
	   The remainder of the line after TODO is counted as a todo item
	   The found todo items are written to a file specified in the options field.
 	   If no file is specified, then a file is automatically created called 'TODO'
	   (e.g. todo -b code.cpp code.todo)

	NOTE: options a,c,u,r take as an option the item no. in the todo list that will be modified accordingly.  
        However, if no item no. is specified, then the user will be asked to enter a item no.
	one per line, until a Ctrl-C is given 

	NOTE: The l option can be placed after all the other options in order
	to print the resulting todo file.
	(e.g. todo -al <todo file> "Walk the dog")
	 
"""

ACTION_OPTS = ['l','a','c','u','r','b'] #Holds the available, notice that -h is not included in this list 

ACTION = "l"            #ACTION will hold the program's instructed action (i.e. add, read, list, or print help)
LIST = False
TODOLIST = ""           #TODOLIST will hold the filename to the user's todo list
REMOVEINT = 0           #If action is [r]emoving or [c]hecking, then REMOVEINT will hold the todo number to remove or check
ITEMTODO = ""           #If action is adding, then ITEMTODO will hold the todo string to add to TODOLIST
INFILE = 0
OUTFILE = 0

def main():
        #Check Arguments
        check_args()
                                                       

        #Check for file 
        global INFILE
        if (os.path.exists (TODOLIST)):
                try:
                        INFILE = open(TODOLIST, "a+")
                except:
                        sys.exit("Error when opening " + TODOLIST)
        else:
                try:
                        INFILE = file(TODOLIST, "w")
                        INFILE = open(TODOLIST, "a+")
                except:
                        sys.exit("ERROR when attempting to create " + TODOLIST)
        #Handle -l ACTION
        if (ACTION == 'l'):
                 list_file ()
        
        if (ACTION == 'a'):
                add_item()
        if ((ACTION == 'r') | (ACTION == 'c') | (ACTION == 'u')):
                modify_item()

        if (ACTION == 'b'):
                build_todo_list()

        #Handle -h, print help message

        #All Actions have been taken, see if LIST is True, if so, run list_file 
        global LIST
        if (LIST):
                list_file()

def build_todo_list():
        global TODOLIST #Our 'infile' was already opened in main
        global ITEMTODO
        global INFILE
        global OUTFILE

        #Scan infile for the string 'TODO' if such a string exists, then copy the rest of the line down (get the line number of the file?)
        infile_lines = INFILE.readlines()
        todo_items = []
        for line in infile_lines:
                #See if TODO is found in line
                aStr = str(line)
                todo_index = aStr.find('TODO')
                if (todo_index != -1):
                        todo_items.append(aStr[(todo_index + 4):])
        print (str(len(todo_items)) + " TODO items have been found!")
        if (len(todo_items) < 1):
                print ("No TODO items were found")
                return
        try:
                if (ITEMTODO == ""):
                        OUTFILE = open ("TODO", "a+")  #TODO will be the default file
                else:
                        OUTFILE = open(ITEMTODO, "a+")
        except:
                sys.exit("ERROR when opening the out-file " + ITEMTODO)
        
        try:
                OUTFILE.writelines(todo_items)
        except:
                sys.exit ("ERROR when writing the found todo items to the out file")
                        
                       
        #Else append todo_items to ITEMTODO

def modify_item():
        global TODOLIST
        global INFILE
        global REMOVEINT
        global ACTION 

        todoItems = INFILE.readlines()
        #print(todoItems)
        if(REMOVEINT > 0):       #This means we're removing 1 item, and the item to be removed was specified as an argument
                print("Modifying item no. " + str(REMOVEINT) + ", of " + str(len(todoItems)))
                if ((REMOVEINT-1) >= len(todoItems) ):
                        sys.exit ("No such item no. exists! Use -l to see current list of items available")
                else:
                        if (ACTION == 'r'):
                                todoItems.pop((REMOVEINT-1))               
                        if (ACTION == 'c'):
                                todoItems[REMOVEINT-1] = ("X " + todoItems[REMOVEINT-1])
                        if (ACTION == 'u'):
                                if (todoItems[REMOVEINT-1][0:2] == "X "):
                                        todoItems[REMOVEINT-1]=todoItems[REMOVEINT-1][2:]
                                else:
                                        print("It appears that item no. " + str(REMOVEINT) + " was not checked to begin with!")
                                     
                        #print(todoItems)
                        write_items(todoItems)
        else:
                print ("Enter todo items to be modified (one per line, press Ctrl-C when done):")
                itemIndexList = []
                while (True):
                        try:
                                aString = raw_input(":")
                                itemIndexList.append(int(aString))
                        except KeyboardInterrupt: break
                        except EOFError: break
                        except:
                               sys.exit("ERROR when accepting input.  Remember, these values should only be integers")
                #Now the itemList must be sorted, then reveresed, so as the popping of the master list turns out right
                itemIndexList.sort()
                itemIndexList.reverse()
                for i in itemIndexList:
                        if ((i-1) >= len(todoItems) ):
                                print ("Item no. " + str(i) + " does not exist!  Use -l to see current list of items available")
                                #Perhaps the above print statement should be a sys.exit instead of a verbal warning
                        else:
                                if(ACTION == 'r'):
                                        todoItems.pop(i-1)
                                if (ACTION == 'c'):
                                        todoItems[i-1] = ("X " + todoItems[i-1])
                                if (ACTION == 'u'):
                                        if (todoItems[i-1][0:2] == "X "):
                                                todoItems[i-1]=todoItems[i-1][2:]
                                        else:
                                                print("It appears that item no. " + str(i) + " was not checked to begin with!")
                                     

                #print(todoItems)
                write_items(todoItems)
        INFILE.flush() #Not sure if needed, or if I should leave it in here to be safe

def write_items(itemList):
        global INFILE
        global TODOLIST
        INFILE.seek(0)
        INFILE.truncate()
        for item in itemList:
                try:
                       INFILE.writelines(item)
                except:
                       sys.exit("ERROR when attempting to write to " + TODOLIST)
        INFILE.flush()

def add_item():
        global TODOLIST
        global ITEMTODO
        global INFILE
        if (len(ITEMTODO) > 0):
                try:
                        INFILE.write(ITEMTODO + "\n")
                except:
                        sys.exit("ERROR when attempting to write to " + TODOLIST)
        else:
                #signal.signal(signal.SIGINT, sig_handler)               #the handler is defined below
                print ("Enter todo items to be added (one per line, press Ctrl-C when done):")
                
                while (True):
                        try:
                                aString = raw_input(":")
                                try:
                                        INFILE.write(aString + "\n")

                                except:
                                        sys.exit("ERROR when attempting to write to " + TODOLIST)
                               
                        except KeyboardInterrupt:
                                break

                        except EOFError:
                                break
                       
        INFILE.flush()


def list_file():
        global TODOLIST
        global INFILE
        global OUTFILE
        global ACTION
                        
        if (ACTION == 'b'):
                OUTFILE.seek(0)
        else:
                INFILE.seek(0)
        try:
                if (ACTION == 'b'):
                        contents = OUTFILE.readlines()
                else:
                        contents = INFILE.readlines()
        except:
                sys.exit("Error when attempting to read from " + TODOLIST)

        print ("TODO:\n")
        index = 1
        todo_items = 0
        completed_items = 0
        for line in contents:
                print (str(index) + ". " + line) 
                index += 1
                if (line[0] == 'X'):
                        completed_items += 1
                else:
                        todo_items += 1
        print( "(" + str(todo_items) + " items TODO, " + str(completed_items) + " items COMPLETED)" )


def check_args():
        if ( (len(sys.argv) < 3) | (len(sys.argv) > 4)):
                print (USAGE)
                exit()
        #Check arg 1, needs to be an option with -, also we only need one option
        if (sys.argv[1][0] != "-"):
                print (USAGE)
                exit()
        else:
                global ACTION 
                ACTION = sys.argv[1][1]
                #if ((ACTION != 'a') & (ACTION != 'r') & (ACTION != 'c') & (ACTION != 'l') & (ACTION != 'h') & (ACTION != 'u') & (ACTION != 'b')):
                if (not (ACTION_OPTS.__contains__(ACTION))): 
			print (USAGE)
                        exit()
                if (len(sys.argv[1]) == 3):
                        if (sys.argv[1][2] == 'l'):
                                global LIST
                                LIST = True

        #Check arg 2, treat as string
        global TODOLIST 
        TODOLIST = sys.argv[2]
        
        #Check for arg 3, if ACTION == 'a' then save arg 3 to ITEMTODO, if ACTION == 'r|c|u' then save arg 3 to REMOVEINT
        if (len (sys.argv) == 4):
                if ((ACTION == 'a')|(ACTION == 'b')):
                        global ITEMTODO 
                        ITEMTODO = sys.argv[3]
                if ((ACTION == 'r') | (ACTION == 'c') | (ACTION == 'u')):
                        try:
                                global REMOVEINT 
                                REMOVEINT = int(sys.argv[3])
                        except:
                                print ("With -r,-c or -u, arg 3 needs to be an integer value")
                                print (USAGE)
                                exit()



if __name__ == '__main__':
        main()

