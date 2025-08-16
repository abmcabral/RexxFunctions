    def __init__(self):
        # Dictionary to track file positions: {filename: current_line}
        self._file_positions = {}

    def linein(self, file_path, line_number=None):
        """
        Stateful LINEIN() that remembers position between calls
        - If line_number provided: read specific line (1-based)
        - If no line_number: read next line from last position
        - Returns line content or END_OF_FILE/FILE_NOT_FOUND
        """
        try:
            path = str(file_path)
            
            # Initialize position tracking if first access
            if path not in self._file_positions:
                self._file_positions[path] = 0
            
            # Determine which line to read
            if line_number is None:
                # Read next line (increment position)
                self._file_positions[path] += 1
                read_line = self._file_positions[path]
            else:
                # Read specific line (don't change position)
                if line_number < 1:
                    raise ValueError("Line numbers must be ≥ 1")
                read_line = line_number
            
            # Read the requested line
            with open(file_path, 'r') as file:
                for i, line in enumerate(file, 1):
                    if i == read_line:
                        return line.rstrip('\n')
                
                # Line not found (past EOF)
                if line_number is None:
                    # For sequential reads, reset position at EOF
                    self._file_positions[path] = 0
                return self.END_OF_FILE
                
        except FileNotFoundError:
            print (f'file {file_path} not found...')
            return self.FILE_NOT_FOUND
        except IOError:
            return self.END_OF_FILE

