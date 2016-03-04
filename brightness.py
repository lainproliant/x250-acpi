#!/usr/bin/env python
import sys

ACTUAL_BRIGHTNESS = '/sys/class/backlight/intel_backlight/actual_brightness'
MAX_BRIGHTNESS = '/sys/class/backlight/intel_backlight/max_brightness'
BRIGHTNESS = '/sys/class/backlight/intel_backlight/brightness'

def main(argv):
    current_brightness = 0
    max_brightness = 0
    target_brightness = 0

    def print_brightness(header = 'Brightness:'):
        print('%s %d / %d (%d%%)' % (
            header, current_brightness, max_brightness,
            int(float(current_brightness) / float(max_brightness) * 100)))

    with open(ACTUAL_BRIGHTNESS) as infile:
        current_brightness = int(infile.read())

    with open(MAX_BRIGHTNESS) as infile:
        max_brightness = int(infile.read())

    if not argv:
        print_brightness()

    else:
        delta = int(argv[0])

        if argv[0][0] in ('+', '-'):
            target_brightness = current_brightness + delta
        else:
            target_brightness = delta

        target_brightness = max(0, min(max_brightness, target_brightness))

        with open(BRIGHTNESS, 'w') as outfile:
            print('%d' % target_brightness, file = outfile)

        current_brightness = target_brightness

        print_brightness('Set brightness:')

if __name__ == '__main__':
    main(sys.argv[1:])
