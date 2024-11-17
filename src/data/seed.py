import pymongo
import random
from faker import Faker
from bson.objectid import ObjectId
from datetime import datetime, date

from src.configs.index import MONGO_URI, DB_NAME

# Kết nối đến MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

fake = Faker()

departments = ['Phòng Kỹ thuật', 'Phòng Marketing', 'Phòng Kinh doanh', 'Phòng Nhân sự', 'Phòng Tài chính', 'Phòng IT']
department_data = [{"name": dept, "employee_count": 0} for dept in departments]

collections_to_drop = ['departments', 'employees', 'performance_reviews', 'training']
for collection in collections_to_drop:
    if collection in db.list_collection_names():
        db.drop_collection(collection)

db.create_collection("departments")
db.departments.insert_many(department_data)

def convert_to_datetime(date_obj):
    if isinstance(date_obj, (datetime, date)):
        return datetime.combine(date_obj, datetime.min.time())
    return date_obj

training_data = []
for _ in range(20):
    training_id = ObjectId()
    training_data.append({
        "_id": training_id,
        "name": fake.text(max_nb_chars=5),
        "date": convert_to_datetime(fake.date_this_year()),
    })


db.create_collection("training")
db.training.insert_many(training_data)


training_ids = {training["name"]: training["_id"] for training in db.training.find()}


def generate_employee_data(num_records):
    employee_data = []
    for _ in range(num_records):
        department = random.choice(departments)
        age = random.randint(22, 60)
        hire_date = convert_to_datetime(fake.date_this_century(before_today=True))

        performance_score = round(random.uniform(6, 10), 1)
        training_participation = [
            {
                "training_id": training_ids[random.choice(list(training_ids.keys()))],
                "date": convert_to_datetime(fake.date_this_year()),
                "score": random.randint(3, 10)
            }
            for _ in range(random.randint(1, 20))
        ]

        employee_data.append({
            "name": fake.name(),
            "age": age,
            "department_id": db.departments.find_one({"name": department})["_id"],
            "hire_date": hire_date,
            "performance_score": performance_score,
            "training_participation": training_participation
        })

    return employee_data

db.create_collection("employees")
employee_data = generate_employee_data(50)
db.employees.insert_many(employee_data)

department_ids = {dept["name"]: dept["_id"] for dept in db.departments.find()}
for dept_name, dept_id in department_ids.items():
    employee_count = db.employees.count_documents({"department_id": dept_id})
    db.departments.update_one({"name": dept_name}, {"$set": {"employee_count": employee_count}})


def generate_performance_reviews(num_records_per_employee):
    review_data = []
    employee_ids = [employee["_id"] for employee in db.employees.find({}, {"_id": 1})]

    for employee_id in employee_ids:
        num_reviews = random.randint(1, num_records_per_employee)
        for _ in range(num_reviews):
            score = random.randint(0, 10)
            review_data.append({
                "employee_id": employee_id,
                "review_date": convert_to_datetime(fake.date_this_year()),
                "score": score,
                "comments": fake.text(max_nb_chars=100)
            })

    return review_data


db.create_collection("performance_reviews")
performance_review_data = generate_performance_reviews(400)
db.performance_reviews.insert_many(performance_review_data)

print("Completed !")
