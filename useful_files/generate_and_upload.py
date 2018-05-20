from subprocess import call
from multiprocessing import Process
import sys
import time

DB_PATH = './automatically_generated_database/'
CLEAN_ANNOTATIONS = True

class MongoDProcess(Process):

    def __init__(self):
        super(MongoDProcess, self).__init__()

    def run(self):
        call(['mkdir', '-p', DB_PATH])
        call(['/bin/sh', '-c', 'mongod --dbpath ' + DB_PATH + ' --config mongod.conf'])

args = sys.argv
if len(args) < 3:
    print('Usage: python generate_and_upload.py <DatabaseName> <AnnotationFile>')
    sys.exit()

DATABASE_NAME = sys.argv[1]
ANNOTATION_NAME = sys.argv[2]

if CLEAN_ANNOTATIONS:
    ANNOTATION_NAME_CLEANED = ANNOTATION_NAME[:-4] + '_cleaned.xml'
    call(['python', '../KnowledgeBase/map_annotation_tool_to_btl_converter.py', ANNOTATION_NAME, ANNOTATION_NAME_CLEANED])


# start mongo deamon
mongod_process = MongoDProcess()
mongod_process.start()

# execute generate example data and wait for it to write everything to the database files
call(['python', '../KnowledgeBase/generate_example_data_clf.py', DATABASE_NAME,  ANNOTATION_NAME])
time.sleep(3)

# terminate the daemon
mongod_process.terminate()

# copy the database to cadmium
call(['scp', DB_PATH + DATABASE_NAME + '.0', 'sync0r@cadmium:/vol/pepper/systems/pepper-robocup-nightly/opt/knowledgebase-current'])
call(['scp', DB_PATH + DATABASE_NAME + '.ns', 'sync0r@cadmium:/vol/pepper/systems/pepper-robocup-nightly/opt/knowledgebase-current'])

# remove evidence all evidence
call(['rm', '-r', DB_PATH])
call(['rm', 'mongodb.log'])
