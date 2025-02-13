# Copyright (c) 2025 Nzeunang Hermane <nzeunang@gmail.com>
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
# For any inquiries, please contact: [nzeunang@gmail.com]


from typing import Dict, List
from pnm_parser_factory import PNMParserFactory


class PNMReader:
    """
    Responsible for reading PNM files from disk and extracting structured data 
    using the appropriate parser.
    """

    def __init__(self, filepath: str) -> None:
        """
        Initializes the PNMReader with the file path.

        :param filepath: The full path to the PNM file to be read.
        """
        self._filepath = filepath

    def read(self) -> List[Dict[str, str]]:
        """
        Reads the PNM file, detects the correct parser, and extracts structured data.

        :return: A list of dictionaries, where each dictionary represents a parsed entry.
        :raises ValueError: If the file format cannot be determined.
        """
        with open(self._filepath, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        # Use the factory to detect and instantiate the appropriate parser
        parser = PNMParserFactory.get_parser(lines)

        return parser.parse(lines)

