"""
Created on Sat Oct 26 18:51:43 2019

@author: furqan.saqib
"""
import zipfile
import datetime
from os.path import basename
import sys
import dateutil.parser as dparser
from datetime import timedelta
#from datetime import date
from zipfile import ZipFile
import os 
import os.path, time

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).date()

def get_all_file_paths(directory,mask,file_type, start_date,end_date): 
    # initializing empty file paths list 
    #print(mask)
    file_paths = []; 
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory):
        for filename in files:
            filename2=filename.upper();
            filepath = os.path.join(root, filename);
            if (root== directory) & (filename2.find(mask.upper())!=-1) & (filename.endswith(file_type)):
                #print(filename)
                #print(filepath)
                modified = modification_date(filepath)
                #start_date=datetime.datetime(start_date)
                if( str(modified)>=str(start_date)) & (str(modified)<=str(end_date)):
                    #print ('modified=' + str(modified))
                    #print(filepath)
                    file_paths.append(filepath)               
    return file_paths        
  
def main(): 
    """
    arguments = len(sys.argv) - 1;
    print(arguments)
    if arguments!=2:
        print("Invalid number of arguments. This Program requires 2 arguments")
    else:
        directory=sys.argv[1]
        mask=sys.argv[2]
        print(mask)
        print(directory)
        # calling function to get all file paths in the directory 
        file_paths = get_all_file_paths(directory,mask)#('D:\\files')
        print('Following files will be zipped:')
        # printing the list of all files to be zipped 
        for file_name in file_paths: 
            print(file_name) # writing files to a zipfile 
        with ZipFile('D:\\files\\'+mask+'.zip','w') as zip: # writing each file one by one 
            for file in file_paths: 
                zip.write(file) 
            for file in file_paths:
                os.remove(file);
        # print('All files zipped successfully!')         
  """
myvars = {};
with open("config.txt") as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2];
        myvars[name.strip()] = str(var)     
File_names=myvars["file_names"].strip();
st_dt=myvars["Start_date"].strip();
end_dt=myvars["End_date"].strip();
Directory=myvars["files_directory"].strip();
zip_directory=myvars["zip_directory"].strip();
file_type=myvars["file_type"].strip();

if st_dt.strip()=='MTD':
    todayDate = datetime.date.today()
    start_date=todayDate.replace(day=1);
else:
    start_date=datetime.datetime.today()- timedelta(int(st_dt))
    start_date=start_date.strftime('%Y-%m-%d')
end_date=datetime.datetime.today()- timedelta(int(end_dt))
end_date=end_date.strftime('%Y-%m-%d')
str_start_date=str(start_date);
str_end_date=str(end_date)

if(File_names.find(',')!=-1):
    File_names = File_names.split(",");
elif(File_names.find(';')!=-1):
    File_names = File_names.split(";");
else: 
    File_names = File_names.split(" ");
    
    
File_names.sort(key=len, reverse=True);
for i in File_names:
    file_paths = get_all_file_paths(Directory,i,file_type,start_date,end_date)#('D:\\files')   
    print(i, 'total files: ', len(file_paths))
    if len(file_paths)>0:  
        #content = file_paths
        fantasy_zip = zipfile.ZipFile(zip_directory+i+str_start_date+'_'+str_end_date+'.zip', 'w')
        #with ZipFile(zip_directory+i+str_start_date+'_'+str_end_date+ '.gzip','w') as zip: # writing each file one by one
        for file in file_paths: 
            #fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'C:\\Stories\\Fantasy'), compress_type = zipfile.ZIP_DEFLATED)
            fantasy_zip.write(file,basename(file),compress_type = zipfile.ZIP_DEFLATED) 
            #os.remove(file);     
fantasy_zip.close();

if __name__ == "__main__": 
    main() 