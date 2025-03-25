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
        self.height = 0
        self.width = 0
        self.depth = 0 # todo: include filename and path???
        self.objects = [] # for storing

    def __str__(self): # todo: property: size, height, width
        return f"\n{self.name}\ndepth: {self.depth}\nheight: {self.height}\nwidth: {self.width} \nobjects: \n" + "\n".join(str(obj) for obj in self.objects)

class DiagramObject : # todo this needs to change, object type is the first, rest is attributes silly goose

    def __init__(self): # todo: ymin, ymax etc etc
        self.objecttype = None
        self.truncated = None
        self.difficult = None
        self.attribs = {} #do this or no?
        self.boundary = [] # xmin, ymin, xmax, ymax

    def __str__(self) :
        return f"\n\t{self.objecttype} \n\t truncated: {self.truncated} \n\t difficult: {self.difficult} \n\t boundaries: \n\t\txmin: {int(self.boundary[0].text)}\n\t\tymin: {int(self.boundary[1].text)}\n\t\txmax: {int(self.boundary[2].text)}\n\t\tymax: {int(self.boundary[3].text)}" #todo: iterate through attribs

diagrams = {} #keys will be file names, values diagrams
invalidInputs = 0

def parsexml(xmlfile, diagram) :
    if os.path.basename(xmlfile)[:-4] in diagrams : #correct key??
        raise Exception(f"Invalid entry: {os.path.basename(xmlfile)[:-4]}.xml already loaded")
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    if root.find('.//size') is not None:
        sizetag = root.find('.//size') # todo: assuming perfect input???
        diagram.width = int(sizetag.find('width').text) # what if doesnt have this attrib??
        diagram.height = int(sizetag.find('height').text)
        diagram.depth = int(sizetag.find('depth').text)
    if root.find('.//object') is not None:
        for object in root.findall('.//object'):
            obj = DiagramObject()
            obj.objecttype = object.find('name').text
            obj.truncated = object.find('truncated').text
            obj.difficult = object.find('difficult').text
            for coord in object.find('bndbox'):
                obj.boundary.append(coord)
            diagram.objects.append(obj)
            # todo: add all the attribs??


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
                    print(len(diagrams), "diagram(s) loaded: ")
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






