import os
def files_merge(file_number,total_no_document):
	files_list=["index/title","index/infobox","index/body","index/reference","index/external","index/category"]
	bifurcated_files=""
	indexing_limit=1000
	total=0
	for files in files_list:
		if total!=0:
			bifurcated_files+=str(total)+":"
			s_out.write(final_string.split('=')[0])
		total=1
		fps=[0]*file_number
		l=[]
		final_string=""
		line=[0]*file_number
		for i in range(file_number):
			f_name=files+str(i+1)
			fps[i]=open(f_name)
			line[i]=fps[i].readline()
			line[i]=line[i].split('\n')[0]
		
		temp_file_name=files.split('/')[0]+"/final_"+files.split('/')[1] # edit from here.. have added counts
		secondary_out=files.split('/')[0]+"/secondary_"+files.split('/')[1]
		s_out=open(secondary_out,'w')
		final_file_name=temp_file_name+"_"+str(total)
#		f1_out=open(temp_file_name,'w')
		f_out=open(final_file_name,'w')
		cur=0
		while(len(set(l))!=file_number):
			listing=[]
			for i in range(file_number):
				if i not in l:
					listing.append((line[i].split('=')[0],i))
			listing.sort()
			indices=[]
			indices.append(int(listing[0][1]))
			for i in range(1,len(listing)):
				if listing[i][0]==listing[0][0]:
					indices.append(int(listing[i][1]))
				else:
					break
			global_count=0
			lengths=[0]*len(indices)
			j=0
			for i in indices:
				count=int((line[i].split('=')[1].split('$')[0]))
				lengths[j]=len(str(count))
				j+=1
				global_count+=count
			final_string=str(listing[0][0])+"="+str(global_count)
			for i in range(len(indices)):
				final_string= final_string+'$'+str(line[indices[i]][len(listing[0][0])+2+lengths[i]:])
			final_string+='\n'
			f_out.write(final_string)
#			f1_out.write(final_string)
			cur+=1
			if(cur==indexing_limit):
				cur=0
				total+=1
				final_file_name=temp_file_name+"_"+str(total)
				f_out=open(final_file_name,'w')
				s_out.write(final_string.split('=')[0]+'\n')
		#	print "----final-----",final_string
			for i in indices:
				line[i]=fps[i].readline()
				line[i]=line[i].split('\n')[0]
				if line[i]=="":
					l.append(i)
	if total!=0:
		bifurcated_files+=str(total)+":"
		s_out.write(final_string.split('=')[0])
	details=open("index/details",'w')
	details.write(bifurcated_files.strip(":")+'\n')
	details.write(str(total_no_document)+'\n')
	details.close()
	for i in range(file_number):
		fps[i].close()
	s_out.close()
#	f1_out.close()
	f_out.close()

