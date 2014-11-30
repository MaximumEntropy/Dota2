import urllib
import xml.etree.ElementTree as ET
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
import fetcher
import xml_parser
import classifier

file_handler_match_id = open('match_ids.txt','r')
file_handler_match_id_manu = open('post_mid_term_ids.txt','r')
#file_handler_features = open('match_features.csv','a')
file_handler_features = open('feature_vectors.csv','r')

file_handler_features_heroes = open('bigram_features.csv','r')

'''
fetcher.get_match_recursively()
apsched.add_job(fetcher.get_match_recursively, trigger='interval', seconds=1200)
apsched.start() # will block
'''

#x = fetcher.populate_match_details()

classifier.classify(file_handler_features_heroes,file_handler_features)

#fetcher.get_xml_games(file_handler_match_id_manu)


