import xml.sax
import re
from Stemmer import Stemmer
#from stemming.porter2 import stem
import files_merge
import sys
import os
stem=Stemmer('english')
stop_words=[]
document_count=1
max_document_per_file=1000
file_number=1
title_dic={}
infobox_dic={}
body_dic={}
references_dic={}
external_dic={}
category_dic={}
title_file=open("index/list_title",'w')
total_no_document=0
f_info=open('index/infobox1','w')
f_title=open('index/title1','w')
f_body=open('index/body1','w')
f_reference=open('index/reference1','w')
f_external=open('index/external1','w')
f_category=open('index/category1','w')
class ABContentHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.doc_id = ""
		self.title = ""
		self.text = ""
		self.infobox = ""
		self.category = ""
		self.ref = ""
		self.external = ""
		self.rest=""
		self.content =  ""
		self.current = ""
		self.parent = ""
		self.elements = []
	def startElement(self, name, attrs):
		self.elements.append(name)
		if self.current:
			self.parent = self.current
		self.current = name
#			print "*** PAGE STARTS ***"
	def endElement(self, name):
		global stop_words
		global document_count
		global max_document_per_file
		global file_number
		global title_dic
		global infobox_dic
		global body_dic
		global references_dic
		global external_dic
		global category_dic
		global f_info
		global f_title
		global f_body
		global f_reference
		global f_external
		global f_category
		global total_no_document
		content = self.content
		if name=="page":
#			print "** PAGE ENDS ***"
			self.doc_id = ""
			self.title = ""
			self.text = ""
			self.infobox = ""
			self.category = ""
			self.ref = ""
			self.external = ""
			self.rest=""
			self.content =  ""
			self.current = ""
			self.parent = ""
			total_no_document+=1
			if document_count==max_document_per_file:
				for i in sorted(infobox_dic.keys()):
					string=i+"="+infobox_dic[i]+'\n'
					f_info.write(string)
				for i in sorted(title_dic.keys()):
					string=i+"="+title_dic[i]+'\n'
					f_title.write(string)
				for i in sorted(body_dic.keys()):
					string=i+"="+body_dic[i]+'\n'
					f_body.write(string)
				for i in sorted(references_dic.keys()):
					string=i+"="+references_dic[i]+'\n'
					f_reference.write(string)
				for i in sorted(external_dic.keys()):
					string=i+"="+external_dic[i]+'\n'
					f_external.write(string)
				for i in sorted(category_dic.keys()):
					string=i+"="+category_dic[i]+'\n'
					f_category.write(string)
				infobox_dic.clear()
				title_dic.clear()
				body_dic.clear()
				references_dic.clear()
				external_dic.clear()
				category_dic.clear()
				document_count=0
				f_info.close()
				f_title.close()
				f_body.close()
				f_reference.close()
				f_external.close()
				f_category.close()
			if document_count==0:
				file_number+=1
				info="index/infobox"+str(file_number)
				title="index/title"+str(file_number)
				body="index/body"+str(file_number)
				reference="index/reference"+str(file_number)
				external="index/external"+str(file_number)
				category="index/category"+str(file_number)
				f_info=open(info,'w')
				f_title=open(title,'w')
				f_body=open(body,'w')
				f_reference=open(reference,'w')
				f_external=open(external,'w')
				f_category=open(category,'w')
			document_count+=1
			pass
		if name=="id":
			if self.parent == "page":
				self.doc_id = self.content
#				print "ID : " + self.doc_id
				title_file.write(hex(int(self.doc_id))+"|"+self.title)
		if name=="title":
			self.title = self.content
#			print "TITLE : " + self.title
		if name=="text":
			self.text = self.content
			self.parse()
			self.write_infobox()
			self.write_title()
			self.write_body()
			self.write_reference()
			self.write_external()
			self.write_category()
