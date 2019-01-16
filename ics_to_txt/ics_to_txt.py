import argparse
import datetime
import quopri
from dataclasses import dataclass
from functools import partial, reduce

import ics
import tzlocal


@dataclass
class Event:
    name: str
    begin: str
    end: str
    duration: int
    all_day: bool

    @property
    def date(self):
        return self.begin.strftime('%F')

    @property
    def time(self):
        if self.all_day:
            return ''
        return '{} - {}'.format(
            self.begin.strftime('%H:%M'),
            self.end.strftime('%H:%M')
        )

    @property
    def hours(self):
        if self.all_day:
            return ''
        return '{:.2f}h'.format(self.duration / 3600)


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid date: "{0}".'.format(s)
        raise argparse.ArgumentTypeError(msg)


def filter_events_newer_than(events, begin):
    if not begin:
        return events
    tz = tzlocal.get_localzone()
    begin_localized = tz.localize(begin)
    return filter(lambda event: event.begin > begin_localized, events)


def filter_events_by_name(events, name):
    if not name:
        return events
    return filter(
        lambda event: name.lower() in event.name.lower(),
        events
    )


def parse_ics(file_path):
    with open(file_path) as f:
        calendar = ics.Calendar(f)
        for event in calendar.events:
            end_minus_one_day = event.end.datetime - datetime.timedelta(days=1)
            if event.begin.datetime == end_minus_one_day:
                all_day = True
                end = event.begin
            else:
                all_day = False
                timezone = event.begin.datetime.tzinfo
                end = event.end.to(timezone)
            try:
                name = quopri.decodestring(event.name).decode()
            except ValueError:
                name = event.name
            yield Event(
                name=name,
                begin=event.begin.datetime,
                end=end.datetime,
                duration=event.duration.seconds,
                all_day=all_day
            )


def print_event(event):
    print(f'{event.date}  {event.time:>13}  {event.hours:>6}  {event.name}')


def chain(*funcs):
    def wrapped(x):
        return reduce(lambda x, y: y(x), funcs, x)
    return wrapped


def main():
    parser = argparse.ArgumentParser(
        description=('ICS to TXT: Print an iCalendar (.ics) file in a '
                     'human-readable plain text format.')
    )
    parser.add_argument(
        '--input', '-i',
        dest='input_file',
        required=True,
        help='input ICS file path'
    )
    parser.add_argument(
        '--begin',
        '-b',
        dest='filter_begin',
        type=valid_date,
        help=('print only events newer than or equal to passed date; '
              'format: YYYY-MM-DD')
    )
    parser.add_argument(
        '--name',
        '-s',
        dest='filter_name',
        help=('print only events the name of which contains passed string '
              '(case-insensitive)')
    )
    args = parser.parse_args()
    chain(
        parse_ics,
        partial(filter_events_newer_than, begin=args.filter_begin),
        partial(filter_events_by_name, name=args.filter_name),
        partial(sorted, key=lambda event: event.begin),
        partial(map, print_event),
        list
    )(args.input_file)
