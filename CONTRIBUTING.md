# Contributing
All contributions are much welcome and greatly appreciated! Expect to be credited for you effort.


## General
Generally try to limit the scope of any Pull Request to an atomic update if possible. This way, it's much easier to assess and review your changes.

You should expect a considerably faster turn around if you submit two or more PRs instead of baking them all into one major PR.


## Types of Contributions
There are many ways you can help out and improve this repository.

### Report Bugs
Report bugs at [gsdatta/nolij/issues][issues].

Consider including the following data in your bug report:

- Any details about your local setup that might be helpful in troubleshooting
- If you can, provide detailed steps to reproduce the bug
- If you don't have steps to reproduce the bug, just note your observations in as much detail as you can. Questions to start a discussion about the issue are welcome.

### Fix Bugs
Look through the [GitHub issues][issues] for bugs. Anything tagged with "bug" is open to whoever wants to implement it. A good idea is also to review the comment thread to see if the issue is already referenced in any open pull requests.

### Implement Features
Look through the [GitHub issues][issues] for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation
nolij could always use more documentation, whether as part of the official nolij docs, in inline docstrings, or even on the web in blog posts, articles, and such.

If you have written your own tutorial or review of the software, please consider adding a refferal link to the repository.

### Submit Feedback
The best way to send feedback is to [open a new issue][issues].

If you are requesting a feature:

- Explain in detail how it would work
- Keep the scope as narrow as possible, to make it easier to implement (atomic)


## Get Started!
Ready to contribute? Here's how to set up `nolij` for local development.

1. Fork the [gsdatta/nolij][repo] repo on GitHub

2. Clone your fork locally:

  ```bash
  $ git clone git@github.com:<your github username>/nolij.git
  ```

3. Install your local copy into a virtualenv using tox. 

  ```bash
  $ tox -e devenv
  ```

4. Create a branch for local development:

  ```bash
  $ git checkout -b name-of-your-bugfix-or-feature
  ```

5. Make you changes locally

6. When you're done making changes, check that your changes pass the tests, with tox:

  ```bash
  $ tox
  ```

7. Commit your changes and push your branch to GitHub:

  ```bash
  $ git add .
  $ git commit
  $ git push origin name-of-your-bugfix-or-feature
  ```

8. Submit a pull request through the GitHub website. 


## Coding conventions
Generally I recommend two ways to stay up-to-date on nolij coding standards.

1. Read and pay attention to current code in the repository

2. Install a plugin for [EditorConfig][editorconfig] and let it handle some of the detailed settings for you.


## Tips
To run a particular test:

```bash
$ python -m pytest tests.test_find.TestFind.test_find_template
```

To run a subset of tests:

```bash
$ python -m pytest tests.test_find
```


[editorconfig]: http://editorconfig.org/
[issues]: https://github.com/gsdatta/nolij/issues
[repo]: https://github.com/gsdatta/nolij
[repo-boards]: https://github.com/gsdatta/nolij/issues#boards
