import services.databox_productivity_metrics_sync.get_number_of_today_productive_hours as GetNumberOfTodayProductiveHours
import services.databox_productivity_metrics_sync.get_today_project_progress_percentage as GetTodayProjectProgressPercentage
import services.databox_productivity_metrics_sync.get_today_project_deadline_percentage as GetTodayProjectDeadlinePercentage
import services.databox_productivity_metrics_sync.get_today_distractions_frequency as GetTodayDistractionsFrequency
import utilities.datetime as DatetimeHelper
import constants.instagantt
from utilities.logger import getLogger
from utilities.api_clients.databox_client import getDataboxClient
from utilities.api_clients.instagantt_client import getInstaganttClient
from models.databox import Metric


logTagSyncDataboxProductivityMetric = "[Sync Databox Productivity Metric]"


def Run():
    try:
        databoxClient = getDataboxClient('jeh48rgr8k7cikj3awtkg')
        response = databoxClient.insert_all(buildDataboxSyncData())
    except Exception as error:
        getLogger().error(
            logTagSyncDataboxProductivityMetric + " failed to sync data to Databox productivity's metrics",
            error
        )
        raise error
    return response


def buildDataboxSyncData():
    projects = [
        constants.instagantt.PROJECTS['Baca Buku Awaken The Giant Within'],
        constants.instagantt.PROJECTS['Baca Buku Bangun Kekayaan Investasi Properti'],
        constants.instagantt.PROJECTS['Digitalisasi Surat Berharga'],
    ]

    syncData = [
        Metric("productive.hours", GetNumberOfTodayProductiveHours.Run(), "hours").toDictionary(),
        Metric("distraction.frequency", GetTodayDistractionsFrequency.Run(), "times").toDictionary(),
    ]

    instaganttClient = getInstaganttClient()
    tasks = instaganttClient.getAllTasks(True)
    for project in projects:
        percentageFormat = "{nominal:.0f}"
        progressPercentage = percentageFormat.format(
            nominal=round(GetTodayProjectProgressPercentage.Run(project['section-gid'], tasks), 0))
        deadlinePercentage = percentageFormat.format(
            nominal=round(GetTodayProjectDeadlinePercentage.Run(project['section-gid'], tasks), 0))

        syncData.append(Metric(
            project['x-serial'] + ".progress",
            progressPercentage,
            "%",
        ).toDictionary())

        syncData.append(Metric(
            project['x-serial'] + ".progress.vs.deadline",
            progressPercentage,
            "%",
            "progress",
            DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d"),
        ).toDictionary())

        syncData.append(Metric(
            project['x-serial'] + ".progress.vs.deadline",
            deadlinePercentage,
            "%",
            "deadline",
            DatetimeHelper.getTodayDateInStringFormat("%Y-%m-%d"),
        ).toDictionary())
    return syncData
