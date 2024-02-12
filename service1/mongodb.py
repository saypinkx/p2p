# import pymongo
# client = pymongo.MongoClient('mongodb+srv://sixzerx:31rasune@clustert0.oflwmxk.mongodb.net/?retryWrites=true&w=majority')
# db = client.testdb
# collection = db.new_collection
# collection.insert_one({"_id": 1, 'name': 'Alex'})
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.testdb
collection = db.new_collection
# collection.insert_one({'_id': 1, 'name': 2})

# INSERT VALUE

# 1 добавляет один документ
# collection.insert_one({'_id': 'test_id2', 'name':'test_name'})

# 2 добавляет несколько документов
# data = [
#     {
#         "_id": 3,
#         'name': 'test3'
#     },
#     {
#         '_id': 4,
#         'family': 'test4'
#     }
# ]
# collection.insert_many(data)


# SELECT VALUE

# 1 вывод всех документов
# for value in collection.find():
#     print(value)

# 2 вывод конкретного

# query = {'name': 2}
# for value in collection.find(query):
#     print(value)

# 3 вывод конкретных значений 1 - показывает 0 - не показываем

# query = {'name': 2}
# for value in collection.find(query, {"_id": 0, 'name': 1}):
#     print(value)
# 0 - только для id, для остальных вызовет ошибку

# 4 получения документа с помощью первой буквы (если код символа больше чем а, то подходит)

# query = {'name': {"$gt": "a"}}
# for value in collection.find(query, {"_id": 0, 'name': 1}):
#     print(value)


# 5  получения документа с помощью регулярного выражения

# query = {'name': {"$regex": "test*"}}
# for value in collection.find(query):
#     print(value)

# 6 получение первого документа в бд

# res = collection.find_one()
# print(res)

# 7 поиск первого документа по конкретному значению

# res = collection.find_one({"name": 2})
# print(res)

# 8 ограничение количества выведенных документов

# for value in collection.find().limit(1):
#     print(value)

# 9 сортировка документов по значению -1 - убывание 1- возрастание

# for value in  collection.find().sort('name', 1):
#     print(value)

# 10 количество всех документов в коллекции

# res = collection.count_documents({})
# print(res)

# 11 количество документов с нужным значением

# res = collection.count_documents({'name': 2})
# print(res)

# 12 получение баз данных, коллекций

# res = client.list_database_names()
# res2 = db.list_collection_names()
# print(res)
# print(res2)


# UPDATE VALUE

# 1 обновление одного документа

# current = {"name": 'test3'}
# new_data = {"$set": {"name": "new"}}
# collection.update_one(current, new_data)

# 2  обновление нескольких с помощью регулярных выражений

# current = {"name": {'$regex': "test*"}}
# new_data = {"$set": {"name": "UPDATE"}}
# collection.update_many(current, new_data)

# 3 использование инкримента

# collection.update_one({'_id': 1}, {'$inc': {'balance': -211}})

# 4  удаление из массива ( с конца 1, с начала -1 )

# collection.update_one({'_id': 1}, {'$pop': {'arrage': -1}})

# 5 добавление  в массив

# collection.update_one({'_id': 1}, {'$push': {'arrage': 1}})


# DELETE VALUE

# 1 удаление одного значения

# collection.delete_one({'_id': 1})

# 2 удаление нескольких значений, вывод колисчества удаленных значений, удаление всех документов

# res = collection.delete_many({'_id': {'$regex': 'test*'}})
# print(res.deleted_count)
# collection.delete_many({})

# CОЗДАНИЕ, УДАЛЕНИЕ, ВЫВОД ИНДЕКСОВ
#
# collection.create_index([("name", pymongo.DESCENDING)], unique=True)
# collection.drop_index("name_-1")
# print(collection.index_information())
