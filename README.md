# CEON: Circular Economy Ontology Network

The Circular Economy Ontology Network (CEON) provides a shared vocabulary in the form of a network of ontologies to support efficient decentralized sharing of industry data in circular economies.

## Developer guidelines

The CEON repository uses GitHub Actions to automate the the generation of ontology documentation and to publish content to https://liusemweb.github.io/CEON/. The action is configured to trigger whenever a pull request is merged into the `main` branch.

The code on the `main` branch is stable, properly tested and should be viewed as the latest realease of the code. No changes should be made directly on the `main` branch (see below).

Development happens primarily on the development branch (`develop`), which should ideally always be working, although this is not always realistic. When the development branch has undergone proper testing, a pull request is created, and the changes are merged into `main`.

When developing or adding a new feature, a specific feature branch should be branched off from the development branch (e.g. `feature/awesome_new_feauture`). A new feature should be regarded as any logically connected set of changes or additions, regardless of how many files are being changed.  A feature branch can also be created directly from an issue using the web interface. When the feature branch has undergone sufficient testing, a pull request is created and the changes are merged into `develop`.

When working on an issue it's good to also reference to them in your commit messages. For example:
```bash
$ git commit -m "resolve issue #123"
```
__Note__: GitHub supports a list of keywords that can be used to automatically close an issue using a commit message. such as _close_, _resolve_ or _fix_.

## Getting started

### Requirements
- Git
- Python 3


### Setup
1. Clone the project:
```bash
$ git@github.com:LiUSemWeb/CEON.git
```
__Note__: Support for password authentication is no longer supported on GitHub. Instead, you should use a personal access token. Please see [instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) for more info.

2. Create a virtual environment for Python and install the requirements:
```bash
$ python3 -m venv ceon-venv
$ source ceon-venv/bin/activate
$ pip3 install -r requirements.txt
```


## Adding a ontology pattern or module
TODO


## Build
TODO


## Contact
* Robin Keskisärkkä <robin.keskisarkka@liu.se>
* Huanyu Li <huanyu.li@liu.se>
* Eva Blmoqvist <eva.blomqvist@liu.se>
* Mikael Lindecrantz <mikael.lindecrantz@ragnsells.com>
