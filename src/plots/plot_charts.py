
import matplotlib.pyplot as plt
import pandas as pd
from bson import ObjectId

from src.queries.data_queries import get_employees, get_departments, get_performance_reviews, get_training_data


def plot_bar_chart(x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_department_distribution(db):
    employees = get_employees(db, {"department_id":1})
    departments = get_departments(db, {"_id":1,"name":1})
    department_counts = employees['department_id'].value_counts()

    print(department_counts)
    department_names = departments.set_index('_id').loc[department_counts.index]['name']

    plot_bar_chart(department_names, department_counts.values,
                   'Phân bố nhân sự theo phòng ban', 'Phòng ban', 'Số lượng nhân viên')



def plot_age_distribution(db):
    employees = get_employees(db, {"age":1})
    age_counts = employees['age'].value_counts().sort_index()
    plot_bar_chart(age_counts.index, age_counts.values,
                   'Độ tuổi nhân sự', 'Độ tuổi', 'Số lượng nhân viên')


def plot_performance_reviews( db):
    performance_reviews = get_performance_reviews(db, {"employee_id":1,"score":1})
    employees = get_employees(db, {"name":1,"_id":1})
    avg_scores = performance_reviews.groupby("employee_id")["score"].mean().reset_index()

    avg_scores = avg_scores.merge(employees[['name', '_id']], left_on='employee_id', right_on='_id', how='left')

    if avg_scores.empty:
        print("Không có dữ liệu đánh giá hiệu suất.")
        return

    plot_bar_chart(avg_scores['name'], avg_scores['score'],
                   'Đánh giá hiệu suất nhân viên', 'Tên Nhân viên', 'Điểm trung bình')


def plot_training_effectiveness(db):
    employees = db.employees.find({}, {"training_participation": 1, "performance_score": 1})

    # Khởi tạo dữ liệu cho biểu đồ
    training_scores = {}
    training_counts = {}
    training_names = {}

    for employee in employees:
        for training in employee.get("training_participation", []):
            training_id = str(training["training_id"])
            score = training["score"]

            if training_id not in training_counts:
                training_counts[training_id] = 0
            training_counts[training_id] += 1


            if training_id not in training_names:
                training_name = db.training.find_one({"_id": ObjectId(training_id)}, {"name": 1})["name"]
                training_names[training_id] = training_name

            if training_id not in training_scores:
                training_scores[training_id] = []
            training_scores[training_id].append(score)

    avg_scores = {training_id: sum(scores) / len(scores) for training_id, scores in training_scores.items()}

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Biểu đồ cột: số lượng người tham gia
    ax1.bar(training_counts.keys(), training_counts.values(), alpha=0.6, color='b', label="Số lượng người tham gia")
    ax1.set_xlabel('Khóa đào tạo')
    ax1.set_ylabel('Số lượng người tham gia', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    #  điểm trung bình
    ax2 = ax1.twinx()
    ax2.plot(list(avg_scores.keys()), list(avg_scores.values()), color='r', marker='o', label="Điểm trung bình sau đào tạo")
    ax2.set_ylabel('Điểm trung bình', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Thiết lập tên các khóa đào tạo dưới trục x
    ax1.set_xticks(list(training_counts.keys()))
    ax1.set_xticklabels([training_names[training_id] for training_id in training_counts.keys()], rotation=90)

    plt.title('Mức độ tham gia và hiệu quả các chương trình đào tạo')
    plt.tight_layout()
    plt.show()


def plot_employee_tenure(db):
    employees = get_employees(db, {"hire_date":1})
    today = pd.to_datetime("today")
    employees['tenure'] = (today - pd.to_datetime(employees['hire_date'])).dt.days // 365
    tenure_counts = employees['tenure'].value_counts().sort_index()

    plot_bar_chart(tenure_counts.index, tenure_counts.values,
                   'Thâm niên nhân viên', 'Thâm niên (năm)', 'Số lượng nhân viên')

