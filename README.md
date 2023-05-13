# AnyArgs

Get script arguments from the CLI, .conf files, environment variables and/or .env files, with only one syntax!


| CLI  | .conf | .env | env vars | Functionality | 
| ---- | ----- | ---- | -------- | ------------- |
|  ✅  |  ✅   |  ✅  |    ✅    | Add groups & arguments everywhere at once        |
|  ✅  |  ✅   |  ✅  |    ✅    | Get the arguments, no matter where they're set   |
|  ❌  |  ✅   |  ✅  |    ❔    | Save args to a file                              |
|  ❔  |  ❔   |  ❔  |    ❔    | Set list type/duplicate args                     |


✅: Implemented
❔: Planned
❌: Not implemented

## How-To
### Usage
```python
# TODO
```

### Install from pip
```bash
python3 -m pip install AnyArgs 
```

### Clone & run scripts locally
```bash
git clone https://github.com/Denperidge-Redpencil/AnyArgs.git
cd AnyArgs
python3 -m pip install -r requirements.txt
python3 src.AnyArgs
```

### Build & install package locally
```bash
git clone https://github.com/Denperidge-Redpencil/AnyArgs.git
cd AnyArgs
python3 -m pip install --upgrade build setuptools
python3 -m build && python3 -m pip install --force-reinstall ./dist/*.whl
```
*Note: other Python versions can be used!*
