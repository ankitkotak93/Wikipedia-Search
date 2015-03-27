import bisect
import math
import re
from Stemmer import Stemmer
stem=Stemmer('english')
f=open("src/stopwords.txt")
details=open("index/details")
secondary_counts=(details.readline().strip("\n")).split(":")
total_no_documents=details.readline().strip('\n')
document_names={}
title_file=open("index/list_title")
for lines in title_file.readlines():
	if "|" in lines:
		try:
			document_names[lines.split("|")[0]]=lines.split("|")[1].strip("\n")
		except:
			continue
#print secondary_counts,total_no_documents
total_no_documents=int(total_no_documents)
ranked_documents={}
stop_words=[]
for lines in f.readlines():
	lines=lines.split('\n')[0]
	if len(lines)>0:
		stop_words.append(lines)
stop_words=set(stop_words)
s_counts={}
indexing_list=[[] for i in range(6)]
files=['index/secondary_title','index/secondary_infobox','index/secondary_body','index/secondary_reference','index/secondary_external','index/secondary_category']
for i in range(6):
	f=open(files[i])
	s_counts[(files[i].split("/")[1]).split("_")[1]]=secondary_counts[i]
	for x in f.readlines():
		try:
			indexing_list[i].append((x.split(" ")[0]).strip("\n"))
		except:
			continue
#print s_counts

fokat={}
fokat["t"]=0
fokat["i"]=1
fokat["b"]=2
fokat["r"]=3
fokat["e"]=4
fokat["c"]=5
no_of_queries=input()
for z in range(no_of_queries):
	documents={}
	query=raw_input()
	query_words=[]
	bitset={}
	if ":" in query:
			parts=query.split(" ")
			for i in parts:
				bitset[stem.stemWord(i.split(":")[1])]=[0 for x in range(6)]
				bitset[stem.stemWord(i.split(":")[1])][fokat[i.split(":")[0]]]=1
				query_words.append(stem.stemWord(i.split(":")[1]))
	else:	
		query_words=[j.strip() for j in re.compile(r'[^A-Za-z]+').split(query.lower()) if len(j)>0]
		query_words=[stem.stemWord(x) for x in query_words if x not in stop_words]
		for i in query_words:
			bitset[i]=[ 1 for x in range(6)]
	#print bitset
	#print query_words
	#print query_words
	for i in query_words:
		for j in range(6):
			if bitset[i][j]!=1:
				continue
			index=bisect.bisect(indexing_list[j],i) #gets the file number in final_type_index.
			if index==s_counts[(files[j].split("/")[1]).split("_")[1]]:
				continue
			else :
				try:
					f_open=open(("index/final_"+((files[j].split("/")[1]).split("_")[1]+"_"+str(index+1))))
				except:
					continue
				for lines in f_open.readlines():
					if lines.split("=")[0]==i:
						rest=lines.split("=")[1]
						g_c=int(rest.split("$")[0])
						if total_no_documents >= 40 * g_c: #rarity of the document
							document_data=rest.split("$")
							document_data=document_data[1:]
							temp_data=[]
							for p in document_data:
								p=p.strip("\n")
								try:
									temp_data.append((int(p.split(":")[1]),p.split(":")[0]))
								except:
									continue
							temp_data=sorted(temp_data,reverse=True)
	#						key=(files[j].split("/")[1]).split("_")[1]
	# define ur heuristics here.. take top 5000 documents or whatever.. here j is the order in which it occurs in my files variable list.. like for j=0, am looking in title
							for q in range(min(5000,g_c)):
								score=temp_data[q][0]*math.log((total_no_documents)/g_c)*(6-j)*(6-j) # heuristic funciton can be 36-i*i too
								if temp_data[q][1] in documents:
									documents[temp_data[q][1]]+=score
								else:
									documents[temp_data[q][1]]=score
						break
	keys=sorted(documents.iterkeys(), key=lambda k: documents[k] ,reverse=True)
	count=0
	for i in keys:
		print document_names[i],documents[i]
		count+=1
		if count==10:
		      break
