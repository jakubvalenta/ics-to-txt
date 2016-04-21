# ICS to TXT

Print an ICS calendar in a human readable plain text format.

## Installation

This software requires Python 3. See [Python's website](https://www.python.org/) for installation instructions.

When you have Python 3 installed, install required packages with pip (Python's package management system):

```
pip install ics
pip install tzlocal
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

Use required parameter `-i` to specify the input CSV file.

Use optional parmater `-b` to print only events newer then or equal to a date.

Use optional parameter `-n` to print only events the subject of which contains passed string (case-insensitive).

The plain text output is written to stdout.

### Example

```
ics-to-txt -i mycalendar.ics -b "2016-01-01" -n findthis > mycalendar-from-2016-about-findthis.txt
```

Example output:

```
2015-12-11  15:00 - 21:00   6.00h  Foobar my event title
2015-12-12  14:00 - 16:00   2.00h  Important meeting
2015-12-13                         An all day event
```

The third column is the duration of the event in hours.

## Caveats

To keep the output simple, ICS to TXT prints events spanning more than one day as single day events. For example an event starting on 2015-12-11 at 22:00 and ending on 2015-12-12 at 07:00 will be printed as

```
2015-12-11  22:00 - 07:00   9.00h  Polygon
```

but if the event was to end on 2015-12-__13__ at 07:00 it will still be printed in the same way as above:

```
2015-12-11  22:00 - 07:00   9.00h  Polygon
```

## Help

Call the executable mentioned in [Usage](#usage) with the parameter `-h` or `--help` to see full documentation. Example:

```
ics-to-txt -h
```

## Contributing

__Feel free to remix this piece of software.__ See [NOTICE](./NOTICE) and [LICENSE](./LICENSE) for license information.
