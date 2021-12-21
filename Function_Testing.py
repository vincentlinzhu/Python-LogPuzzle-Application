#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

def alphabetical_sort_key(url):
    match = re.search(r'-(\w+)\.jpg', url)
    if match:
        return match.group(1)
    else:
        return url

    
def read_urls_Htable_Method(filename):
    Htable = {}
    hostname = filename[filename.index('_') + 1:] 
    uf = open(filename, 'rU') 
    uf_code = uf.readlines()
    for line in uf_code:
        match = re.search(r'"GET (\S+)', line)
        if match: 
            Get_Image_Path = match.group(1)
            if 'puzzle' in Get_Image_Path:
                Htable['http://' + hostname + Get_Image_Path] = 1
    Sorted_Htable = sorted(Htable.keys(), key = alphabetical_sort_key)
    for element in Sorted_Htable:
        print element
    return Sorted_Htable


def read_urls_List_Method(filename):
    List = []
    hostname = filename[filename.index('_') + 1:] 
    uf = open(filename, 'rU') 
    uf_code = uf.readlines()
    for line in uf_code:
        match = re.search(r'"GET (\S+)', line)
        if match: 
            Get_Image_Path = match.group(1)
            if 'puzzle' in Get_Image_Path and 'http://' + hostname + Get_Image_Path not in List:
                List.append('http://' + hostname + Get_Image_Path)
    Sorted_List = sorted(List, key = alphabetical_sort_key)
    #for element in Sorted_List:
        #print element
    return Sorted_List


def download_images(img_urls, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        
    index = file(os.path.join(dest_dir, 'index.html'), 'w')
    index.write('<html><body>\n')

    i = 0
    for url in img_urls:
        local_name = 'img%s' % i
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
        index.write('<img src="%s">' % (local_name,))
        i += 1
        
    index.write('\n</body></html>\n')
    index.close()

    
def main():
    #img_urls = read_urls_List_Method('place_code.google.com')
    #download_images(img_urls, 'abc')
    
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls_List_Method(args[0])
    
    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
    main()
