## Description
This runs a SpaCy implementation of the Stanford NLP dependency parser and writes the output to `.conll` files in the Universal Dependencies format. It was originally made to parse the Corpus of Contemporary American English (COCA).

## Running the code
Create and activate a virtual environment:

```
ENV_NAME=
python3 -m venv $ENV_NAME
source $ENV_NAME/bin/activate
```

Run `pip install -r requirements.txt` to download the dependencies. To run the parser, you need to specify input and output directories, and whether you want to use a GPU (default false, add the `--use_gpu flag` to make it true.

```
INPUT=
OUTPUT=
python run_parser.py --input_dir $INPUT --output_dir $OUTPUT
```

The output files can be read by a parser like [`conllu`](https://pypi.org/project/conllu/) or [`pyconll`](https://github.com/pyconll/pyconll).
