import argparse
import os
import random
import string
import json
from typing import Type, Union, Dict

# chance to add [] value in key
EMPTY_DATA_CHANCE = 20

class ValueGenerator():
    # Function that generates random string value (combination of letters and number) up to the specified length by -l parameter 
    def generate_random_string(self, max_string_length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k = max_string_length))

    # Function that generates random integer within a specified range
    def generate_random_integer(self, min_value: int, max_value: int) -> int:
        return random.randint(min_value, max_value)

    # Function that generates random float within a specified range
    def generate_random_float(self, min_value: float, max_value: float) -> float:
        return random.uniform(min_value, max_value)

    # Function that generates random value
    def generate_random_value(self, data_type: str, max_string_length: int, is_root: bool) -> Type[Union[str, int, float]]:

        random_int = self.generate_random_integer(0, 100)
        if random_int < EMPTY_DATA_CHANCE and is_root:
            return None
        elif data_type == "string":
            return self.generate_random_string(max_string_length)
        elif data_type == "int":
            return self.generate_random_integer(0,100)
        elif data_type == "float":
            return self.generate_random_float(0.0,100.0)


class KeyValuePairGenerator:
      
    def __init__(self, key_file_dict: dict, value_generator: ValueGenerator):
        self.key_file_dict = key_file_dict
        self.value_generator = value_generator
    
    # is_root checks if recursion is in root object. If so, the value can be None and the key must be unique   
    def generate_random_KeyValue_pair(
        self, 
        num_lines: int, 
        max_nesting: int, 
        max_keys: int, 
        max_string_length: int, 
        keyFile_dict: dict, 
        is_root: bool
        ) -> Dict[str, Union[str, int, float, None, Dict]]:

        random_data = {}

        # Generate a random number of keys up to the maximum specified by the -m parameter
        num_keys = random.randint(1, max_keys)
        increasing_num = str(0)

        for i in range(num_keys):
            key = random.choice(list(keyFile_dict.keys()))
            data_type = self.keyFile_dict[key]

            if is_root:
                key += increasing_num

            # If the maximum level of nesting is 0, then its at the bottom level and random values can be generated for each key, up to the specified keys inside each value
            random_data[key] = self.value_generator.generate_random_value(data_type, max_string_length)

            # If the maximum level of nesting is greater than 0, then a random number of keys for the current level of nesting can be generated, up to the specified keys inside each value
            # and the function can be called recursively, to generate the values of each these keys
            if max_nesting > 0 and random_data[key] != None :
                random_data[key] = self.generate_random_KeyValue_pair(
                    num_lines, 
                    max_nesting-1, 
                    max_keys, 
                    max_string_length, 
                    keyFile_dict, 
                    False)

            increasing_num += str(1)

        return random_data


class DataGenerator():
    def __init__(self, key_value_pair_generator: KeyValuePairGenerator):
        self.key_value_pair_generator = key_value_pair_generator

    # Function that reads the given keyFile.txt and stores each lines key and its data type in a dictionary
    def read_keyFile_and_store_keys_and_their_data_types(self, keyFile: str) -> dict:
        keyFile_dict = {}

        # Open the file and read its lines
        with open(keyFile, "r") as keyFile:
            lines = keyFile.readlines()

            # Read each line of the file and store the key and its data type in the dictionary
            for each_line in lines:

                # Check if the line contains two parts (key and data type)
                if len(each_line.strip().split(" ")) == 2:
                    key_name, data_type = each_line.strip().split()
                    keyFile_dict[key_name] = data_type
                else:
                    # Skip the current iteration of the loop if the line does not contain two parts and ignore that line
                    continue
            
        # Return the dictionary
        return keyFile_dict

    # Function that generates and writes the data to a file
    def generate_and_write_data_to_file(
        self, 
        num_lines: int, 
        max_nesting: int, 
        max_keys: int, 
        max_string_length: int, 
        keyFile: str
        ):

        # Read the key file and store the keys and their data types in a dictionary
        keyFile_dict = self.read_keyFile_and_store_keys_and_their_data_types(keyFile)
        
        # If keyFile dictionary is empty, then return
        if not keyFile_dict:
            return

        with open("dataToIndex2.txt", "w") as generated_file: # Open the output file for writing

            for i in range(num_lines):
                # Generate a random key-value pair
                generated_data = self.key_value_pair_generator.generate_random_KeyValue_pair(
                    num_lines, 
                    max_nesting, 
                    max_keys, 
                    max_string_length, 
                    keyFile_dict, 
                    True
                    )
                generated_file.write(json.dumps(generated_data) + "\n") # Write the data to the output file in JSON format

        generated_file.close() # Close the output file


def parse_dataCreation_arguments():

    dataCreation_parser = argparse.ArgumentParser(description="Data Creation Parser")
    dataCreation_parser.add_argument(
        "-k", 
        type=txt_file, 
        required=True, 
        help="File containing a space-separated list of key names and their data types"
        )
    dataCreation_parser.add_argument(
        "-n", 
        type=int_type, 
        required=True, 
        help="Number of lines (i.e. separate data) to generate"
        )
    dataCreation_parser.add_argument(
        "-d", 
        type=int_type, 
        required=True, 
        help="Maximum level of nesting"
        )
    dataCreation_parser.add_argument(
        "-l", 
        type=int_type, 
        required=True, 
        help="Maximum length of a string value"
        )
    dataCreation_parser.add_argument(
        "-m", 
        type=int_type, 
        required=True, 
        help="Maximum number of keys inside each value"
        )
    dataCreation_args = dataCreation_parser.parse_args()
    return dataCreation_args

# This code will first check if the file has a .txt extension. 
def txt_file(arg):

    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError(f"Error: {arg} does not exist. Please provide an existing file!")
    elif not os.path.splitext(arg)[1] == ".txt":
        raise argparse.ArgumentTypeError(f"Error: {arg} is not a text file. Please provide a txt file as argument!")
    return arg

def int_type(arg):

    if not arg.isdigit():
        raise argparse.ArgumentTypeError(f"Error: {arg} is not an integer. Please provide an integer as argument!")
    return int(arg)


def main():
    dataCreation_args = parse_dataCreation_arguments()
    DataGenerator.generate_and_write_data_to_file(
        dataCreation_args.n, 
        dataCreation_args.d, 
        dataCreation_args.m, 
        dataCreation_args.l, 
        dataCreation_args.k
        )


if __name__ == "__main__":
    main()
