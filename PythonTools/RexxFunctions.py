import sys
from pathlib import Path

class RexxFunctions:
    """Complete REXX functions implementation with EOF control in linein()"""

    # Constants
    FILE_NOT_FOUND = 0xEEEEEEEE
    END_OF_FILE = 0xFFFFFFFF

    def __init__(self, exit_on_error=True, verbose=True):
        """
        Initialize with:
        - exit_on_error: Terminate program on errors (default: True)
        - verbose: Show detailed messages (default: True)
        """
        self._file_positions = {}
        self.exit_on_error = exit_on_error
        self.verbose = verbose
        self.next_record = 0

    def linein(self, file_path, line_number=None, exit_on_eof=True):
        """
        Read a file line with EOF control:
        - exit_on_eof=True: Exit program on EOF (default)
        - exit_on_eof=False: Return END_OF_FILE constant
        """
        try:
            path = Path(file_path).absolute()
            
            if not path.exists():
                msg = f"File does not exist: {path}"
                if self.verbose:
                    print(msg, file=sys.stderr)
                if self.exit_on_error:
                    sys.exit(1)
                return self.FILE_NOT_FOUND

            if not path.is_file():
                msg = f"Path is not a file: {path}"
                if self.verbose:
                    print(msg, file=sys.stderr)
                if self.exit_on_error:
                    sys.exit(1)
                return self.FILE_NOT_FOUND

            file_key = str(path)
            if file_key not in self._file_positions:
                self._file_positions[file_key] = 0

            target_line = (self._file_positions[file_key] + 1) if line_number is None else line_number

            with open(path, 'r') as file:
                for current_line, content in enumerate(file, 1):
                    if current_line == target_line:
                        self._file_positions[file_key] = current_line
                        self.next_record = current_line
                        return content.rstrip('\n')

                # EOF handling
                if line_number is None:
                    self._file_positions[file_key] = 0
                if exit_on_eof and self.exit_on_error:
                    sys.exit(0)
                return self.END_OF_FILE

        except PermissionError:
            msg = f"Permission denied: {path}"
            if self.verbose:
                print(msg, file=sys.stderr)
            if self.exit_on_error:
                sys.exit(1)
            return self.FILE_NOT_FOUND

        except Exception as e:
            msg = f"Error reading file {path}: {str(e)}"
            if self.verbose:
                print(msg, file=sys.stderr)
            if self.exit_on_error:
                sys.exit(1)
            return self.END_OF_FILE

    def rm(self, file_path):
        """Delete file with guaranteed feedback"""
        path = Path(file_path).absolute()
        
        if not path.exists():
            msg = f"File does not exist (not deleted): {path}"
            if self.verbose:
                print(msg, file=sys.stderr)
            return self.FILE_NOT_FOUND

        try:
            path.unlink()
            if self.verbose:
                print(f"File successfully deleted: {path}")
            return 0
        except Exception as e:
            msg = f"Error deleting file {path}: {str(e)}"
            if self.verbose:
                print(msg, file=sys.stderr)
            if self.exit_on_error:
                sys.exit(1)
            return 1

    def lineout(self, file_path, string, append=False):
        """Write to file with error handling"""
        try:
            with open(file_path, 'a' if append else 'w') as file:
                file.write(string + '\n')
            return 0
        except Exception as e:
            msg = f"Error writing to file {file_path}: {str(e)}"
            if self.verbose:
                print(msg, file=sys.stderr)
            if self.exit_on_error:
                sys.exit(1)
            return 1

    # =========================================
    # STRING FUNCTIONS (Original implementation)
    # =========================================

    @staticmethod
    def translate(string, output_chars=None, input_chars=None, pad=None):
        if output_chars is None and input_chars is None:
            return string.upper()
        if input_chars is None:
            return string.translate(str.maketrans('', '', output_chars))
        if pad and len(input_chars) < len(output_chars):
            input_chars += pad * (len(output_chars) - len(input_chars))
        return string.translate(str.maketrans(input_chars, output_chars))

    @staticmethod
    def substr(string, start, length=None):
        if start < 1:
            raise ValueError("Start position must be ≥ 1")
        if length:
            return string[start-1 : start-1 + length]
        return string[start-1:]

    @staticmethod
    def word(string, n, delimiter=' '):
        words = string.split(delimiter)
        return words[n-1] if 0 < n <= len(words) else ""

    @staticmethod
    def words(string, delimiter=' '):
        if not string.strip():
            return 0
        return len(string.split(delimiter))

    @staticmethod
    def pos(needle, haystack, start=1):
        idx = haystack.find(needle, start-1)
        return idx + 1 if idx != -1 else 0

    @staticmethod
    def changestr(old, new, string):
        return string.replace(old, new)

    @staticmethod
    def strip(string, mode='B', char=' '):
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
        for i, char in enumerate(string, 1):
            if (mode == 'N' and char not in ref_chars) or (mode == 'M' and char in ref_chars):
                return i
        return 0

    @staticmethod
    def delstr(string, start, length=None):
        if start < 1:
            raise ValueError("Start position must be ≥ 1")
        return string[:start-1] + (string[start-1 + length:] if length else "")

    @staticmethod
    def compare(string1, string2, pad=' '):
        max_len = max(len(string1), len(string2))
        s1 = string1.ljust(max_len, pad)
        s2 = string2.ljust(max_len, pad)
        for i, (c1, c2) in enumerate(zip(s1, s2), 1):
            if c1 != c2:
                return i
        return 0

    @staticmethod
    def left(string, length, pad=' '):
        return string[:length] if len(string) >= length else string.ljust(length, pad)

    @staticmethod
    def right(string, length, pad=' '):
        return string[-length:] if len(string) >= length else string.rjust(length, pad)

    @staticmethod
    def copies(string, n):
        return string * n

    @staticmethod
    def delword(s, word_num, count=1, delimiter=" "):
        words = s.split(delimiter)
        if word_num <= 0 or word_num > len(words):
            return s
        remaining_words = words[:word_num - 1] + words[word_num - 1 + count:]
        return delimiter.join(remaining_words)

    @staticmethod
    def insert(new_str, original_str, position):
        if position < 1:
            position = 1
        return original_str[:position-1] + new_str + original_str[position-1:]
