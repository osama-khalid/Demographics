import pandas as pd
import numpy as np
import sys

eFol = sys.argv[1]
time = sys.argv[2]
datType = sys.argv[3]

dataList = np.genfromtxt("time_stamp_day_" + datType,dtype='str')
mergeDf = pd.DataFrame()
expFol = eFol + "/"
result_file = "/result_" + time + "_" + datType + "_mw_prior"
test_tweets_full = "/test_tweets_full_" + time + "_" + datType
test_tweets_full_merged = "/test_tweets_full_"  + time + "_" + datType + "_merged"
final_tweets = expFol + "/finalTweets_" + time + "_" + datType + "_mw.csv"

for fold in [1]:
	for data in dataList:
			print("data = ",fold,data)
			resultFile = expFol + "fold" + str(fold) + "/" + data + result_file
			fullText = expFol + "fold" + str(fold) + "/"+ data + test_tweets_full
			exportPath = expFol + "fold" + str(fold) + "/" + data + test_tweets_full_merged
			df1 = pd.read_csv(resultFile,sep="|")
			df2 = pd.read_csv(fullText)
			df = pd.concat([df2, df1], axis=1)
			df.drop(['Unnamed: 0','user_id','full_tweet','xxx','retweet_flag','city_flag','time_stamp','hash_tags', df.columns.values[-1]], axis=1, inplace=True)
			df.rename(columns={'coordinates':'GroundTruthCoordinate','location':'GroundTruthCity'},inplace=True)
			#---change columns----
			c = df.columns.values.tolist()
			if 'retweet_flag' in c:
				c.remove('retweet_flag')
			if 'IgnoreFlag' in c:
				c.remove('IgnoreFlag')
			if 'nouns' in c:
				c.remove('nouns')

			c = ['IgnoreFlag'] + c
			df = df[c]
			#---
			df.to_csv(exportPath,index=False)
			colList = df.columns.values
			print("colList = ",colList)
			# np.savetxt("finalTweets2.csv",colList,fmt="%s",delimiter="|",newline='|')
			with open(final_tweets,"w") as f:
				f.write("|".join(colList) + "\n")
			break


for fold in range(1,11):
	for data in dataList:
		print("data = ",fold,data)
		try: 
			resultFile = expFol + "fold" + str(fold) + "/" + data + result_file
			fullText = expFol + "fold" + str(fold) + "/"+ data + test_tweets_full
			exportPath = expFol + "fold" + str(fold) + "/" + data + test_tweets_full_merged
			df1 = pd.read_csv(resultFile,sep="|")
			df2 = pd.read_csv(fullText)
			df = pd.concat([df2, df1], axis=1)
			#df.drop(labels=df.columns.values[-1], axis=1,inplace=True)
			df.drop(['Unnamed: 0','user_id','full_tweet','xxx','retweet_flag','city_flag','time_stamp','hash_tags', df.columns.values[-1]], axis=1, inplace=True)
			df.rename(columns={'coordinates':'GroundTruthCoordinate','location':'GroundTruthCity'},inplace=True)
			#---change columns----
			c = df.columns.values.tolist()
			if 'retweet_flag' in c:
				c.remove('retweet_flag')
			if 'IgnoreFlag' in c:
				c.remove('IgnoreFlag')	
			if 'nouns' in c:
				c.remove('nouns')
			c = ['IgnoreFlag'] + c
			df = df[c]
			#---
			#df['IgnoreFlag'] = 0
			df.to_csv(exportPath,index=False)
			df.to_csv(final_tweets, mode="a",header=False,index=False,sep="|")
		except Exception as e:
			print("got error: ",e)
			continue
