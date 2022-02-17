import time
import db_queries as q
import settings

import pandas as pd

from inference import Classifier


def getPendingReports():
    fields = 'photo.report_id, photo.photo'
    return q.runSQL(#TODO check if not already assigned
    f"""SELECT {fields} FROM tigaserver_app_report report
    JOIN tigaserver_app_photo photo ON report."version_UUID"=photo.report_id
        WHERE 
            EXTRACT(YEAR FROM creation_time) != 2014
            AND type='adult'
            AND note NOT LIKE '%#345%'
            AND report.report_id NOT IN
                (SELECT report_id FROM tigaserver_app_report WHERE version_number=-1 GROUP BY report_id, user_id)
            AND "version_UUID" IN
                (SELECT "version_UUID" FROM tigaserver_app_report r,(SELECT report_id, MAX(version_number) AS higher FROM tigaserver_app_report GROUP BY report_id) maxes WHERE r.report_id = maxes.report_id AND r.version_number = maxes.higher)
            LIMIT {settings.QUERY_LIMIT}""")

def classifyReports(classifier, photos, scores):
    df = pd.DataFrame.from_records(photos,columns=photos[0].keys())
    for report,group in df.groupby('report_id'):
        for photo in group.iterrows():
            print(photo)


def infer(photos):
        photoList = list(map(lambda row: row['photo'], photos))

        isInsect_classifier = settings.classifiers['isInsect']

        insectScore = Classifier(isInsect_classifier['filename'],photoList).scores
        insect_classification = classifyReports(isInsect_classifier,photos,insectScore)

        #cropList = [row['photo'] for row in photos if insect_classification[row['report_id'] == 'insect']
        #crops = Cropper(cropList)

        #species_classifier = settings.classifiers['species']
        #speciesScore = Classifier(species_classifier['filename'],cropList,crops).scores)
        #insect_classification = classifyReports(species_classifier,photos,speciesScore)


        #f"""INSERT INTO tigacrafting_classificationscores
        #    VALUES {map(lambda row: )}"""


if __name__ == '__main__':
    while True:
        finished = False
        while not finished:
            photos = getPendingReports()
            nReports = 1#countReports(photos) 
            finished = True # nReports < settings.QUERY_LIMIT
            if nReports > 0:
                inference_results = infer(photos)
                #insertResults(inference_results)
                #hideReports(inference_results)
        time.sleep(settings.SLEEP_TIME)