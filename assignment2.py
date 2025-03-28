import sys
import os
import xml.etree.ElementTree as ET  # For parsing XML files

# Represents a diagram composed of height, width, depth, and objects extracted from an XML annotation.
class Diagram : #
    # Initializes a diagram with a given name and default dimensions and an empty object list.
    def __init__(self, name):
        self.name = name
        self._height = 0
        self._width = 0
        # Depth of the image (e.g., color channels); default is 0.
        self.depth = 0
        # List to store DiagramObject instances representing objects within the diagram.
        self.objects = []

    @property
    def area(self):
        return self._width * self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def __str__(self):
        return f'\n{self.name}\ndepth: {self.depth}\nheight: {self.height}\nwidth: {self.width}\narea: {self.area} \nobjects: \n' + '\n'.join(str(obj) for obj in self.objects)

# Represents a single object detected within a diagram, including its type, attributes, and bounding box.
class DiagramObject :

    # Initializes a DiagramObject with default values for type, truncated, difficult, and bounding box boundaries.
    def __init__(self):
        self.objecttype = None
        self._truncated = None
        self._difficult = None
        # Optional dictionary for storing additional attributes from the XML, if needed.
        self.attribs = {}
        # Bounding box coordinates of the object (xmin, ymin, xmax, ymax).
        self.boundary = {'xmin':None, 'ymin':None, 'ymax':None, 'xmax':None}# xmin, ymin, xmax, ymax
        self.area = 0

    @property
    def truncated(self):
        return self._truncated

    @truncated.setter
    def truncated(self, value):
        self._truncated = value

    @property
    def difficult(self):
        return self._difficult

    @difficult.setter
    def difficult(self, value):
        self._difficult = value

    # Provides a formatted string representation of the object, including its type, truncated/difficult flags, and boundaries.
    def __str__(self) :
        return f'\n\t{self.objecttype} \n\t truncated: {self.truncated} \n\t difficult: {self.difficult} \n\t boundaries: \n\t\txmin: {self.boundary["xmin"]}\n\t\tymin: {self.boundary["ymin"]}\n\t\txmax: {self.boundary["xmax"]}\n\t\tymax: {self.boundary["ymax"]}'

diagrams = {} #keys will be file names, values diagrams
invalid_inputs = 0

def parsexml(xmlfile, diagram) :
    if os.path.basename(xmlfile)[:-4] in diagrams : #correct key??
        raise Exception(f'Invalid entry: {os.path.basename(xmlfile)[:-4]}.xml already loaded')
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    if root.find('.//size') is not None:
        size_tag = root.find('.//size')
        diagram._width = int(size_tag.find('width').text)
        diagram._height = int(size_tag.find('height').text)
        diagram.depth = int(size_tag.find('depth').text)
    if root.find('.//object') is not None:
        for obj_element in root.findall('.//object'):
            obj = DiagramObject()
            obj.objecttype = obj_element.find('name').text
            obj.truncated = obj_element.find('truncated').text
            obj.difficult = obj_element.find('difficult').text
            for coord in obj_element.find('.//bndbox'):
                obj.boundary[coord.tag] = coord.text
            obj.area = (abs(int(obj.boundary['ymax']) - int(obj.boundary['ymin'])) * abs(int(obj.boundary['xmax']) - int(obj.boundary['xmin'])))
            diagram.objects.append(obj)

