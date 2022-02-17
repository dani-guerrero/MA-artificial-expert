import time
import db_queries as q
import settings

from inference import Classifier


def getPendingReports():
    return q.runSQL(
    f"""SELECT * FROM tigaserver_app_report report
    JOIN tigaserver_app_photo photo ON report."version_UUID"=photo.report_id
        WHERE 
            EXTRACT(year FROM creation_time) != 2014
            AND type='adult'
            AND note NOT LIKE '%#345%'
            AND report.report_id NOT IN
                (SELECT report_id FROM tigaserver_app_report WHERE version_number=-1 GROUP BY report_id, user_id)
            AND "version_UUID" IN
                (SELECT "version_UUID" FROM tigaserver_app_report r,(SELECT report_id, MAX(version_number) AS higher FROM tigaserver_app_report GROUP BY report_id) maxes WHERE r.report_id = maxes.report_id AND r.version_number = maxes.higher)
            LIMIT {settings.QUERY_LIMIT}""")

def infer(photos):
    for row in photos:
        print(row['version_UUID'],row['photo'])

if __name__ == '__main__':
    while True:
        photos = getPendingReports()
        inference_results = infer(photos)
        #insertResults(inference_results)
        #hideReports(inference_results)
        time.sleep(settings.SLEEP_TIME)