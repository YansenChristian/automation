import services.sync_instagantt_to_gcalendar_asana.move_tasks_to_overview_in_asana as MoveTasksToOverviewInAsana
import services.sync_instagantt_to_gcalendar_asana.create_daily_tasks_event_for_each_tasks_in_gcalendar as CreateDailyTasksEventForEachTasksInGCalendar
import services.common.instagantt as InstaganttCommonService
import datetime


def Run():
    tasks = InstaganttCommonService.getAllTasks()
    todayTasks = list(filter(lambda task:
        task.start != "" and task.due != ""
        and datetime.datetime.strptime(task.start, '%Y-%m-%d').date() <= datetime.datetime.today().date() <= datetime.datetime.strptime(task.due, '%Y-%m-%d').date(),
    tasks))

    return {
        'Move Tasks To Overview In Asana': MoveTasksToOverviewInAsana.Run(todayTasks),
        'Create Daily Tasks Event Foreach Tasks In GCalendar': CreateDailyTasksEventForEachTasksInGCalendar.Run(todayTasks)
    }
