#!/usr/bin/env python3
import sys

BACKLIGHT = "/sys/class/backlight/amdgpu_bl1"

MAX_BRIGHTNESS = f"{BACKLIGHT}/max_brightness"
BRIGHTNESS = f"{BACKLIGHT}/brightness"

def clear_line():
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()

def pct_of(total, ratio):
    return int(round((float(ratio) / float(total)) * 100))

def pct_ratio(total, pct):
    return int(round((pct / 100) * float(total)))

def read_brightness(file=BRIGHTNESS):
    with open(file, "r") as infile:
        return int(infile.read())

def write_brightness(value):
    with open(BRIGHTNESS, "w") as outfile:
        print(f"{value}", file=outfile)
    return read_brightness()

def print_brightness(header="Brightness:"):
    current_brightness = read_brightness()
    max_brightness = read_brightness(MAX_BRIGHTNESS)

    print(
        "%s %d / %d (%d%%)"
        % (
            header,
            current_brightness,
            max_brightness,
            pct_of(max_brightness, current_brightness),
        )
    )

def main(argv):
    current_brightness = 0
    max_brightness = 0
    target_brightness = 0

    current_brightness = read_brightness()
    max_brightness = read_brightness(MAX_BRIGHTNESS)

    if not argv:
        print_brightness()

    else:
        pct = int(argv[0])
        current_pct = pct_of(max_brightness, current_brightness)

        if argv[0][0] in ("+", "-"):
            pct = current_pct + pct

        pct = max(0, min(100, pct))
        target_brightness = int((pct / 100) * max_brightness)
        write_brightness(target_brightness)

        print_brightness("Set brightness:")


if __name__ == "__main__":
    main(sys.argv[1:])
