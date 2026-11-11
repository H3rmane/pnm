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



from abc import abstractmethod
from typing import List, Dict, Tuple, Protocol


class IPNMParser(Protocol):
    """Interface for parsing PNM files."""

    @abstractmethod
    def parse(self, lines: List[str]) -> List[Dict[str, str]]:
        pass


class PNMParser(IPNMParser):
    """
    Base class for parsing.
    Subclasses must define the `fields` class variable as a list of tuples (field_name, start, end).
    """
    fields: List[Tuple[str, int, int]] = []

    def parse(self, lines: List[str]) -> List[Dict[str, str]]:
        entries = []
        for line in lines[1:]:  # assuming the first line is a company name
            entry = {field: line[start:end].strip() for field, start, end in self.fields}
            entries.append(entry)
        return entries


class PNMFormat105(PNMParser):
    fields = [
        ("journal_code", 0, 3),
        ("date_piece", 3, 9),
        ("type_piece", 9, 11),
        ("compte_general", 11, 24),
        ("type_compte", 24, 25),
        ("compte_analytique", 25, 38),
        ("reference_ecriture", 38, 51),
        ("libelle_ecriture", 51, 76),
        ("mode_paiement", 76, 77),
        ("date_echeance", 77, 83),
        ("sens", 83, 84),
        ("montant_monnaie_tcompte", 84, 104),
        ("type_ecriture", 104, 105),
    ]


class PNMFormat112(PNMFormat105):
    fields = PNMFormat105.fields + [("numero_piece", 105, 112)]


class PNMFormat138(PNMFormat112):
    fields = PNMFormat112.fields + [("zone_reserve", 112, 138)]


class PNMFormat141(PNMFormat138):
    fields = PNMFormat138.fields + [("code_iso_devise", 138, 141)]


class PNMFormat164(PNMFormat141):
    fields = PNMFormat141.fields + [
        ("montant_devise", 141, 161),
        ("code_iso_devise_ecriture", 161, 164),
    ]


class PNMFormat199(PNMFormat164):
    fields = PNMFormat164.fields + [
        ("axe_analytique", 164, 174),
        ("section_analytique", 174, 199),
    ]
