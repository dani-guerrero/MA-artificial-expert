MEDIA_ROOT = '/home/dani/projects/tigatrapp-dockers/tigatrapp-server/media/'
QUERY_LIMIT = 10
SLEEP_TIME = 3

classifiers = {
    'isInsect': {
        'filename': 'models/isInsect.pth',
        'classifier_db_number': 0,
        'classes': ['insect', 'not-insect'],
        'thresholds': [0.5, 0.5]
    },
    'species': {
        'filename': 'models/whichSpecie.pth',
        'classifier_db_number': 1,
        'classes': ['aegypti','albopictus','anopheles','culex','culiseta','japonicus-koreicus','other_insect','other_mosquito','unidentifiable'],
        'thresholds': [1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]
    }
}