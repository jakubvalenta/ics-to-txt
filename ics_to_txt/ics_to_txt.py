import argparse
import datetime

import ics
import pytz


DATE_FORMAT_IN = '%m/%d/%y %I:%M:%S'
TIMEZONE = pytz.timezone('Europe/Prague')


def main():
    parser = argparse.ArgumentParser(
        description='ICS to TXT: Print an ICS calendar in a human readable '
        'format'
    )
    parser.add_argument('--input', '-i', dest='inputfile', required=True,
                        help='input file path')
    parser.add_argument('--filter-begin', '-fb', dest='filterbegin',
                        type=valid_date,
                        help='input file path')
    parser.add_argument('--filter-name', '-fn', dest='filtername',
                        help='input file path')

    args = parser.parse_args()

    events = parse_ics(args.inputfile)
    events_filtered = filter_events(
        events,
        begin=args.filterbegin,
        name=args.filtername
    )
    events_sorted = sorted(events_filtered, key=lambda x: x['begin'])
    [
        print_event(
            x['name'],
            x['begin'],
            x['end'],
            x['duration'],
            x['all_day']
        )
        for x in events_sorted
    ]


def valid_date(s):
    try:
        return TIMEZONE.localize(
            datetime.datetime.strptime(s, '%Y-%m-%d')
        )
    except ValueError:
        msg = 'Not a valid date: "{0}".'.format(s)
        raise argparse.ArgumentTypeError(msg)


def filter_events(events, begin=None, name=None):
    filtered = events
    if begin:
        filtered = filter(lambda x: x['begin'] > begin,
                          filtered)
    if name:
        filtered = filter(lambda x: name.lower() in x['name'].lower(),
                          filtered)
    return filtered


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
                end = event.end.to('local')
            yield({
                'name': event.name,
                'begin': event.begin.datetime,
                'end': end.datetime,
                'duration': event.duration.seconds,
                'all_day': all_day
            })


def print_event(subject, start, end, duration, all_day=False):
    _date = start.strftime('%F')
    if all_day:
        _time = ''
        end = ''
        hours = ''
    else:
        _time = '{} - {}'.format(
            start.strftime('%H:%M'),
            end.strftime('%H:%M')
        )
        hours = '{:.2f}h'.format(duration / 3600)
    print('{date}  {time:>13}  {hours:>6}  {subject}'.format(
        date=_date,
        time=_time,
        hours=hours,
        subject=subject
    ))
