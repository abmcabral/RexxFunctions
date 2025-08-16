import re
import os
from pathlib import Path

class RexxFunctions:
    """
    A complete Python implementation of Regina Rexx string and file operations.
    Includes 1-based indexing and exact Rexx behavior where applicable.
    """

    FILE_NOT_FOUND = 0xEEEEEEEE
    END_OF_FILE = 0xFFFFFFFF

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
            print (f'File does not exist: {file_path}')
            return self.FILE_NOT_FOUND
        except IOError:
            return self.END_OF_FILE

    @staticmethod
    def translate(string, output_chars=None, input_chars=None, pad=None):
        """
        Rexx TRANSLATE():
        - With 1 arg: Converts to uppercase
        - With 2 args: Removes output_chars
        - With 3+ args: Character mapping with padding
        """
        if output_chars is None and input_chars is None:
            return string.upper()
        
        if input_chars is None:
            return string.translate(str.maketrans('', '', output_chars))
        
        if pad and len(input_chars) < len(output_chars):
            input_chars += pad * (len(output_chars) - len(input_chars))
            
        return string.translate(str.maketrans(input_chars, output_chars))

    @staticmethod
    def substr(string, start, length=None):
        """Rexx SUBSTR() with 1-based indexing"""
        if start < 1:
            raise ValueError("Start position must be ≥ 1")
        if length:
            return string[start-1 : start-1 + length]
        return string[start-1:]

    @staticmethod
    def word(string, n, delimiter=' '):
        """Rexx WORD(): Get nth word (1-based)"""
        words = string.split(delimiter)
        return words[n-1] if 0 < n <= len(words) else ""

    @staticmethod
    def words(string, delimiter=' '):
        """
        Rexx WORDS(): Counts the number of words in a string.
        - delimiter: Character to split words (default: space)
        - Returns 0 for empty strings (like REXX)
        """
        if not string.strip():
            return 0
        return len(string.split(delimiter))

    @staticmethod
    def pos(needle, haystack, start=1):
        """Rexx POS(): Find substring position (1-based)"""
        idx = haystack.find(needle, start-1)
        return idx + 1 if idx != -1 else 0

    @staticmethod
    def changestr(old, new, string):
        """Rexx CHANGESTR(): Global replace"""
        return string.replace(old, new)

    @staticmethod
    def strip(string, mode='B', char=' '):
        """
        Rexx STRIP():
        - mode='L'/'T'/'B' (default='B')
        - char=' ' (default)
        """
        if mode == 'L':
            return string.lstrip(char)
        elif mode == 'T':
            return string.rstrip(char)
        elif mode == 'B':
            return string.strip(char)
        else:
            raise ValueError("Invalid mode. Use 'L','T', or 'B'")

    @staticmethod
    def datatype(string, test_type='N'):
        """
        Rexx DATATYPE():
        - 'N' = Number (default)
        - 'A' = Alphanumeric
        - 'U' = Uppercase
        - 'L' = Lowercase
        - 'W' = Whole number
        """
        if not string:
            return 0
        
        if test_type == 'N':
            try:
                float(string)
                return 1
            except ValueError:
                return 0
        elif test_type == 'A':
            return int(string.isalnum())
        elif test_type == 'U':
            return int(string.isupper())
        elif test_type == 'L':
            return int(string.islower())
        elif test_type == 'W':
            return int(string.lstrip('-+').isdigit())
        else:
            raise ValueError(f"Invalid test_type: {test_type}")

    @staticmethod
    def verify(string, ref_chars, mode='N'):
        """
        Rexx VERIFY():
        - mode='N' = First invalid char (default)
        - mode='M' = First valid char
        """
        for i, char in enumerate(string, 1):
            if (mode == 'N' and char not in ref_chars) or (mode == 'M' and char in ref_chars):
                return i
        return 0

    @staticmethod
    def delstr(string, start, length=None):
        """Rexx DELSTR(): Delete substring (1-based)"""
        if start < 1:
            raise ValueError("Start position must be ≥ 1")
        return string[:start-1] + (string[start-1 + length:] if length else "")

    @staticmethod
    def compare(string1, string2, pad=' '):
        """Rexx COMPARE(): Compare strings with padding"""
        max_len = max(len(string1), len(string2))
        s1 = string1.ljust(max_len, pad)
        s2 = string2.ljust(max_len, pad)
        for i, (c1, c2) in enumerate(zip(s1, s2), 1):
            if c1 != c2:
                return i
        return 0

    @staticmethod
    def left(string, length, pad=' '):
        """Rexx LEFT(): Pad/truncate left"""
        return string[:length] if len(string) >= length else string.ljust(length, pad)

    @staticmethod
    def right(string, length, pad=' '):
        """Rexx RIGHT(): Pad/truncate right"""
        return string[-length:] if len(string) >= length else string.rjust(length, pad)

    @staticmethod
    def copies(string, n):
        """Rexx COPIES(): Repeat string"""
        return string * n

    @staticmethod
    def rm(file_path):
        passfile = Path(file_path)    
        if passfile.exists():
           passfile.unlink()  # Equivalent to os.remove()
        else:
           print(f"File does not exist: {passfile}")

    @staticmethod
    def lineout(file_path, string, append=False):
        """
        Rexx LINEOUT():
        - append=False: Overwrite (default)
        - append=True: Append
        - Returns 0 (success) or 1 (failure)
        """
        try:
            mode = 'a' if append else 'w'
            with open(file_path, mode) as file:
                file.write(string + '\n')
            return 0
        except IOError:
            return 1

    @staticmethod
    def delword(s, word_num, count=1, delimiter=" "):
        """
        Delete words from a string (like Rexx's DELWORD).
        
        Args:
            s (str): Input string.
            word_num (int): Position of the first word to delete (1-based).
            count (int): Number of words to delete (default=1).
            delimiter (str): Word separator (default=" ").
        
        Returns:
            str: String with specified words removed.
        
        Examples:
            >>> RexxFunctions.delword("one two three four", 2)
            "one three four"
            >>> RexxFunctions.delword("a,b,c,d", 3, 2, ",")
            "a,b"
        """
        words = s.split(delimiter)
        if word_num <= 0 or word_num > len(words):
            return s  # No change if position is invalid
        # Slice out the unwanted words
        remaining_words = words[:word_num - 1] + words[word_num - 1 + count:]
        return delimiter.join(remaining_words)

    @staticmethod
    def insert(new_str, original_str, position):
        """
        Inserts 'new_str' into 'original_str' at 1-based 'position'.
        Mimics REXX's INSERT function.

        Args:
            new_str (str): String to insert.
            original_str (str): Target string.
            position (int): 1-based insertion point.

        Returns:
            str: Combined string.

        Example:
            >>> RexxFunctions.insert("_0000", "file.txt", 5)
            'file_0000.txt'
        """
        if position < 1:
            position = 1  # REXX treats positions <1 as 1
        # Convert to 0-based for Python slicing
        return original_str[:position-1] + new_str + original_str[position-1:]
