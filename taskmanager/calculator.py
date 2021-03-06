from django.db.models import Max

from taskmanager.models import Day, Availability, WeeklySchedule


def hasConflict(critical, ws):
    criticalIsTransitive = critical.endingTime < critical.startingTime
    critical_end_day = Day.objects.get(id=(critical.day.id - (not criticalIsTransitive) % 7) + 1)
    wsIsTransitive = ws.endingTime < ws.startingTime
    ws_end_day = Day.objects.get(id=(ws.day.id - (not wsIsTransitive) % 7) + 1)

    sameDay = ws.day == critical.day
    almost_sameDay1 = critical_end_day == ws.day
    almost_sameDay2 = ws_end_day == critical.day

    check_days = sameDay | almost_sameDay1 | almost_sameDay2
    if check_days:
        if criticalIsTransitive & wsIsTransitive:
            return True

        if criticalIsTransitive & (
        not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
            secondHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)
        else:
            secondHalfTaken = (critical.startingTime <= ws.startingTime) & (
            critical.endingTime > ws.startingTime)  # ([)]

        if wsIsTransitive & (not ((critical.startingTime >= ws.endingTime) & (critical.endingTime <= ws.startingTime))):
            firstHalfTaken = (critical.startingTime < ws.endingTime) | (critical.endingTime > ws.startingTime)
        else:
            firstHalfTaken = (ws.startingTime <= critical.startingTime) & (
            critical.startingTime < ws.endingTime)  # [(])

        return secondHalfTaken | firstHalfTaken


def update_ws_total_weight(av):
    ws_list = WeeklySchedule.objects.all()
    for ws in ws_list:
        if av.task == ws.task:
            temp = Availability.objects.filter(user=av.user, task=av.task, instanceId=av.instanceId).aggregate(
                Max('totalWeight'))
            ws.totalWeight = temp.get("totalWeight__max")
            ws.save()


def arrangeTasks(user):
    availabilityList = Availability.objects.filter(user=user).order_by('-totalWeight')
    while availabilityList:
        availability = availabilityList.first()
        weeklySchedule = WeeklySchedule.objects.filter(user=user, task_id=availability.task,
                                                       instanceId=availability.instanceId).first()

        weeklySchedule.startingTime = availability.startingTime
        weeklySchedule.day = availability.day
        ws_list = WeeklySchedule.objects.filter(user=user, valid=True)
        flag = False
        for ws in ws_list:
            if hasConflict(weeklySchedule, ws):
                flag = True
                break
        if not flag:
            weeklySchedule.valid = True
            weeklySchedule.save()
            availabilityList = availabilityList.exclude(task_id=availability.task, instanceId=availability.instanceId)
        availabilityList = availabilityList.exclude(id=availability.id)
    return True
