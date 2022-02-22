MEDIA_ROOT = '/home/dani/projects/tigatrapp-dockers/tigatrapp-server/media/'
QUERY_LIMIT = 10
SLEEP_TIME = 3

fasterRCNN = {
    'filename': 'models/fasterRCNN.pth',
    'batch_size': 32,
}
classifiers = {
    'isInsect': {
        'filename': 'models/isInsect.pth',
        'batch_size': 32,
        'classifier_db_number': 0,
        'classes': ['insect', 'not-insect'],
        'thresholds': [0.5, 0.5]
    },
    'species': {
        'filename': 'models/whichSpecie.pth',
        'batch_size': 32,
        'classifier_db_number': 1,
        'classes': ['aegypti','albopictus','anopheles','culex','culiseta','japonicus-koreicus','other_insect','other_mosquito','unidentifiable'],
        'thresholds': [1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]
    }
}