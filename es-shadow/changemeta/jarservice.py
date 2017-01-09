# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import zipfile
import shutil

JAR_SERVICE_PREFIX = 'META-INF/services/'
JAR_SERVICE_PREFIX_LEN = len(JAR_SERVICE_PREFIX)

def prepareLocalServiceDir(local_services_dir = '/tmp/services'):
    if os.path.exists(local_services_dir):
        if os.path.isdir(local_services_dir):
            shutil.rmtree(local_services_dir)
 #           os.removedirs(local_services_dir)
        else:
            os.remove(local_services_dir)
    os.makedirs(local_services_dir)

# 适合较小的文件
def readZipFile(filePath, local_service_dir = '/tmp/services'):
    servicesFileList = []
    zipFileHandler = zipfile.ZipFile(filePath, 'r')
    for zipFile in zipFileHandler.namelist():
        if zipFile.startswith(JAR_SERVICE_PREFIX) and \
           len(zipFile) > JAR_SERVICE_PREFIX_LEN:
            resultFile = os.path.split(zipFile)[1]\
                                .replace('org.apache.lucene', 'org.apache.lucene.sfck')\
                                .replace('com.fasterxml', 'com.fasterxml.sfck')
            with open(os.path.join(local_service_dir,resultFile), 'a' ) as wfile:
                wfile.write('# ' + os.path.split(filePath)[1] + '\n')
                with zipFileHandler.open(zipFile, 'r') as serviceFile:
                    lines = serviceFile.readlines()
                    for line in lines:
                        line = line.decode('utf-8').strip()
                        if line and not line.startswith('#'):
                            wfile.write(line\
                                .replace('org.apache.lucene', 'org.apache.lucene.sfck')\
                                .replace('com.fasterxml', 'com.fasterxml.sfck') + '\n')
                    wfile.write('\n')
            servicesFileList.append(zipFile)
    zipFileHandler.close()
    return servicesFileList


if __name__ == '__main__':
    LIBDIRPATH = '/Users/lx/opt/ELK/elasticsearch-2.4.1/lib'
    LOCAL_SERVICES_DIR = os.path.join(os.path.split(__file__)[0], JAR_SERVICE_PREFIX)
    prepareLocalServiceDir(LOCAL_SERVICES_DIR)
    if os.path.isdir(LIBDIRPATH):
        fileList = os.listdir(LIBDIRPATH)
        for file in fileList:
            if (file.startswith('lucene') or file.startswith('jackson')):
                filePath = os.path.join(LIBDIRPATH, file)
                if zipfile.is_zipfile(filePath):
                    content = readZipFile(filePath, LOCAL_SERVICES_DIR)
                    print(file)
                    print(content)
    else :
        print('LIBDIRPATH is not dir')
