import os
import json
import codecs
#This class is written for supplying basic I/O operations

# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)

#Control whether or not file exists in that path
def fileExists(path):
    if os.path.isfile(path):
        return 1
    else:
        return 0

# Create queue and crawled files (if not created)
def create_data_files_for_spiders(project_name, base_url):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled_links.txt")

    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,base_url)



def create_data_files_for_transaction(project_name):
    visited_company_pages=os.path.join(project_name,"visited_company_pages.txt")
    if not os.path.isfile(visited_company_pages):
        try:
            open(visited_company_pages, 'x')
        except FileExistsError:
            pass

# Create a new file
def write_file(path, data):
    with open(path, 'w',encoding='utf-8') as f:
        f.write(data)
# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a',encoding="utf-8") as file:
        file.write(data + '\n')

# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt',encoding="utf-8") as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results
#Read a file and convert each line to a list
def file_to_list(file_name):
    results = list()
    with open(file_name, 'rt',encoding="utf-8") as f:
        for line in f:
            results.append(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    #index=0
    with open(file_name, "w",encoding="utf-8") as f:
        for l in sorted(links):
            f.write(l + "\n")
#Write string to a file
def string_to_file(content,file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content+"\n")

def string_append_to_file(content, file_name):
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(content + "\n")


#Write list to file in sorted way and eleminate null entries
def list_to_file(the_list,file_name):
    with open(file_name,"w",encoding="utf-8") as f:
        for l in sorted(the_list):
            if l is None:
                continue
            else:
                f.write(l+"\n")
    print('All contents are written to file for the first time!')

#Append to an existing list in sorted way and eleminate null entries
def list_append_to_file(the_list,file_name):
    with open(file_name,"a",encoding="utf-8") as f:
        for l in sorted(the_list):
            if l is None:
                continue
            else:
                f.write(l+"\n")
    print('All contents are appended to existing file succesfully!')

#Bonus: Reads and sorts the existing data in the path and writes a new file or appends to existing one
def sortFile(path):
    readFile="mynet_finans\data_json.txt"
    sortedList=[]
    try:
        with open(readFile, 'rt',encoding="utf-8") as f:
            for line in sorted(f):
                sortedList.append(line.replace('\n', ''))

        if os.path.isfile(path):
            list_append_to_file(sortedList, path)
            print('Data is written to file in sorted fashion to existing file:'+path)
        else:
            list_to_file(sortedList, path)
            print('File created!')
            print('Data is written to file' +path+' in sorted fashion for the first time!')
    except:
        print('Error writing data to files')

def jsonRead(path):
    with codecs.open(path,'r','utf-8-sig') as data_file:
        data = json.load(data_file)
        return data

#Converts a set to a list
def set_to_list(the_set):
    the_list = list(the_set)
    return the_list

#Write in json format also considering the Turkish Characters
def writeJson(data,path):
    with codecs.open(path, 'w','utf-8-sig') as f:
        json.dump(data,f,ensure_ascii=False)
    print('All contents are written to file for the first time!')

#Append in json format also considering the Turkish Characters
def appendJson(data,path):
    feeds=jsonRead(path)
    feeds.extend(data)
    writeJson(feeds,path)

    print('All contents are written to existing file!')


#print(generateID('akbank','akbnk','gokce','asd','1 oy','3 gun once'))
#print(generateID('akbank','akbnk','gokce','asd','1 oy','3 gun once'))
#the_list=jsonRead("mynet_finans/company_data.txt")




