# random-key-value-pair-generator
This code generates a specified number of random JSON objects with nested key-value pairs, and writes them to a file. The keys and data types of the key-value pairs are specified in a separate file.

##Description
This code generates a specified number of random JSON objects with nested key-value pairs, and writes them to a file. The keys and data types of the key-value pairs are specified in a separate file.


##Requirements

- Python 3.7 or higher
- argparse library (comes with Python
- os library (comes with Python)
- random library (comes with Python)
- string library (comes with Python)
- json library (comes with Python)
- typing library (comes with Python)

##Usage
The data generation program is used to generate random data in the form of key-value pairs that can be stored in a key-value store.

To use this code, open a terminal or command prompt in the same directory as the code file and run the following command:
```python
python3 random_key-value_generator.py -n <number of lines> -m <maximum keys> -l <maximum string length> -d <maximum level of nesting> -f <key file>
```

#Parameters

- "-k": a file containing a space-separated list of key names and their data types that can be used to generate tha data
- "-n": the number of data items to generate
- "-d": the maximum depth of nesting for the key-value pairs
- "-l": the maximum length of string values
- "-m": the maximum number of keys per nesting level

#Example

```python
python3 dataGenerator.py -n 5 -m 3 -l 10 -d 2 -f keyFile.txt
```
This command will generate 5 JSON objects with a maximum of 3 keys each, string values with a maximum length of 10, and a maximum level of nesting of 2. The keys and data types for the key-value pairs are specified in the "keyFile.txt" file.

#Key File Format

The file containing the space-separated list of key names and their data types should contain one key and its data type per line, separated by a single space. The data type can be "string", "int", or "float".

Here is an example "keyFile.txt" file:

```python
key1 string
key2 int
key3 float
```

#Output Data Format

The generated JSON objects will be written to a file called "dataToIndex.txt" in the same directory as the code file. Each JSON object will be on its own line. 

Notes

- If a key-value pair is nested, the value will be a JSON object with its own set of key-value pairs.
- Keys at the root level must be unique. If a key appears more than once at the root level, it will be suffixed with an increasing integer starting from 0.
