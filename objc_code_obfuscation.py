#coding=utf-8
import os
import sys
import re
import uuid

#use uuid for symbol
def random_symbol():
    symbol = str(uuid.uuid4())
    symbol = symbol.replace('-','')
    return symbol

def prefix_random_symbol():
    symbol = 'hehe'+random_symbol()
    return symbol

def list_project_methods(dir_path):
    file_names = os.listdir(dir_path)
    head_file_suffix = ".h"
    head_file_suffix_len = len(head_file_suffix)
    
    interface_pattern = re.compile("^\s*@interface")
    end_pattern = re.compile("^\s*@end")
    method_pattern = re.compile("^\s*(-|\+)\s*\(")
    '''多参数方法或者单参数方法'''
    method_slice_pattern = re.compile("\)([^:;]+).*")

    method_name_symb_dict = {}

    for name in file_names:
        if name[len(name)-head_file_suffix_len:] != head_file_suffix:
            continue
        head_file_path = os.path.join(dir_path,name)
        head_file = open(head_file_path,"r")
        
        in_interface_body = False
        next_line = head_file.readline()
        while next_line != '':
            interface_matches = re.findall(interface_pattern,next_line)
            if interface_matches and len(interface_matches) >0:
                in_interface_body = True
        
            end_matches = re.findall(end_pattern,next_line)
            if end_matches and len(end_matches) >0:
                in_interface_body = False
            
            if in_interface_body:
                mathod_matches = re.findall(method_pattern,next_line)
                if mathod_matches and len(mathod_matches) >0:
                    method_name_matches = re.findall(method_slice_pattern, next_line)
                    if method_name_matches and len(method_name_matches):
                        exist_method_name = method_name_symb_dict.get(method_name_matches[0])
                        if exist_method_name != None:
                            # print method_name_matches[0]
                            pass
                        else:
                            method_name_symb_dict[method_name_matches[0]] =prefix_random_symbol()
            
            next_line = head_file.readline()

    all_in_one_head_content = ''
    for a_method_name in method_name_symb_dict:
        all_in_one_head_content += "#define %s %s\n"%(a_method_name,method_name_symb_dict[a_method_name])

    return all_in_one_head_content

'''保存头文件'''
def save_head_oneshot(dir_path,content):
    oneshot_name = random_symbol()+'.h'
    oneshot_name = os.path.join(dir_path,oneshot_name)
    oneshot_file = open(oneshot_name,'a')
    oneshot_file.write(content)
    return oneshot_name


if __name__=="__main__":
    argv = sys.argv
    argvLength = len(argv)
    if (argvLength>1):
        entry_path = argv[1]
        if os.path.isdir(entry_path):
            content = list_project_methods(entry_path)
            result_file_name = save_head_oneshot(entry_path,content)
            print u"In Xcode,'Add Files to xxx' with："+result_file_name.decode('utf-8')
        else:
            print u"Please input code directory path"
