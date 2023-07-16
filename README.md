# AIS WS feedhandler

<img src="https://img.shields.io/static/v1?label=Languages&message=Python&color=ff0000"/>&nbsp;<img src="https://img.shields.io/static/v1?label=Restriction&message=NO&color=26c601"/> ![GitHub release (latest by date)](https://img.shields.io/github/v/release/lcsrodriguez/AIS-ws-feedhandler) ![python version | 3.10+](https://img.shields.io/badge/Python%20version-3.10+-magenta) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![](https://img.shields.io/badge/Dependabot-enabled-blue)



## Overview

Data provided by the **[AISStream.io](https://aisstream.io/)** API. 
To use it, please sign up using your GitHub account [here](https://aisstream.io/authenticate). 


<p align="center">
    <img alt="Example" width="750px" src="assets/img/ex.png">
</p>



### Project's architecture

```
.
├── AIS/
│   ├── Config.py
│   ├── Scraper.py
│   ├── Usage.py
│   ├── __init__.py
│   ├── constants.py
│   └── utils.py
├── Makefile
├── README.md
├── assets/
│   ├── _empty.config.toml
│   └── img
├── config.toml
├── examples/
│   └── script.py
├── out/
│   ├── cookies
│   ├── plots
│   └── usages
├── requirements.txt
└── setup.py

```

## Getting started

```shell
git clone https://github.com/lcsrodriguez/AIS-ws-feedhandler.git
cd AIS-ws-feedhandler/

python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
pip3 freeze

python3 setup.py sdist bdist_wheel # Build the package from source
```

Run the example script:
```
python3 examples/script.py
```


### ``config.toml`` file structure

```toml
[local]
api.secret_key = "<AISSTREAM API KEY HERE>"
gh.username="<GH_USERNAME HERE>"
gh.password="<GH_PASSWORS HERE>"

[dev]
api.secret_key = ""

[uat]
api.secret_key = ""

[prod]
api.secret_key = ""
```

## License

[MIT](LICENSE)