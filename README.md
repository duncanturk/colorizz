# Colorizz

**Colorizz** is a Python script designed to apply customized colorization to text based on predefined rules. This script can be used both via the command line and through a simple graphical user interface (GUI).

## Getting Started

### Prerequisites

To run the Colorizz script, you need:

- Python 3.x installed on your machine.
- The `pyperclip` package for clipboard interactions. Install it using the following command:
  ```sh
  pip install pyperclip
  ```

### Usage

To use the script, you can either run it from the command line or open the GUI for interactive colorization.

#### Command Line Usage

```sh
python colorizz.py [--rules RULES_PATH] [--gui] [--replace-clipboard]
```

##### Arguments

- `--rules RULES_PATH`: Path to the JSON file containing colorization rules. If not specified, it defaults to `$XDG_CONFIG_HOME/colorizz/rules.json`.
- `--gui`: Launch the GUI to input and colorize text interactively.
- `--replace-clipboard`: Colorize the text from the clipboard and copy the result back to the clipboard.

##### Examples

1. **Colorize Text Using GUI**

    ```sh
    python colorizz.py --gui
    ```

2. **Colorize Text From Clipboard**

   Copy some text to your clipboard before running this command:

    ```sh
    python colorizz.py --replace-clipboard
    ```

   The colorized version of the text will be copied back to your clipboard.