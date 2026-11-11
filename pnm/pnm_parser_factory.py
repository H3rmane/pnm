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


from typing import Dict, List, Type
from pnm_parser import (
        PNMParser, 
        PNMFormat105, 
        PNMFormat112, 
        PNMFormat138, 
        PNMFormat141, 
        PNMFormat164, 
        PNMFormat199
    )


class PNMParserFactory:
    """
    Factory class responsible for selecting the appropriate PNM parser 
    based on the length of the data lines in the file.
    """

    _parsers: Dict[int, Type[PNMParser]] = {
        105: PNMFormat105,
        112: PNMFormat112,
        138: PNMFormat138,
        141: PNMFormat141,
        164: PNMFormat164,
        199: PNMFormat199,
    }

    @classmethod
    def register_parser(cls, line_length: int, parser_class: Type[PNMParser]) -> None:
        """
        Registers a new parser dynamically. This allows extending the system 
        without modifying existing code.

        :param line_length: The expected length of the data line for this parser.
        :param parser_class: The parser class that should be used for this line length.
        """
        cls._parsers[line_length] = parser_class

    @classmethod
    def get_parser(cls, lines: List[str]) -> PNMParser:
        """
        Determines and returns the appropriate parser based on the length 
        of the second line in the file (assuming the first line contains 
        metadata such as the company name).

        :param lines: A list of strings representing the lines of the PNM file.
        :return: An instance of the appropriate PNMParser subclass.
        :raises ValueError: If the file is too short or if no matching parser is found.
        """
        if len(lines) < 2:
            raise ValueError("Incomplete file: not enough lines to determine the format.")

        # Remove either Unix (\n) or Windows (\r\n) line endings without
        # trimming spaces that may be part of the fixed-width record.
        sample_line = lines[1].rstrip("\r\n")
        line_length = len(sample_line)

        parser_class = cls._parsers.get(line_length)
        if parser_class is None:
            raise ValueError(
                f"Unknown format with a line length of {line_length} characters."
            )

        return parser_class()
