import argparse
import datetime

import ics
import tzlocal


def main():
    parser = argparse.ArgumentParser(
        description='ICS to TXT: Print an ICS calendar in a human readable '
        'format'
    )
    parser.add_argument('--input', '-i', dest='inputfile', required=True,
                        help='input ICS file path')
    parser.add_argument('--begin', '-b', dest='filterbegin',
                        type=valid_date,
                        help='print only events newer then or equal to passed '
                        'date; format YYYY-MM-DD')
    parser.add_argument('--name', '-n', dest='filtername',
                        help='print only events the subject of which contains '
                        'passed string; case-insensitive')

    args = parser.parse_args()

    if args.filterbegin:
        tz = tzlocal.get_localzone()
        filterbegin_aware = tz.localize(args.filterbegin)
    else:
        filterbegin_aware = None

    events = parse_ics(args.inputfile)
    events_filtered = filter_events(
        events,
        begin=filterbegin_aware,
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
        return datetime.datetime.strptime(s, '%Y-%m-%d')
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
                timezone = event.begin.datetime.tzinfo
                end = event.end.to(timezone)
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
