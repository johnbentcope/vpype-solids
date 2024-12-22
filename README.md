# vpype-solids

[`vpype`](https://github.com/abey79/vpype) plug-in to generate renders of three dimensional scenes


## Examples

_to be completed_


## Installation

See the [installation instructions](https://vpype.readthedocs.io/en/latest/install.html) for information on how
to install `vpype`.

If *vpype* was installed using pipx, use the following command:

```bash
$ pipx inject vpype vpype-solids
```

If *vpype* was installed using pip in a virtual environment, activate the virtual environment and use the following command:

```bash
$ pip install vpype-solids
```

Check that your install is successful:

```
$ vpype vpype_solids --help
[...]
```

## Documentation

The complete plug-in documentation is available directly in the CLI help:

```bash
$ vpype vpype_solids --help
```


## Development setup

Here is how to clone the project for development:

```bash
$ git clone https://github.com/johnbentcope/vpype-solids.git
$ cd vpype-solids
```

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install `vpype-solids` and its dependencies (including `vpype`):

```bash
$ pip install -e .
$ pip install -r dev-dependencies.txt
```


## License

See the [LICENSE](LICENSE) file for details.
