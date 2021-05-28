def student_helper(student) -> dict:
    return {
        "id": str(student['_id']),
        "fullname": student['fullname'],
        "email": student['email'],
        "course_of_study": student['course_of_study'],
        "year": student['year'],
        "GPA": student['gpa']
    }
def order_helper(order) -> dict:
    return {
        "id": str(order['_id']),
        "pair": order['pair'],
        # "exchange": order['exchange'],
        # "account_name": order['account_name'],
        # "account_type": order['account_type'],
        # "main_account": order['main_account'],
        # "account_balance": order['account_balance'],
        "trade_type": order['trade_type'],
        "auto_scalp":order['auto_scalp'],
        "amount_quantity":order['amount_quantity'],
        "limit_price":order['limit_price'],
        "stop_loss_price":order['stop_loss_price'],
    }

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
    }
