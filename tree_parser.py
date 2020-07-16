"""
TreeParser - count the number of trees in a ascii map of a garden
@author: Giuseppe Minardi
@date: 15/07/2020
"""
# Import standard libraries
from collections import defaultdict
import argparse

# Import package for fast computing
import numpy as np
from scipy.ndimage import label
#==============================================================================
def parse_argouments():
    """
    This function returns the path of the mapo given in input
    from the command line
    """
    parser = argparse.ArgumentParser(description="Count the number of trees in each garden given an ASCII garden map")
    parser.add_argument("path_to_map",
                        type=str,
                        help="File containing the map of the apartment to be parsed")
    return parser.parse_args().path_to_map

#==============================================================================
def map_parser(path):
    """
    This function takes in input the path of a map, opens the file and returns:
        full_map: list of each line of the original file
        labeled_image: numpy arrray with labelled gardens
        num_features: number of gardens found
    """

    # Initialize list where all the data will be kept
    binary_image = []
    full_map = []
    with open(path) as ascii_map:

        # read each line and creates a list with all the lines and a another list
        # where the walls are set to zero
        for line in ascii_map:
            full_map.append(line)
            line = [0 if char in "\\|-/+" else 1 for char in line]
            binary_image.append(line)
            # This function clusters all the  pixels of the same gardens
            #and assign them a label
            labeled_image, num_features = label(np.matrix(binary_image))
    return full_map, (labeled_image, num_features)

#==============================================================================
def parse_gardenName_treeNumber(full_map, labeled_image, num_features):
    """
    This function takes in input a list of strings (labeled_image),
    a np matrix as long as the previous list (labeled_image) and the number of
    gardens in the matrix. It returns a dictionary of the garden's name.
    Each value of the dictionary is a dictionary that contains the number
    of each type of trees.
    """
    #Initialize the dictionary that will contain the processed data
    garden_dict = {}
    #For each cluster we extract the name of the garden and the number of trees
    for label in range(1, num_features+1):
        #Initialize variables that will contain the name of the garden and the
        #dictionary that will contain the number of each type of tree
        tree_dict = defaultdict(int)
        name_garden = None
        for labeled_image_row_idx, labeled_image_row in enumerate(labeled_image):
            #Here we extract the index of the matrix where the label is present
            index_list = list(np.where(labeled_image_row == label)[0])
            # Avoid rows where the label is not present
            if len(index_list) > 0:
                # Slice of the string where the label is present
                query_string = full_map[labeled_image_row_idx]
                query_string_sliced = query_string[index_list[0]:index_list[-1]]
                # Check if the name of the garden is in this row
                start_name_garden = query_string_sliced.find(" (")
                end_name_garden = query_string_sliced.find(") ")
                # If we find the name of the garden we update the variable garden_name
                if start_name_garden != -1:
                    name_garden = query_string_sliced[start_name_garden+2:end_name_garden]
                # For each row we count the number of tree and we add it to the
                #previous number in order to get the total number at the end
                tree_dict["A"] += query_string_sliced.count("A")
                tree_dict["B"] += query_string_sliced.count("B")
                tree_dict["C"] += query_string_sliced.count("C")
                tree_dict["D"] += query_string_sliced.count("D")
        # Here we avoid to parse false gardens (artifact from the parsing)
        if name_garden: garden_dict[name_garden] = tree_dict
    return garden_dict
#==============================================================================

if __name__ == '__main__':
    #Take the file path given in input
    file_path = parse_argouments()

    full_map, (labeled_image, num_features) = map_parser(file_path)
    garden_dict = parse_gardenName_treeNumber(full_map, labeled_image,
                                           num_features)
    # We sort all the name of the gardens
    garden_dict_keys = list(garden_dict.keys())
    garden_dict_keys.sort()
    # Print the output
    total_dict = defaultdict(int)
    for key in garden_dict_keys:
        tree_dict = garden_dict[key]
        total_dict["A"] += tree_dict["A"]
        total_dict["B"] += tree_dict["B"]
        total_dict["C"] += tree_dict["C"]
        total_dict["D"] += tree_dict["D"]
    print(f"total:\nA: {total_dict['A']}, B: {total_dict['B']}, "
          f"C: {total_dict['C']}, D: {total_dict['D']}")

    for key in garden_dict_keys:
        tree_dict = garden_dict[key]
        print(f"{key}:\nA: {tree_dict['A']}, B: {tree_dict['B']}, "
              f"C: {tree_dict['C']}, D: {tree_dict['D']}")
