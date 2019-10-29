# Library
import numpy as np
import math
# Library

# START OF FUNCTION
def read_excel_files(loc):
    import xlrd 
    file = xlrd.open_workbook(loc) 
    sheet = file.sheet_by_index(0)
    return sheet

def show_dataSet(dataSet, number_of_features):
    for i in range (0, len(dataSet)):
        str_row = ""
        for j in range (0, number_of_features):
            str_row += str(dataSet[i][j]) + "\t"
        print(str_row)
    print("Number of Data Set : ", len(dataSet))

def get_std(class_list, avg):
    sum = 0
    for i in range(0, len(class_list)):
        sum += math.pow((float(class_list[i]) - float(avg)), 2)
    variance = sum/len(class_list)
    std = math.sqrt(variance)
    print("std : ", std)
    return std

def get_avg(class_list):
    sum = 0
    for i in range (0, len(class_list)):
        sum += float(class_list[i])
    avg = sum/len(class_list)
    print("avg : ", avg)
    return avg

def cal_Euclidean_Distance(input_test_list, Neighbor_from_dataSet_list, number_of_feature):
    
    sequence = 0
    for i in range (0, number_of_feature):
        sequence += math.pow((input_test_list[i] - Neighbor_from_dataSet_list[i]), 2)
    D = float(math.sqrt(sequence))
    return D

def insertion_sort(my_list):
    for i in range(0, len(my_list)):
        Min = 10000000
        index = 0
        for j in range(i, len(my_list)):
            if(my_list[j]<Min):
                Min = my_list[j]
                index = j
        my_list[i], my_list[index] = my_list[index], my_list[i]
    
    return my_list

# END OF FUNCTION
    
# CREATE DATA SET AND FEATURES LISTS:
sheet = read_excel_files("DataSet4.xlsx")
number_of_feature = sheet.ncols - 1
dataSet = []
tmp_rows_list = []
for i in range(0, sheet.nrows):    
    for j in range(0, number_of_feature + 1):
        tmp_rows_list.append(sheet.cell_value(i, j))
    dataSet.append(tmp_rows_list)
    tmp_rows_list = []
show_dataSet(dataSet, number_of_feature + 1)

Feature_List = []
tmp_cols_list = []
for j in range(0, number_of_feature):
    for i in range(0, len(dataSet)):
        tmp_cols_list.append(dataSet[i][j])
    Feature_List.append(tmp_cols_list)
    tmp_cols_list = []
# END CREATE DATA SET AND FEATURES LISTS:

# Input Test :
input_test = []
k = int(input('Enter K : '))
for i in range(0, number_of_feature):
    str_message = "Enter Value of Feature " + str(i+1) + " : "
    tmp = float(input(str_message))
    input_test.append(tmp)
    

avg_of_features = []
std_of_features = []
for i in range(0, number_of_feature):
    avg_of_features.append(get_avg(Feature_List[i]))
    std_of_features.append(get_std(Feature_List[i], avg_of_features[i]))
    
for i in range(0, len(dataSet)):
    for j in range(0, number_of_feature):
        new_value = (float(dataSet[i][j]) - float(avg_of_features[j]))/ float(std_of_features[j])
        dataSet[i][j] = new_value
    
print("\n[Normalization DataSet]")
show_dataSet(dataSet, number_of_feature + 1)
print("\n\n")


print("[Euclidean Distance Dictionary]")
Distance_dict = {} #include 1/d , label
for i in range(0, len(dataSet)):
    D = cal_Euclidean_Distance(input_test, dataSet[i], number_of_feature)
    label = dataSet[i][number_of_feature]
    Distance_dict.update( {1/D : label} )
    print("Distance : ", 1/D , "---> label : ", label)
Distance_dict_list = sorted(Distance_dict.keys())
print("\n\n[Euclidean Distance Dictionary was sorted]")
print(Distance_dict_list)
print("\n\n")


print("[Selected Euclidean Distance for voting]")
vote_list = []
for i in range(0, k):
    key = Distance_dict_list.pop(len(Distance_dict_list)- 1) # selected_distance (by maximum 1/d)
    label = Distance_dict[key]
    print(str(key) + "\t" + str(label))
    
    vote_list.append(label)


count_class_1 = 0
count_class_2 = 0

for i in range(0, len(vote_list)):
    if(vote_list[i] == 0):
        count_class_1 += 1

    else:
        count_class_2 += 1


print("[Voting Result]")
print("0 : ", (count_class_1/len(vote_list)) * 100 , "%")
print("1 : ", (count_class_2/len(vote_list)) * 100 , "%")







