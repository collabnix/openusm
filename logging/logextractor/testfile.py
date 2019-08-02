# bulk_data = [] 
# for row in csv_file_object:
#     data_dict = {}
#     for i in range(len(row)):
#         data_dict[header[i]] = row[i]
#     op_dict = {
#         "index": {
#             "_index": INDEX_NAME, 
#             "_type": TYPE_NAME, 
#             "_id": data_dict[ID_FIELD]
#         }
#     }
#     bulk_data.append(op_dict)
#     bulk_data.append(data_dict)

x = 10
y= 20

def a():
    print(x)
    x = x + 10

def b():
    print(y)

print(a(),b(),x)