# ICS to TXT

Print an ICS calendar in a human readable format.

## Installation

This software requires Python 3. See [Python's website](https://www.python.org/) for installation instructions.

When you have Python 3 installed, install required packages with pip (Python's package management system):

```
pip install ics
pip install pytz
```

Then you can call the executable:

```
./ics-to-txt -h
```

Or you can install this software as a Python package, which will also install all the dependencies and make the executables available globally:

```
python setup.py install

ics-to-txt -h
```

## Usage

Example:

```
ics-to-txt -i mycalendar.ics -fb "2016-01-01" -fn findthis > mycalendar-from-2016-about-findthis.txt
```

## Help

Call any of the scripts mentioned in [Usage](#usage) with the parameter `-h` or `--help` to see full documentation. Example:

```
ics-to-txt -h
```

## Contributing

__Feel free to remix this piece of software.__ See [NOTICE](./NOTICE) and [LICENSE](./LICENSE) for license information.
