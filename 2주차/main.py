import os
import csv

uri = os.path.dirname(__file__) + '/'

# csv 파일 읽어오고 list로 리턴하는 함수
def read_csv(file_name):
    with open(uri + file_name, 'r') as c:
        csv_data = csv.reader(c)
        
        return list(csv_data)

# 특정 행으로 정렬해주는 함수
def sort_matrix(matrix, index, reverse=False):
    return [matrix[0], 
                *sorted(matrix[1:], key=lambda x: x[index], reverse=reverse)]

# 인화성이 0.7 이상인 값만 필터링해서 리턴하는 함수
def filter_high_flammability(matrix, identifier, threshold):
    identifier_index = matrix[0].index(identifier)
    
    return [matrix[0], 
                *filter(lambda x: float(x[identifier_index])>=threshold, matrix[1:])]

if __name__ == '__main__':
    csv_list = read_csv('Mars_Base_Inventory_List.csv')

    print('############csv 데이터############')
    for c in csv_list:
        print(c)

    sorted_csv_list = sort_matrix(csv_list, 4, True)

    filterd_csv_list = filter_high_flammability(csv_list, 'Flammability', 0.7)

    print('############0.7 이상 Flammability############')
    for f in filterd_csv_list:
        print(f)

    with open(uri + 'Mars_Base_Inventory_danger.csv', 'w', newline='') as f:
        write = csv.writer(f)

        write.writerows(filterd_csv_list)

