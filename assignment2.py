import sys
import os
import xml.etree.ElementTree as ET    # for parsing XML files.
# import XPath                          # for extracting specific elements from XML.

'''
	•	CLI menu implementation.
	•	User input handling.
	•	Calls to relevant classes/functions.

If the program gets too large, structure it into:
	•	diagram.py – Contains Diagram and DiagramObject class definitions.
	•	xml_parser.py – Handles XML file reading and data extraction.
	•	menu.py – Manages CLI display and user interactions.
	•	utils.py – Helper functions for searching, filtering, and formatting output.

Test Files
	•	Include sample XML files for testing.
	•	test_data/ directory to store these XML files.
	
Make sure errors (ex: FNF) are handled gracefully, invalid entries
'''
class Diagram : # How do I get the whole layered aspect of it??
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.height = 0
        self.width = 0
        self.objects = [] # for storing

    def __str__(self): # todo: property: size, height, width
        return f"Diagram {self.name} has size {self.size}, height: {self.height}, width: {self.width} \nnodes: \n" + "\n".join(str(obj) for obj in self.objects)

class DiagramObject :
    def __init__(self, attribname, attribvalue): # todo: ymin, ymax etc etc
        self.attribute = attribname #todo take the size box for height and width info
        self.value = attribvalue
        self.children = []

    def __str__(self) :
        return f"{self.attribute}: {self.value}" #wrapper tags no value hmmmm what to do?

diagrams = {} #keys will be file names, values diagrams
invalidInputs = 0

# make array list of elements each of which has a list or set or smt that holds its "attributes"
# could you have any amount of branches off it?

# wrapper section below rest and ":"
def recursiveHelper(root, diagram): # how to count height and width
    for child in root:
        if type(child) is dict:
            #what here?? like when its more children and not a dictionary
            obj = DiagramObject(child.key, child.value)
            print(child.key, child.value) #debugging purposes
            diagram.objects.append(obj)
            diagram.size += 1
            #check if has sub library, is it possible for there to be a sublibrary in this case?
        else:
            print(child.tag, child.text) #debugging purposes
            obj = DiagramObject(child.tag, child.text) #is this correct (passing vars)
            diagram.objects.append(obj)
            diagram.size += 1
            recursiveHelper(child, diagram)
        # iterate similarly through all tags in bottom child

def parsexml(xmlfile, diagram) :
    if os.path.basename(xmlfile)[:-4] in diagrams : #correct key??
        raise Exception(f"Invalid entry: {os.path.basename(xmlfile)[:-4]}.xml already loaded")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    recursiveHelper(root, diagram)

def main():
    global invalidInputs

    if len(sys.argv) != 2:
        print("Usage: python3 your_script.py </path/to/xml/folder/>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print("Invalid directory")
        sys.exit(1)

    while True:
        input("Press Enter to continue...")

        print("""
        1. List Current Files
        2. List Diagrams
        3. Load File
        4. Display Diagram Info
        5. Search
        6. Statistics
        7. Exit""")

        response = input("\nYour selection: ")

        match response:
            case "1":
                allfiles = os.listdir(directory)
                print("\nEnclosed files: ") #filter out only xmls?
                counter = 1
                for xml in allfiles:
                    if xml.endswith('.xml'):
                        print(" ",counter, ".", xml)
                        counter += 1
                continue
            case "2":
                if len(diagrams) == 0:
                    print("0 diagrams loaded.")
                else:
                    print(len(diagrams), "diagrams loaded: ")
                    print(", ".join(diagrams.keys())) # remove line breaks todo: '' around each elem
                continue
            case "3":
                filename = input("Enter the filename to load: ")
                #check if file available, if not return
                pathtofile = directory + "/" + filename
                if not os.path.isfile(pathtofile): #at this point are we in directory or do I have to put the whole path here?
                    print("nuh uh! ")
                else:
                    diagram = Diagram(filename[:-4])
                    try:
                        parsexml(pathtofile, diagram) # this will be our value
                        diagrams[filename[:-4]] = diagram
                        print(filename + " successfully loaded")
                    except Exception as e:
                        print(e)
                continue
            case "4":
                filename = input("Enter the filename to display: ") #only those that are already loaded right?, specify what format to type name of diagram (w xml?)
                if filename[:-4] in diagrams:
                    print(diagrams[filename[:-4]])
                else:
                    print(f"{filename} not found in loaded diagrams")
                continue
            case "5":
                print("5")
                response2 = input("Would you like to search by type (1) or by dimension (2)? ")
                match response2:
                    case "1":
                        print("search by type...")
                        continue
                    case "2":
                        found = {}

                        print("\nSearch parameters \n---------------")
                        minwidth = input("Min width (enter blank for 0): ")
                        maxwidth = input("Max width (enter blank for max): ")
                        minheight = input("Min height (enter blank for zero): ")
                        maxheight = input("Max height (enter blank for max): ")
                        difficult = input("Difficult (yes/no/All): ")
                        truncated = input("Truncated (yes/no/All): ")

                        for diagram in diagrams:
                            if minwidth:
                                if diagram.width >= minwidth:
                                    continue #?
                                else:
                                    break #? onto next digram to check
                            if maxwidth:
                                if diagram.width <= maxwidth:
                                    continue # this be good, next param
                                else:
                                    break
                            if minheight:
                                if diagram.height >= minheight:
                                    continue
                                else:
                                    break
                            if maxheight:
                                if diagram.height <= maxheight:
                                    found[diagram.name] = diagrams[diagram]
                                else:
                                    break
                        if len(found) > 0:
                            print(f"Found {len(found)} diagrams: ")
                            print(", \n".join(diagrams.keys()))
                        else:
                            print("No matching diagrams found")
                        continue # todo: consistency in search format (.xml or no .xml)
                    # default???
            case "6":
                print("6")
                continue
            case "7":
                confirm = input("Are you sure you want to quit the program (Yes/No)? ")
                match confirm.lower():
                    case "y"|"yes":
                        print("Good bye…")
                        sys.exit()
                    case _:
                        continue

            # else say selection not valid, invalid inputs ++
        if invalidInputs == 0:
            print("That's not valid dingus")
        elif invalidInputs == 1:
            print("Again fuck face?...try again")
        elif invalidInputs == 2:
            print("Can you read? Theres 7 fucking options")
        invalidInputs += 1

        if invalidInputs == 3:
            print("No bueno, go fuck yourself")

main()






