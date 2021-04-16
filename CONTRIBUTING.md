# Contributing to TRUNAJOD

:+1::tada: Thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to `TRUNAJOD`. These are mostly guidelines, however there are some special steps you need to be aware of when creating a pull request so we end up with a standardized code. Please feel free to propose changes to this document in a PR.

#### Table Of Contents

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)
  * [Documentation Styleguide](#documentation-styleguide)

## How Can I Contribute?

### Reporting Bugs

If you encounter a bug or something in the functionality does not seem right, feel free to file an issue in the Github issue tracker. Ideally, provide an isolated example on how to reproduce the issue. The minimal information to help us assess the bug/issue:

* Clear description of the bug
* Current behavior and expected behavior
* Ideally a minimal example on how to reproduce it. We know that it is not always straightforward doing this, so this is optional.

### Suggesting Enhancements

Feel free to suggest any enhancement. Note that if you'd like a certain new index to be implemented, please provide in the description a reference paper or article, so we understand better what the enhancement is about and how can we make sure it is correctly implemented. 

We accept any kind of enhancements, so if you feel that usability, API, documentation can be improved, feel free to submit an issue.

### Your First Code Contribution

Unsure where to begin contributing to `TRUNAJOD`? You can start by looking through these `good-first-issue` and `help-wanted` issues:

* [Good first issue][good-first-issue] - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] - issues which should be a bit more involved than `good first issue` issues.

### Pull Requests

Feel free to submit a pull request if you have a proposal for a feature or bugfix. However, make sure that the changes description are clear and you provide unit tests for the new code. Moreover, make sure that all the worflows in the CI (Github actions) pass, as we'd prefer not having regressions on the test cases. Finally, make sure to add citations if you add an algorithm. This will involve updating the `.bib` file for the updated module and making sure that you add the citation in the docstring of the new function. For example:

```python
def d_estimate(
    doc: Doc, min_range: int = 35, max_range: int = 50, trials: int = 5
) -> float:
    r"""Compute D measurement for lexical diversity.

    The measurement is based in :cite:`richards2000measuring`. We pick ``n``
    numbers of tokens, varying ``N`` from ``min_range`` up to ``max_range``.
    For each ``n`` we do the following:

    # Continues...
    """
```

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

Now, before committing, `pre-commit` hooks will be run, and you can ensure the checks are passed before the commit is created. Finally, make sure that you use typehints for the new functions you define, as we are planning to add `mypy` checks to the workflows.

### Documentation Styleguide

We use restructured text format, this is important as the documentation is hosted in [Read the Docs](https://readthedocs.org/). In particular, `TRUNAJOD` docs can be found in [https://trunajod20.readthedocs.io/en/latest/](https://trunajod20.readthedocs.io/en/latest/).

You can test the docs locally by running `sphinx-build -a -b html -W docs/ docs/_build/`. You might need to run `pip install -r docs/requirements.txt` in order to properly generate the documentation. Finally, you can check the docs by opening `docs/_build/index.html` file in your favorite browser.

[good-first-issue]:https://github.com/dpalmasan/TRUNAJOD2.0/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
[help-wanted]:https://github.com/dpalmasan/TRUNAJOD2.0/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
