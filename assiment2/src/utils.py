import datetime
# 1,1293840000,1293840848,952,2021

# 2,1293840001,1293840523,1372,2815

# 3,1293840003,1293840276,856,1149

# 4,1293840004,1293840299,2060,1956

# 5,1293840007,1293841159,2506,1332

times = [
    1293840000,
    1293840001,
    1293840003,
    1293840004,
    1293840007
]

# 处理 unix time
def unix2time(x):
    return datetime.datetime.fromtimestamp(x)

if __name__ == '__main__':
    for t in times:
        print(unix2time(t))
