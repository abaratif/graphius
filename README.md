# Graphius

Collapse redundant subtrees in a graph.

## Environment Setup
Initialize the virtualenv and install packages
```
    virtualenv VENV
    source VENV/bin/activate
    pip install -r requirements_dev.txt
```

## Usage

### Input
Graphius takes JSON formatted input representing graph nodes, similar to the example below.
```
[{
		"id": 1,
		"value": "A",
		"children": [2, 3]
	},
	{
		"id": 2,
		"value": "B",
		"children": []
	},
	{
		"id": 3,
		"value": "C",
		"children": [4]
	},
	{
		"id": 4,
		"value": "B",
		"children": []
	}
]
```
### Running and Output

Use the `run` target of the makefile, with a `file=FILENAME` argument to specify input.
Graphius will collapse redundant subtrees and print JSON formatted output to stdout.

```
make run file=examples/example3.json
python cli.py examples/example3.json
[{"id": 1, "neighbors": [3, 4], "value": "A"}, {"id": 3, "neighbors": [4], "value": "C"}, {"id": 4, "neighbors": [], "value": "B"}]
```
To save output to a file, simply pipe the results to a file.
```
make run file=examples/example3.json > output.json
```

## Development

### Testing
run `make test` to execute unit tests.

