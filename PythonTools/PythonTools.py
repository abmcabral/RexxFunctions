class Read_infile:
    def __init__(self, filename):
        self.filename = filename

    def get_inrec(self):
        try:
            with open(self.filename, 'r') as infile:
                for inrec in infile:
                    yield inrec.rstrip('\n')
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found")
            yield from ()  # Return an empty generator to avoid StopIteration issues