#	  print "Text"
#	  print self.tex
		self.elements.pop()
      		if self.elements:
			self.current = self.parent
			if len(self.elements) ==1:
				self.parent=""
			else:
				self.parent= self.elements[-1]
		else:
			self.current=""
		self.content=""


	def write_infobox(self):
		global infobox_dic
		words_list=set(self.infobox)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in infobox_dic:
				infobox_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.infobox.count(words))
			else:
				string=infobox_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				infobox_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.infobox.count(words))


	def write_title(self):
		global title_dic
		words_list=set(self.title)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in title_dic:
				title_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.title.count(words))
			else:
				string=title_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				title_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.title.count(words))


	def write_body(self):
		global body_dic
		words_list=set(self.rest)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in body_dic:
				body_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.rest.count(words))
			else:
				string=body_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				body_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.rest.count(words))


	def write_reference(self):
		global references_dic
		words_list=set(self.ref)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in references_dic:
				references_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.ref.count(words))
			else:
				string=references_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				references_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.ref.count(words))


	def write_external(self):
		global external_dic
		words_list=set(self.external)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in external_dic:
				external_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.external.count(words))
			else:
				string=external_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				external_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.external.count(words))


	def write_category(self):
		global category_dic
		words_list=set(self.category)
		for words in words_list:
			int_id=int(self.doc_id)
			if words not in category_dic:
				category_dic[words]=str(1)+"$"+str(hex(int_id))+":"+str(self.category.count(words))
			else:
				string=category_dic[words]
				global_count=string.split('$')[0]
				l=len(global_count)
				global_count=str(int(global_count)+1)
				category_dic[words]=global_count+string[l:]+"$"+str(hex(int_id))+":"+str(self.category.count(words))


	def parse(self):
		info_flag=0
		data=""
		lines=self.text.split('\n')
		i=0
		for i in range(0,len(lines)):
			if "{{Infobox" in lines[i] and info_flag==0:
				info_flag=1
				self.infobox+=lines[i]+'\n'
			elif  lines[i]=="}}" and info_flag==1:
				info_flag=2
				break
			elif info_flag==1:
				self.infobox+=lines[i]+'\n'
		for j in range(i+1,len(lines)):
			if lines[j].find("==Reference")!=-1:
				i=j+1
				break
			if(len(lines[j]))>1:
				self.rest+=lines[j]+'\n'
		for j in range(i,len(lines)):
			if (lines[j].find("==")!=-1 and ("Reference" not in lines[j] or "sources" not in lines[j] or "===" not in lines[j]) or ("Category" in lines[j])):# or lines[j].find("")!=-1:
				i=j+1
				break
			if(len(lines[j]))>1 and "==" not in lines[j]:
				self.ref+=lines[j]+'\n'
		for j in range(i,len(lines)):
			if lines[j].find("[[Category")!=-1 or lines[j].find("{{")!=-1:
				i=j
				break
			if(len(lines[j]))>1:
				self.external+=lines[j]+'\n'
		for j in range(i,len(lines)):
			if lines[j].find("[[Category")!=-1:
				x=lines[j].split(':')
				try:
					self.category+=x[1][:len(x[1])-2]+"\n"
				except:
					continue
			else:
				continue
#		print len(stop_words)	
#		print stop_words
#		print "-----Infobox-------"
		self.infobox=[j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.infobox.lower()) if len(j)>0]
		self.infobox=[stem.stemWord(x) for x in self.infobox if x not in stop_words]
#		print self.infobox
#		print "--------Rest-------"
		self.rest=[j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.rest.lower()) if len(j)>0]
		self.rest=[stem.stemWord(x) for x in self.rest if x not in stop_words]
#		print self.rest
#		print "-------References-------"
		self.ref=[j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.ref.lower()) if len(j)>0]
		self.ref=[stem.stemWord(x) for x in self.ref if x not in stop_words]
#		print self.ref
#		print "-----External-------"
		self.external = [j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.external.lower()) if len(j)>0]
		self.external=[stem.stemWord(x) for x in self.external if x not in stop_words]
#		print self.external
#		print "-------Categories-----"
		self.category = [j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.category.lower()) if len(j)>0]
		self.category=[stem.stemWord(x) for x in self.category if x not in stop_words]
#		print self.category
		self.title = [j.strip() for j in re.compile(r'[^A-Za-z]+').split(self.title.lower()) if len(j)>0]
		self.title=[stem.stemWord(x) for x in self.title if x not in stop_words]

 
	def characters(self, content):

		uni = content.encode("utf-8").strip()
		if uni:
			self.content += uni+'\n'
    #print("characters '" + content + "'")
 
def main(sourceFileName):
#	try:
#		os.system("rm body* category* infobox* title* reference* external* final_*")
#	except:
#		pass
	global stop_words
	global stop_words
	global document_count
	global max_document_per_file
	global file_number
	global title_dic
	global infobox_dic
	global body_dic
	global references_dic
	global external_dic
	global category_dic
	global f_info
	global f_title
	global f_body
	global f_reference
	global f_external
	global f_category
	global total_no_document
	f=open("src/stopwords.txt")
	for lines in f.readlines():
		lines=lines.split('\n')[0]
		if len(lines)>0:
			stop_words.append(lines)
	stop_words=set(stop_words)
	source = open(sourceFileName)
	xml.sax.parse(source, ABContentHandler())
	for i in sorted(infobox_dic.keys()):
#		print i,infobox_dic[i]
		string=i+"="+infobox_dic[i]+'\n'
#		print "in main"
		f_info.write(string)
	for i in sorted(title_dic.keys()):
		string=i+"="+title_dic[i]+'\n'
		f_title.write(string)
	for i in sorted(body_dic.keys()):
		string=i+"="+body_dic[i]+'\n'
		f_body.write(string)
	for i in sorted(references_dic.keys()):
		string=i+"="+references_dic[i]+'\n'
		f_reference.write(string)
	for i in sorted(external_dic.keys()):
		string=i+"="+external_dic[i]+'\n'
		f_external.write(string)
	for i in sorted(category_dic.keys()):
		string=i+"="+category_dic[i]+'\n'
		f_category.write(string)
	infobox_dic.clear()
	title_dic.clear()
	body_dic.clear()
	references_dic.clear()
	external_dic.clear()
	category_dic.clear()
	document_count=0
	f_info.close()
	f_title.close()
	f_body.close()
	f_reference.close()
	f_external.close()
	f_category.close()
	files_merge.files_merge(file_number,total_no_document)
	os.system("rm index/body* index/category* index/infobox* index/title* index/reference* index/external*")

	
if __name__ == "__main__":
	main(sys.argv[1])
