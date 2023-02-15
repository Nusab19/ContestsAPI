from os import listdir


for i in listdir():
    if not i.endswith(".py") or i == "t.py":
        continue

    with open(i, "r+", encoding="utf8") as f:
        a = f.read().replace("format_time(", "secondsToTime(")
        f.write(a)from os import listdir


for i in listdir():
    if not i.endswith(".py") or i == "t.py":
        continue

    with open(i, "r+", encoding="utf8") as f:
        a = f.read().replace("secondsToTime(", "secondsToTime(")
        f.write(a)
