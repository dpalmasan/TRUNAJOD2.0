# Contributing to TRUNAJOD

:+1::tada: Thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to `TRUNAJOD`. These are mostly guidelines, however there are some special steps you need to be aware of when creating a pull request so we end up with a standardized code. Please feel free to propose changes to this document in a PR.

#### Table Of Contents

This section is TBD.

## How Can I Contribute?

### Reporting Bugs

This section is TBD.

### Suggesting Enhancements

This section is TBD.

### Your First Code Contribution

Unsure where to begin contributing to Atom? You can start by looking through these `beginner` and `help-wanted` issues:

* [Good first issue][good-first-issue] - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] - issues which should be a bit more involved than `good first issue` issues.

### Pull Requests

TBD

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

We recommend using `pre-commit` hooks, which are already set up in `.pre-commit-config.yaml`. In particular, we are using the following checks:

* [black](https://github.com/psf/black)
* [flake8](https://pypi.org/project/flake8/)
* [reorder_python_imports](https://github.com/asottile/reorder_python_imports)
* [pydocstyle](https://pypi.org/project/pydocstyle/)

Therefore, before committing, we recommend installing [pre-commit](https://pre-commit.com/). To have everything set up, please follow these steps:

* `pip install pre-commit`
* `pre-commit install`

Now, before committing, `pre-commit` hooks will be run, and you can ensure the checks are passed before the commit is created.

### Documentation Styleguide

We use restructured text format, this is important as the documentation is hosted in [Read the Docs](https://readthedocs.org/). In particular, `TRUNAJOD` docs can be found in [https://trunajod20.readthedocs.io/en/latest/](https://trunajod20.readthedocs.io/en/latest/).

#### Example

To be added.

## Additional Notes

### Issue and Pull Request Labels

To be added.

[good-first-issue]:https://github.com/dpalmasan/TRUNAJOD2.0/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
[help-wanted]:https://github.com/dpalmasan/TRUNAJOD2.0/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
