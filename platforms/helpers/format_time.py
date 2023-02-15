def secondsToTime(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    result = ""
    if d > 0:
        result += f"{d} day{'s' if d > 1 else ''}"
    if h > 0:
        result += f" {h} hour{'s' if h > 1 else ''}"
    if m > 0:
        result += f" {m} minute{'s' if m > 1 else ''}"
    if not result:
        result = "0 minutes"
    return result.strip()


def timeToSeconds(duration):
    parts = duration.split()
    units = {
        'days': 24 * 60 * 60,
        'hours': 60 * 60,
        'minutes': 60,
        'day': 24 * 60 * 60,
        'hour': 60 * 60,
        'minute': 60}

    total = sum(int(parts[i - 1]) * units[parts[i]]
                for i in range(1, len(parts), 2))

    return total
