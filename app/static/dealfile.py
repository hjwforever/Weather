import json
from django.db import models

def _out_log(request):
    contains = json.loads(_open_andreadfile(request))
    people = request.POST.get("peoples", None)
    version = request.POST.get("versions", None)
    if contains:
        models.result.objects.create(bug_num=contains['total'], anr_num=contains['anr'],
                                     crash_num=contains['crash'], exception_num=contains['exception'],
                                     monkey_is_finish=contains['is_finish'],
                                     name=people, version_num=version, remark="写死到备注")
        list = models.result.objects.all()
        return list
    else:
        models.result.objects.create(bug_num=contains['total'], anr_num=contains['anr'],
                                     crash_num=contains['crash'], exception_num=contains['exception'],
                                     monkey_is_finish=contains['is_finish'],
                                     name=people, version_num=version, remark="写死到备注")


def _open_andreadfile(request):
    File = request.FILES.get("files", None)
    log_out_str = "./app/upload_file/" + File.name
    log_content = open(log_out_str, "r")
    s = log_content.read()
    anr = s.count('ANR')
    crash = s.count('CRASH')
    exception = s.count('Exception')
    monkey_is_finish = s.count('Monkey finished')
    total = anr + crash + exception
    is_finish = False
    if (monkey_is_finish > 0):
        is_finish = True
    log_content.close()
    _result_list = json.dumps(
        {'anr': anr, 'crash': crash, 'exception': exception, 'is_finish': is_finish, 'total': total})
    return _result_list