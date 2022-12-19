# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 21:24:00 2022

@author: skrob
"""
import os
import json
import sys

first_file_path = sys.argv[1]
second_file_path = sys.argv[2]
merged_file_path = sys.argv[3]

class FileBuffer:  # объектом будет обновляемый буфер для записи в файл фиксированного кол-ва строк

    def __init__(self, file_name: str, max_size: int):
        self.max_size = max_size
        self.storage = []
        self.file_name = file_name

    def add(self, element):     # добавляет в буфер результат сравнения строк из двух файлов
        self.storage.append(element)
        if len(self.storage) == self.max_size:  # когда буфер достигает максимального размера, происходит запись в файл
            self.flush()

    def flush(self):    # запись строк из буфера в файл с последующим обнулением буфера
        if os.path.exists(self.file_name):
            with open(self.file_name, 'a', encoding='UTF-8') as result_file:
                for element in self.storage:
                    result_file.write(json.dumps(element, indent = 4))
        else:
            with open(self.file_name, 'w', encoding='UTF-8') as result_file:
                for element in self.storage:
                    result_file.write(json.dumps(element, indent = 4))
        self.storage = []
        
with open(os.path.realpath(first_file_path), 'r', encoding = 'UTF-8') as first_file, open(os.path.realpath(second_file_path), 'r', encoding = 'UTF-8') as second_file:
    file_storage = FileBuffer(os.path.realpath(merged_file_path), 6)  
    
    element_1 = json.loads(second_file.readline())
    comp_1 = element_1['timestamp']
    element_2 = json.loads(second_file.readline())
    comp_2 = element_2['timestamp']
    cond = comp_2 >= comp_1
    if cond == True:
        file_storage.add(element_1)
    if cond == False:
        file_storage.add(element_2)
        
    while comp_1 != 'a' and comp_2 != 'b':
        if cond == True:
            temp = first_file.readline()
            if temp:
                element_1 = json.loads(temp)
                comp_1 = element_1['timestamp']
            else:
                comp_1 = 'a'
        else:
            temp = second_file.readline()
            if temp:
                element_2 = json.loads(temp)
                comp_2 = element_2['timestamp']
            else:
                comp_2 = 'b'
        cond = comp_2 >= comp_1
        if cond == True:
            file_storage.add(element_1)
        if cond == False:
            file_storage.add(element_2)
    file_storage.flush()
    
        
