import time
import db_queries as q
import settings

import pandas as pd

from inference import Classifier
from fasterRCNN import Cropper


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
    results = {}
    for report,group in df.groupby('report_id'):
        for _,photo in group.iterrows():
            report_scores = [[]] * len(classifier['classes'])
            print(scores)
            for idx,s in enumerate(scores[photo['photo']]):
                if s >= classifier['thresholds'][idx]:
                    report_scores[idx].append(s)

            results[report] = list(map(sum,report_scores)).index(max(map(sum,report_scores)))

    return results


def infer(photos):
        photoList = list(map(lambda row: row['photo'], photos))
        isInsect_classifier = settings.classifiers['isInsect']

        insectScore = Classifier(isInsect_classifier['filename'],photoList).scores
        insect_classification = classifyReports(isInsect_classifier,photos,insectScore)

        cropList = [row['photo'] for row in photos 
            if isInsect_classifier['classes'][insect_classification[row['report_id']] == 'insect']]

        crops = Cropper(cropList).boxes

        species_classifier = settings.classifiers['species']
        speciesScore = Classifier(species_classifier['filename'],cropList,crops).scores
        #escriure tots els scores a bdd

        #species_classification = classifyReports(species_classifier,photos,speciesScore)
        print(species_classification)

def countReports(photos):
    df = pd.DataFrame.from_records(photos,columns=photos[0].keys())
    return df['report_id'].nunique()

if __name__ == '__main__':
    while True:
        finished = False
        while not finished:
            photos = getPendingReports()
            nReports = countReports(photos) 
            finished = nReports < settings.QUERY_LIMIT
            if nReports > 0:
                inference_results = infer(photos)
                #insertResults(inference_results)
                #hideReports(inference_results)
        time.sleep(settings.SLEEP_TIME)