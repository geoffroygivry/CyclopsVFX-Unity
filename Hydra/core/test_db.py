from Core.utils import cycGoodies as utils
from datetime import datetime
from pprint import pprint

shots = [{u'status': u'NOT STARTED', u'tasks': [{u'comp': u'Geoffroy'}, {u'lght': u'user1'}], u'name': u'MANOR_010', u'target_date': u'2017-05-17T22:52:29.569000', u'frame_out': 1047, u'frame_in': 1001, u'thumbnail': u'https://s3.amazonaws.com/cyclopsvfx/.MANOR_001_v001_comp.thumbnail.jpg'}, {u'status': u'NOT STARTED', u'tasks': [{u'comp': u'Geoffroy'}], u'name': u'MANOR_020', u'target_date': u'2017-05-31T22:52:29.569000', u'frame_out': 1072, u'frame_in': 1001, u'thumbnail': u'https://s3.amazonaws.com/cyclopsvfx/.MANOR_020_v001_comp_thumbnail.jpg'}, {u'status': u'NOT STARTED', u'tasks': [{u'comp': u'Geoffroy'}], u'name': u'MANOR_030', u'target_date': u'2017-05-20T23:59:59.0000', u'frame_out': 1034, u'frame_in': 1001, u'thumbnail': u'https://s3.amazonaws.com/cyclopsvfx/.MANOR_030_v001_comp.thumbnail.jpg'}]


def sort_by_date(shots):
    overdueList = []
    todayList = []
    tomorrowList = []
    thisWeekList = []
    nextWeekList = []
    laterList = []
    for shot in shots:
        datetime_target_date = utils.convert_isotime_to_datetime(shot.get("target_date"))
        now = datetime.utcnow()
        now_week = now.date().isocalendar()[1]
        datetime_target_date_week = datetime_target_date.date().isocalendar()[1]

        time_diff = datetime_target_date - now
        time_diff_days = time_diff.days
        if time_diff_days < 0:
            overdueList.append(shot)
        elif time_diff_days == 0:
            todayList.append(shot)
        elif time_diff_days == 1:
            tomorrowList.append(shot)
        elif 2 <= time_diff_days <= 6:
            if now_week == datetime_target_date_week:
                thisWeekList.append(shot)
            else:
                nextWeekList.append(shot)
        elif 7 <= time_diff_days:
            if now_week + 1 == datetime_target_date_week:
                nextWeekList.append(shot)
            if now_week + 2 <= datetime_target_date_week:
                laterList.append(shot)

    return {"today": todayList, "tomorrow": tomorrowList, "thisWeek": thisWeekList, "nextWeek": nextWeekList, "later": laterList, "overdue": overdueList}


test_sort = sort_by_date(shots)
pprint(test_sort)
