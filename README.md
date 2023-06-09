# AnyArgs

Get script arguments from the CLI, .conf files, environment variables and/or .env files, with only one syntax!


| CLI  | .conf | .env | env vars | Functionality | 
| ---- | ----- | ---- | -------- | ------------- |
|  ✅  |  ✅   |  ✅  |    ✅    | Add groups & arguments everywhere at once        |
|  ✅  |  ✅   |  ✅  |    ✅    | Load arguments, no matter where they're set      |
|  ❌  |  ✅   |  ✅  | ❕[*](#save-to-env-vars) | Save/export args                  |
|  ❔  |  ❔   |  ❔  |    ❔    | Set list type/duplicate args                     |


✅: Implemented
❕: Implemented with caveats
❔: Planned
❌: Not implemented

*: [Save/export to env vars](#save-to-env-vars)

## How-To
### (Project) Install from pip
```bash
python3 -m pip install AnyArgs 
```

### (Code) Basic usage 
In just a few lines of code, you can allow your users to set args in whatever way they prefer
```python
# index.py
args = AnyArgs()
args.add_group("Config").add_argument("Username", help="Username for logging in")
args.load_args()
print("Provided username: " + args.get_argument("Username"))
```
<details>
<summary>That's it! With just these lines of code, you've allowed the following</summary>

- A help interface through `python3 index.py -h` or `python3 index.py --help`
- A CLI interface through `python3 index.py --username Denperidge` and `python3 index.py -u Denperidge`
- Allow configuring through a .env in the current working directory with `USERNAME=Denperidge`
- Allow configuring through environment variables with `export USERNAME=Denperidge`
- Allow configuring through a *.conf in the current working directory with 
    ```conf
    [Config]
    Username=Denperidge
    ```


</details>

### (Code) Booleans
```python
# index.py
args = AnyArgs()
args.add_group("Config").add_argument("Load on launch", typestring=ARGTYPE_BOOLEAN, help="Whether to load files on launch", default=False)
args.load_args()
```
And now, a simple `python3 index.py --load-on-launch` is enough to enable load-on-launch!

### (Code) Explicitly defining flags
While AnyArgs will auto-generate some flags, you can always define your own instead to override this behaviour!
```python
# index.py
args = AnyArgs()
args.add_group("Config").add_argument("Username", cli_flags=["--username", "--login", "--email"])
args.load_args()
```

### (Code) Exporting/saving args
```python
# index.py
args = AnyArgs()
args.add_group("Config").add_argument("Username", help="Username for logging in")
args.load_args()
args.save_to(conf_filepath="conf.conf", env_filepath=".env", env_vars=True)  # To only save to one or two of these, simply omit the other values
```
<details>
<summary>Output:</summary>

.env
```conf
# Login
Username=Denperidge
```

conf.conf
```conf
[Login]
username = Denperidge
```

Env_vars:
```python
print("Env: " + environ.get("Username", None))
# Output:
# Env: Denperidge
```

</details>


### (Project) Clone & run tests
```bash
git clone https://github.com/Denperidge-Redpencil/AnyArgs.git
cd AnyArgs
python3 -m pip install -r requirements.txt
python3 -m src.tests
```

### (Project) Clone & run scripts locally
```bash
git clone https://github.com/Denperidge-Redpencil/AnyArgs.git
cd AnyArgs
python3 -m pip install -r requirements.txt
python3 src.AnyArgs
```

### (Project) Clone, build & install package locally
```bash
git clone https://github.com/Denperidge-Redpencil/AnyArgs.git
cd AnyArgs
python3 -m pip install --upgrade build setuptools
python3 -m build && python3 -m pip install --force-reinstall ./dist/*.whl
```

## Reference
### Argtypes
There are different argtypes. Defining them will change how your arguments get handled & parsed.

| Argtype name      | Literal value     | Behaviour                 |
| ----------------- | ----------------- | ------------------------- |
| `ARGTYPE_STRING`  | `"STRING"`        | [View](#argtype_string)   |
| `ARGTYPE_BOOLEAN` | `"BOOL"`          | [View](#argype_boolean)   |
| `ARGTYPE_LIST`    | `"LIST"`          | [View](#argtype_list)     |

#### ARGTYPE_STRING
*Default, will be used when no argtype is defined.*

Simple string storage
##### Resulting CLI:




#### ARGYPE_BOOLEAN


#### ARGTYPE_LIST
Not yet implemented.


### Cli-flag auto-generation
When cli-flags is undefined while defining arguments, AnyArg will try to auto-generate some. Below are some examples that illustrate how auto-generation works.

```python
args.add_group("Login").add_argument("Username", typestring=ARGTYPE_STRING).add_argument("Handle")
```

Will result in the following output syntax:
```bash
usage: example.py [-h] [--username USERNAME] [--handle HANDLE]

optional arguments:
  -h, --help            show this help message and exit

Login:
  --username USERNAME, -u USERNAME
  --handle HANDLE
```
- Long-flag arg under --NAME
- Short-flag using first letter(s) under -N
- If an auto-generated flag would conflict with another (whether that be from the predefined `--help`/`-h` or previously added args), it does not get generated


```python
args.add_group("Save Configuration").add_argument("To .conf", typestring=ARGTYPE_BOOLEAN)
```

Will result in the following output syntax:
```bash
usage: test.py [-h] [--to-conf]

optional arguments:
  -h, --help            show this help message and exit

Save Configuration:
  --to-conf, -tc
```
- Long-flag arg replaces spaces with dashes (` ` -> `-`) and ignores non-letters (~~`.`~~)
- Short-flag ignores non-letters (~~`.`~~) and uses the first letters split by spaces (` `) 


## Discussions
### Save to env vars
First of all: apparently on MacOSX & FreeBSD modifying environ is also [bad news](https://docs.python.org/3/library/os.html#os.environ).

That aside you should note that this - due to limitations of Python (at least without wild workarounds) - is a bit limited. The environment variables should normally get modified for the Python script and its child processes, but not outside of it. This is because Python environ is not persistent outside of the python script runtime.

You can view some explanations and possible workarounds [here](https://stackoverflow.com/a/716046) and the more out of date Python2 discussion [here](https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python).