def main():
    global invalid_inputs

    # Ensure the program is run with exactly one command-line argument (the path to the XML directory).
    if len(sys.argv) != 2:
        print('Usage: python3 your_script.py </path/to/xml/folder/>')
        sys.exit(1)

    # Check if the provided argument is a valid directory path.
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print('Invalid directory')
        sys.exit(1)

    while True:
        input('Press Enter to continue...')

        print('''
        1. List Current Files
        2. List Diagrams
        3. Load File
        4. Display Diagram Info
        5. Search
        6. Statistics
        7. Exit''')

        response = input('\nYour selection: ').strip()

        match response:

            case '1':
                # List all .xml files in the specified directory.
                all_files = os.listdir(directory)
                print('\nEnclosed files: ') #filter out only xmls?
                counter = 1
                for xml in all_files:
                    if xml.endswith('.xml'):
                        print(' ',counter, '.', xml)
                        counter += 1
                continue

            case '2':
                # List all diagrams currently loaded into memory.
                if len(diagrams) == 0:
                    print('\n0 diagrams loaded.\n')
                else:
                    print(f'{len(diagrams)} diagram(s) loaded: ')
                    print(', '.join(diagrams.keys()))
                    print()
                continue

            case '3':
                # Load an XML file and parse its contents into a Diagram object.
                filename = input('Enter the filename to load (include ".xml")').strip()
                #check if file available, if not return
                path_to_file = directory + '/' + filename
                if not os.path.isfile(path_to_file): #at this point are we in directory or do I have to put the whole path here?
                    print('\nEntered document does not exist\n')
                elif not filename.endswith('.xml'):
                    print('\nInvalid doctype, only xml file parsing is available\n')
                else:
                    diagram = Diagram(filename[:-4])
                    try:
                        parsexml(path_to_file, diagram) # this will be our value
                        diagrams[filename[:-4]] = diagram
                        print(f'\n{filename} successfully loaded\n')
                    except Exception as e:
                        print(e)
                continue

            case '4':
                # Display the details of a specific loaded diagram.
                filename = input('Enter the filename to display: (include ".xml")').strip() #only those that are already loaded right?, specify what format to type name of diagram (w xml?)
                if filename[:-4] in diagrams:
                    print(diagrams[filename[:-4]])
                else:
                    print(f'{filename} not found in loaded diagrams')
                continue

            case '5':
                # Search diagrams by object type or dimensions and attributes.
                response_2 = input('Would you like to search by type (1) or by dimension (2)? ').strip()
                match response_2:
                    case '1':
                        search_type = input('Enter the object type: ').strip()
                        found = {}

                        for name, diagram in diagrams.items():
                            for obj in diagram.objects:
                                if obj.objecttype.lower() == search_type.lower():
                                    found[name] = diagram

                        if len(found) > 0:
                            print(f'\nFound {len(found)} diagrams: ')
                            print(', \n'.join(found.keys()))
                            print()
                        else:
                            print('No matching diagrams found')
                        continue
                    case '2':
                        print('\nSearch parameters \n---------------')
                        min_width = input('Min width (enter blank for 0): ').strip()
                        max_width = input('Max width (enter blank for max): ').strip()
                        min_height = input('Min height (enter blank for zero): ').strip()
                        max_height = input('Max height (enter blank for max): ').strip()

                        valid = False
                        while not valid:
                            truncated = input('Containing Truncated Object (yes/no/All): ').strip()
                            if truncated.lower() in ['y', 'yes', 'n', 'no', 'a', 'all']:
                                valid = True
                                continue
                            print('Invalid input, try again')

                        valid = False
                        while not valid:
                            difficult = input('Containing Difficult Object (yes/no/All): ').strip()
                            if difficult.lower() in ['y', 'yes', 'n', 'no', 'a', 'all']:
                                valid = True
                                continue
                            print('Invalid input, try again')

                        found = {}
                        matched = False

                        min_width = int(min_width) if min_width else 0
                        max_width = int(max_width) if max_width else float('inf')
                        min_height = int(min_height) if min_height else 0
                        max_height = int(max_height) if max_height else float('inf')
                        if truncated.lower() in ['y', 'yes']:
                            truncated = 1
                        elif truncated.lower() in ['n', 'no']:
                            truncated = 0

                        if difficult.lower() in ['y', 'yes']:
                            difficult = 1
                        elif difficult.lower() in ['n', 'no']:
                            difficult = 0

                        #search for diagram with matching parameters and object of corresponding truncated and difficult values
                        for name, diagram in diagrams.items():
                            if not (min_width <= diagram.width <= max_width):
                                continue
                            if not (min_height <= diagram.height <= max_height):
                                continue

                            matched = False  # reset per diagram

                            for obj in diagram.objects:
                                trunc_match = (truncated not in [0, 1]) or (int(obj.truncated) == truncated)
                                diff_match = (difficult not in [0, 1]) or (int(obj.difficult) == difficult)

                                if trunc_match and diff_match:
                                    matched = True
                                    break

                            if matched:
                                found[name] = diagram

                        if len(found) > 0:
                            print(f'\nFound {len(found)} diagrams: ')
                            print(', \n'.join(found.keys()))
                            print()
                        else:
                            print('No matching diagrams found')
                        continue

            case '6':
                # Display various statistics about the loaded diagrams and objects.
                valid = False
                while not valid:
                    stat = input('\nAvailable statistics: \n\t1) Number of loaded diagrams\n\t2) Total number of total objects\n\t3) Diagram Object Types (list names)\n\t4) Minimum and Maximum dimensions\n\t5) Minimum and Maximum object areas\nYour Selection: ').strip()
                    if 1 <= int(stat) <= 5:
                        valid = True
                    else:
                        print('Invalid input...')

                    if len(diagrams) == 0:
                        print("No Diagrams loaded, load diagrams to access statistics")

                    match stat:
                        case '1':
                            print(f'\nThere are currently {len(diagrams)} diagrams loaded.\n')
                            continue
                        case '2':
                            ctr = 0
                            for name, diagram in diagrams.items():
                                ctr += len(diagram.objects)
                            print(f'\nTotal of objects: {ctr}\n')
                            continue
                        case '3':
                            obj_types = []

                            for name, diagram in diagrams.items():
                                for obj in diagram.objects:
                                    if obj.objecttype not in obj_types:
                                        obj_types.append(obj.objecttype)
                            print('\nAll object types:')
                            for name in obj_types:
                                print(f'\t- {name}')
                            print()
                            continue
                        case '4':
                            min_w_diagram = 'none'
                            max_w_diagram = 'none'
                            min_h_diagram = 'none'
                            max_h_diagram = 'none'

                            min_width = float('inf')
                            max_width = 0
                            min_height = float('inf')
                            max_height = 0

                            # find minimal and maximal width and height diagram
                            for name, diagram in diagrams.items():
                                if diagram.width < min_width:
                                    min_w_diagram = name
                                    min_width = diagram.width
                                if diagram.width > max_width:
                                    max_w_diagram = name
                                    max_width = diagram.width
                                if diagram.height < min_height:
                                    min_h_diagram = name
                                    min_height = diagram.height
                                if diagram.height > max_height:
                                    max_h_diagram = name
                                    max_height = diagram.height
                            print(f'\nminimum width: {min_width} ({min_w_diagram}) \nmaximum width: {max_width} ({max_w_diagram}) \nminimum height: {min_height} ({min_h_diagram})\nmaximum height: {max_height} ({max_h_diagram})\n ')
                            continue

                        case '5':
                            min_diagram = 'None'
                            min_obj = 'None'
                            min_area = float('inf')
                            max_diagram = 'None'
                            max_obj = 'None'
                            max_area = 0

                            for name, diagram in diagrams.items():
                                for obj in diagram.objects:
                                    if obj.area < min_area:
                                        min_area = obj.area
                                        min_obj = obj.objecttype
                                        min_diagram = name
                                    if obj.area > max_area:
                                        max_area = obj.area
                                        max_obj = obj.objecttype
                                        max_diagram = name
                            print(f'\nMinimum and Maximum object areas: \n\tmin area: {min_area} ({min_obj} in {min_diagram})\n\tmin area: {max_area} ({max_obj} in {max_diagram})\n')
                            continue
                continue

            case '7':
                # Confirm and exit the program.
                valid = False
                while not valid:
                    confirmation = input('Are you sure you want to quit the program (Yes/No)? ').strip()
                    if confirmation.lower() in ['y', 'yes', 'n', 'no']:
                        valid = True
                        continue
                    print('Invalid entry'
                          )
                match confirmation.lower():
                    case 'y'|'yes':
                        print('Good bye…')
                        sys.exit()
                    case _:
                        continue

        if invalid_inputs >= 0:
            print(f'Invalid entry, try again (Warning {invalid_inputs + 1}/5)')
            invalid_inputs += 1
            if invalid_inputs == 5:
                print('Invalid entry limit reached, System will terminate')
                sys.exit(0)

main()
