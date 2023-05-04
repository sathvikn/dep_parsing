import argparse
import os
import re

from spacy_conll import init_parser
from tqdm import tqdm

def initialize_parser(use_gpu):
    """
    if you're running this in parallel and are getting out of memory erros, add
    "depparse_batch_size":400 to the parser_opts dictionary.
    stanza is the SpaCy implementation of the Stanford NLP library
    """
    return init_parser("en", "stanza", parser_opts = {"use_gpu": use_gpu}, include_headers=True)

def parse_documents(parser, input_dir, output_dir):
    # goes through the documents in the corpus and writes them into an output file line-by-line
    files = os.listdir(input_dir)
    for filename in files:
        path = os.path.join(input_dir, filename)
        output_filename = filename.split(".txt")[0] + ".conll"

        with open(path, "r") as f:
            file_lines = f.readlines()
            print("read " + path)
        print("lines in file read: \n")
        for line in tqdm(file_lines):
            # if the line is not empty
            if len(line.strip()):
                # the first character should be the ID of the line. multiple sentences are in the same line.
                line_tokens = line.split()
                line_id = line_tokens[0]
                doc = " ".join(line_tokens[1:])
                dependency_parse = parse_line(doc, parser)
                write_output_file(line_id, dependency_parse, output_dir, output_filename)
        close_file(output_dir, output_filename)

def write_output_file(line_id, parse, output_dir, output_filename):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "a") as f:
        f.write("# line ID: " + line_id + "\n")
        f.write(parse)
        f.write("\n")

def close_file(output_dir, output_filename):
    f = open(os.path.join(output_dir, output_filename))
    f.close()

def clean_html(html):
    """	
    from https://github.com/jkallini/PrincetonThesis/blob/master/COCAcleaner.py
    Adapted from NLTK package.	
    Removes HTML markup from the given string.
    Removes COCA article titles and parenthetical asides.
        input: the HTML string to be cleaned (string)
        output: string
    """

    # Remove inline JavaScript/CSS:	
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())	
    # Then we remove html comments. This has to be done before removing regular	
    # tags since comments can contain '>' characters.	
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)	
    # Next we can remove the remaining tags:	
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

    # Remove article headers
    cleaned = re.sub(r'##[0-9]+ ', "", cleaned)		

    # Remove content of parentheticals
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)

    # Remove html image data
    cleaned = re.sub(r'alt=.* src=.*.', "", cleaned)

    # Remove speaker titles in spoken text
    cleaned = re.sub(r'@![^\s]*', "", cleaned)

    # Remove special characters and titles:	
    cleaned = re.sub(r"[!@##$$%^&*():\"]", "", cleaned)	
    cleaned = re.sub(r"%&%.*%&%", "", cleaned)
    cleaned = re.sub(r"//", "", cleaned)

    # Normalize 2 > whitespace to 1 whitespace
    cleaned = re.sub("\s{2,}", " ",cleaned)
    return cleaned.strip()

def parse_line(text, parser):
    text = clean_html(text)
    doc = parser(text)
    return doc._.conll_str

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input_dir', help='path to input files')
    arg_parser.add_argument('--output_dir', help='where the output should be written')
    arg_parser.add_argument('--use_gpu', action = "store_true")
    args = arg_parser.parse_args()
    print("======loading parser: with GPU=" + str(args.use_gpu) + " =======")
    parser = initialize_parser(args.use_gpu)
    print("=====parsing documents======")
    dependency_parses = parse_documents(parser, args.input_dir, args.output_dir)
