import urllib
import xml.etree.ElementTree as ET
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
import fetcher
import xml_parser
import classifier

fetcher.get_match_recursively()
apsched.add_job(fetcher.get_match_recursively, trigger='interval', seconds=1200)
apsched.start() # will block

#x = fetcher.populate_match_details()

#classifier.classify()


