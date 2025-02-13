import io
import argparse
from pprint import pprint
from pnm_reader import PNMReader
from pnm_parser import PNMFormat141 
from pnm_writer import PNMWriter, PNMFormatter

def parse_arguments():
    parser = argparse.ArgumentParser(description="PNM Test.")
    parser.add_argument("--file", "-f", help="PNM file path.", required=True)
    return parser.parse_args() 

def test():
    args = parse_arguments()
    filepath = args.file
    try:
        reader = PNMReader(filepath)    
        entries = reader.read()
        pprint(entries)

        formatter = PNMFormatter(PNMFormat141.fields)

        with open("output1.pnm", "w", encoding="utf-8")  as fp:
            writer = PNMWriter(formatter, fp)
            writer.write(entries)
        
        writer = PNMWriter(formatter, io.StringIO())
        writer.write(entries)
        with open("output2.pnm", "w", encoding="utf-8") as fp:
            fp.write(writer.get_data())


    except Exception as e:
        print(e)


if __name__ == "__main__":
    test()
