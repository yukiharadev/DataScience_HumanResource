# Các hàm tiện ích giúp xử lý dữ liệu
def format_date(date_str):
    """Chuyển đổi định dạng ngày tháng (YYYY-MM-DD) thành thâm niên tính từ năm hiện tại."""
    return 2024 - int(date_str.split('-')[0])
