import json
import time


def transfer_date(old_value, new_month, new_day):
    iso_formate = "%Y-%m-%dT%H:%M:%S.%fZ"
    normal_format = "%Y-%m-%d"

    time_array = time.strptime(old_value, iso_formate)
    right_time = time.strftime(normal_format, time_array)
    temp_month = right_time.replace('-12', new_month)
    temp_day = temp_month.replace('-31', new_day)

    return temp_day


def format_json(json_file, t_month, t_day):
    j = json.load(open(json_file))

    d = {}
    for key in j:
        print(key, j[key])
        d[transfer_date(key, '-' + t_month, '-' + t_day)] = j[key]

    return d
