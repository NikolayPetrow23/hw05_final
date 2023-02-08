import datetime


def year(reqeust):
    return {
        'year': int(datetime.datetime.now().strftime("%Y")),
    }
