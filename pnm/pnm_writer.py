# Copyright (c) 2025 Nzeunang Hermane <hnzeunang@gmail.com>
# 
# This software is protected by copyright law. All rights reserved.
# 
# Permission is granted, free of charge, to any person obtaining a copy
# of this software and associated files (the "Software"), to use the Software
# without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# subject to the following conditions:
# 
# 1. This copyright notice and permission notice shall be included in all
#    copies or substantial portions of the Software.
# 
# 2. The Software is provided "as is", without warranty of any kind, express or implied,
#    including but not limited to warranties of merchantability, fitness for a particular
#    purpose, and non-infringement. In no event shall the authors or copyright holders
#    be liable for any claim, damages, or other liability, whether in an action of contract,
#    tort, or otherwise, arising from, out of, or in connection with the Software or the
#    use or other dealings in the Software.
# 
# For any inquiries, please contact: [hnzeunang@gmail.com]



import io
from typing import Dict, List, Tuple, TextIO


class PNMFormatter:
    """
    A class responsible for formatting PNM entries based on predefined field positions.

    It ensures that each entry follows the specified format by aligning fields correctly 
    and truncating values if necessary.
    """

    def __init__(self, fields: List[Tuple[str, int, int]]) -> None:
        """
        Initializes the formatter with the given field definitions.

        :param fields: A list of tuples, where each tuple contains:
            - Field name (str)
            - Start position (int)
            - End position (int)
        """
        # Sort fields based on their start position to maintain correct order
        self.fields = sorted(fields, key=lambda x: x[1])
        self.entry_format = self._build_entry_format()

    def _build_entry_format(self) -> str:
        """
        Constructs a format string based on the width of each field.

        :return: A format string that ensures proper spacing between fields.
        """
        return "".join("{%s:%d}" % (field[0], field[2] - field[1]) for field in self.fields)

    def prepare_entry(self, entry: Dict[str, str]) -> Dict[str, str]:
        """
        Prepares an entry by ensuring that each field's value does not exceed its defined width.

        :param entry: A dictionary representing a single record.
        :return: A dictionary with truncated or padded field values.
        """
        return {
            field[0]: entry.get(field[0], "")[: (field[2] - field[1])]
            for field in self.fields
        }

    def format_entry(self, entry: Dict[str, str]) -> str:
        """
        Formats a given entry into a string based on the predefined field structure.

        :param entry: A dictionary containing field values.
        :return: A formatted string representation of the entry.
        """
        prepared = self.prepare_entry(entry)
        return self.entry_format.format(**prepared)


class PNMWriter:
    """
    A class responsible for writing formatted PNM entries to a specified output stream.

    It ensures that data is properly formatted before being written, and allows for flexible 
    output destinations, such as files or in-memory buffers.
    """

    def __init__(self, formatter: PNMFormatter, stream: TextIO = None) -> None:
        """
        Initializes the writer with a formatter and an optional output stream.

        :param formatter: An instance of PNMFormatter used to format entries before writing.
        :param stream: An optional text stream (e.g., a file or StringIO). If not provided, 
                       a default in-memory buffer is used.
        """
        self.formatter = formatter
        # Allows injecting any stream (StringIO, file, etc.)
        self.stream = stream if stream is not None else io.StringIO()

    def write(self, entries: List[Dict[str, str]]) -> None:
        """
        Writes a list of formatted entries to the output stream.

        :param entries: A list of dictionaries, each representing a PNM record.
        """
        if self.stream.writable():
            for entry in entries:
                line = self.formatter.format_entry(entry) + "\n"
                self.stream.write(line)

    def get_data(self) -> str:
        """
        Retrieves the full content written to the output stream.

        :return: A string containing all formatted entries.
        """
        return self.stream.getvalue()
