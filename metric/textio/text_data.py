__author__ = ["jwely"]

import os


class text_data():
    """
    a text data object is a very simple template structure for passing
    text type data (usually lists of obsgrid or climate data entries)
    between other functions in dnppy
    """

    def __init__(self, headers=None, row_data=None, text_filepath=None):

        self.headers = headers  # headers   (1d list)
        self.row_data = row_data  # data      (2d list)
        self.text_filepath = text_filepath  # filepath  (string)
        self.col_data = {}  # columnwise data (dict)

        # if only a text filepath is defined, try reading from it.
        if text_filepath is not None and headers is None and row_data is None:
            try:
                self.read_csv(text_filepath)
            except:
                pass

        if row_data is not None:
            self.build_col_data()
        return

    def __getitem__(self, index):
        """ used to return row data when using __getitem__ on this object type """

        return self.row_data[index]

    def build_col_data(self):
        """ builds column wise data matrix with an actual dict """

        temp_col = zip(*self.row_data)

        self.col_data = {}
        for i, col in enumerate(temp_col):
            self.col_data[self.headers[i]] = list(col)
        return

    def write_csv(self, text_filepath=None, delim=','):
        """ writes the contents of this text file object as a CSV """

        root = os.path.dirname(text_filepath)
        if not os.path.isdir(root) and root != "":
            os.makedirs(root)

        if text_filepath:
            self.text_filepath = text_filepath

        elif self.text_filepath:
            pass

        else:
            raise Exception("cannot write csv with no filepath defined!")

        # write the file as a csv
        with open(self.text_filepath, 'w+') as f:
            if self.headers:
                f.write(delim.join(self.headers) + '\n')

            for row in self.row_data:
                row = map(str, row)
                entry = delim.join(row) + '\n'
                f.write(entry)
            f.close()

        return

    def read_csv(self, text_filepath=None, delim=',', has_headers=True):
        """ simple default reader of a delimited file. Does not read fixed-width """

        if text_filepath is not None:
            self.text_filepath = text_filepath

        print("")
        with open(self.text_filepath, 'r') as f:

            self.row_data = []

            if has_headers:
                self.headers = next(f).replace('\n', '').split(delim)
                self.headers = [x for x in self.headers if x != ""]
            else:
                self.headers = None

            for line in f:
                entry = line.replace('\n', '').split(delim)
                self.row_data.append(entry)
        f.close()
        return
