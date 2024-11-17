import pandas as pd


def get_employees(db, filter):
    employees = pd.DataFrame(list(db.employees.find({}, filter)))
    return employees

def get_performance_reviews(db, filter):

    performance_reviews = pd.DataFrame(list(db.performance_reviews.find({}, filter)))

    return performance_reviews

def get_training_data(db, filter):

    training_data = pd.DataFrame(list(db.training.find({}, filter)))

    return training_data

def get_departments(db, filter):

    departments = pd.DataFrame(list(db.departments.find({}, filter)))

    return departments

