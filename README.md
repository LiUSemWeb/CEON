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

## Adding a ontology pattern or module
The easiest way to publish a new ontology or ontology module is to follow the steps below:

1. Checkout the `develop` branch and pull the latest changes
```bash
$ git checkout develop
$ git pull
```
2. Create a new branch (e.g., `update-actor-module-to-version-1.0`)
```bash
$ git checkout -b update-actor-module-to-version-1.0
```
3. Add your ontology or ontology module to the `ontology/` directory, e.g. `ontology/modules/actor/1.0/actor.owl`
4. Add config info about the file to `config.yml`:
```yml
  - source: "ontology/modules/actor/1.0/actor.owl"
    path: "ontology/modules/actor/"
    version: "1.0"
    latest: true
```
5. (optional) Build and check the output
```bash
6 ./build.py
```
7. Add, commit and push:
```bash
$ git add ontolgies/ config.yml
$ git commit -m "update actor module to version 1.0"
$ git push origin update-actor-module-to-version-1.0
```
8. From the GitHub page, create a pull request from your branch to `develop`.
9. Done!

## Building locally
Building the documentation locally is a great way to verify that you don't have any obvious errors in your ontology, and that nothing is missing. The same files are generated in the in `main` branch automatically.

### Requirements
- Git
- Python 3
- Java 8 (or higher)

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

3. Build the documentation
```bash
$ ./build.py
```

4. __(optional)__ Host the generated documentation locally:
```bash
$ python3 -m "http.server" -d ./docs 
# navigate to http://localhost:8000/
```

## Versioning
Releases are deployable iterations of the repo that can be packaged and made available for download and use. The project uses semantic version numbering for releases following the pattern: MAJOR.MINOR.PATCH:
- Patch releases (e.g., going from version v1.0.1 to version v1.0.2) indicate bug fixes or trivial updates)
- Minor releases (e.g. going from version v1.0.2 to v1.1.0) indicate a change to functionality. This can be any functionality change or new functionality but should not break backward compatability
- Major releases (e.g. going from version v1.1.0 to version v2.0.0) indicate changes that significantly alter functionality or might break backward compatibility
 
Releases are created by adding a release tag in the GitHub web interface, which marks a specific commit as meaningful in some way. Each new release should be accompanied by release notes:
- A patch release should contain a list of bugfixes
- A minor release should contain a list of changes and usage details
- A major release should contain a list of removals, a list of additions, and instructions on how to upgrade from the previous version (if needed)
 
## Pre-releases
It sometimes useful to be able to publish a release before all the features are developed and tested. In these cases, the use of semantic versioning still applies; however, the release should be tagged with, e.g., a `beta` suffix. In the GitHub web interface, define the new tag name (e.g. `v1.0.0-beta`) and then check the radio button `Set as a pre-release` prior to publishing the release. When the release has been tested, create a new release without the beta suffix.

## Initial development
Any release with major version zero (e.g., `v0.1.0`) is part of initial development. This indicates that the ontologies should not be considered stable, and that anything may change at any time. This also means that nothing is considered a *breaking change* until the first non-zero major release. Developers are free to add alternative tags with suffixes to add meaning to these early releases (e.g. release `v0.1.0` could at the same time be tagged with `v1.0.0-prototype1`).



## Contact
* Robin Keskisärkkä <robin.keskisarkka@liu.se>
* Huanyu Li <huanyu.li@liu.se>
* Eva Blomqvist <eva.blomqvist@liu.se>
* Mikael Lindecrantz <mikael.lindecrantz@ragnsells.com>
