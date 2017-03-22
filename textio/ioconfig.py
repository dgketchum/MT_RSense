import os

from text_data import text_data


class IoConfig(text_data):
    """
    An ioconfig object is an extension to the text_data_class
    it has the same methods of text_data_class, plus an add_param function
    and simplified save,load functions.

    It is used to generate "config" files, lists of important inputs to a set
    of complex functions. Allows you to save inputs and call them over and over
    again to avoid tedious input definitions, also facilitates good record keeping
    by keeping a hard file with a summary of all inputs alongside any outputs that
    might have been generated.

    when a param has been added or imported, its value may be accessed with:
        ioconfig_object['param_name']
            
    """

    # overrides
    def __init__(self, input_filepath = None):

        self.headers    = ["param_name".ljust(30), "param_type".ljust(18), "param_value"]
        self.row_data   = []        # standard text data object row_data formating
        self.conf_dict  = {}        # config dict of {param_name: param_value}

        if input_filepath and os.path.exists(input_filepath):
            self.read(input_filepath)
        return


    def __getitem__(self, index):

        if isinstance(index, str):
            return self.conf_dict[index]
        elif isinstance(index, int):
            return self.row_data[index][2]

    
    def add_param(self, param_dict):
        """
        adds parameters to the ioconfig object
        
        input a dictionary of param names (keys) and values.

        when a param has been added or imported, its value may be accessed with:
            ioconfig_object['param_name']
        """

        # avoid indexing errors by handling list inputs differently
        param_names  = param_dict.keys()
        param_values = param_dict.values()

        if isinstance(param_names, list):
            for i, param in enumerate(param_names):
                entry = [param_names[i].ljust(30), str(type(param_values[i])).ljust(18), param_values[i]]
                self.row_data.append(entry)
                self.conf_dict[entry[0].strip()] = entry[2]
        else:
            entry = [param_names.ljust(30), str(type(param_values)).ljust(18), param_values]
            self.row_data.append(entry)
            self.conf_dict[entry[0].strip()] = entry[2]
            
        return


    def write(self, filepath):
        """ saves the contents of ioconfig object as text_data_object"""

        self.write_csv(filepath, delim = " ; ")
        return
        

    def read(self, filepath):
        """
        loads the contents of ioconfig object as a text data object

        interprets and formats each of the variables
        """

        self.read_csv(text_filepath = filepath, delim = " ; ")

        for i, row in enumerate(self.row_data):
            self.row_data[i][2] = self.interp(row[1], row[2])
            self.conf_dict[row[0].strip()] = row[2]

        print("Imported config file '{0}'".format(filepath))
        print("Keys                           : Values")
        print("---------------------------------------")
        for key, value in sorted(self.conf_dict.iteritems()):
            print("{0} : {1}".format(key.ljust(30), value))
        
        return


    def summary(self):
        """ prints a summary of the ioconfig object """
        pass


    def interp(self, in_type, in_value):
        """ wraps other interp functions into one """

        in_type = in_type.strip()
        
        if  "str" in in_type or "unicode" in in_type:
            return str(in_value)
        
        elif "bool" in in_type:
            if in_value == "True":
                return True
            else:
                return False

        elif "float" in in_type:
            return float(in_value)

        elif "int" in in_type:
            return int(in_value)
        
        elif "long" in in_type:
            return long(in_value)

        elif "complex" in in_type:
            return complex(in_value)

        elif "None" in in_type:
            return None

        elif "list" in in_type or "dict" in in_type or "tuple" in in_type:
            raise TypeError("values of {0} are not supported. To save these ".format(in_type) + \
                            "values, please separate each entry and add the parameters individually")
        else:
            raise TypeError("could not interpret input'{0}'".format(in_type))
        return
    


# testing area
if __name__ == "__main__":


    test_dict = {"str" : "test string",
                  "bool" : True,
                  "float" : 1.12345,
                  "int" : 1,
                  "long" : 100000000000000000000000,
                  "complex": 1 + 1j}


    conf = ioconfig()
    conf.add_param(test_dict)
    conf.add_param({"outfilepath" : "some filepath on my hard drive"})
    conf.write("conf_test.txt")
    del conf
    
    conf = ioconfig("conf_test.txt")
    print conf["str"]
