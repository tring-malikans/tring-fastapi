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
        "coin": order['coin'],
        "pair": order['pair'],
        "exchange": order['exchange'],
        "trade_type": order['trade_type'],
        "account_balance": order['account_balance'],
        "main_account": order['main_account'],
        "account_type": order['account_type'],
        "account_name": order['account_name'],
        "up_percentage": order['up_percentage'],
        "down_percentage": order['down_percentage'],
        "loss_sell_percentage": order['loss_sell_percentage'],
        "threshold_percentage": order['threshold_percentage'],
        "buy_quantity": order['buy_quantity'],
        "amount_quantity": order['amount_quantity'],
        "first_amount": order['first_amount'],
        "first_quantity": order['first_quantity'],
        
        # "entry_time": order['entry_time'],
        # "exit_time": order['exit_time'],
        # "duration": order['duration'],
        # "in_amount": order['in_amount'],
        # "in_amount_pair": order['in_amount_pair'],
        # "in_quantity": order['in_quantity'],
        # "in_quantity_pair": order['in_quantity_pair'],
        # "out_amount": order['out_amount'],
        # "out_amount_pair": order['out_amount_pair'],
        # "out_quantity": order['out_quantity'],
        # "out_quantity_pair": order['out_quantity_pair'],
        # "entry_price": order['entry_price'],
        # "entry_price_pair": order['entry_price_pair'],
        # "exit_price": order['exit_price'],
        # "exit_price_pair": order['exit_price_pair'],
        # "fees_amount": order['fees_amount'],
        # "fees_amount_pair": order['fees_amount_pair'],
        # "fees_percentage": order['fees_percentage'],
        # "profit_loss": order['profit_loss'],
        # "profit_loss_amount": order['profit_loss_amount'],
        # "profit_loss_pair": order['profit_loss_pair'],
        # "profit_loss_percentage": order['profit_loss_percentage'],
        "trade_status": order['trade_status'],
        "auto_trail": order['auto_trail'],

        "lowest_price": order['lowest_price'],
        "target_buy_price": order['target_buy_price'],
        "highest_price": order['highest_price'],
        "target_sell_price": order['target_sell_price'],
        "loss_sell_price": order['loss_sell_price'],
        "threshold_price": order['threshold_price'],
        "threshold_status":order['threshold_status'],
        "buy_price": order['buy_price'],
        "buy_order_filled": order['buy_order_filled']
    }

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
        "password": admin['password'],
        # "fav_coins":admin['fav_coins']
    }


def coin_helper(coin) -> dict:
    return {
        "id": str(coin['_id']),
        "pair": coin['pair'],
        "coin": coin['coin'],
    }


def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "accountname": user['accountname'],
        "email": user['email'],
        "coin": user['coin'],
        "pair": user['pair'],
        "api_key": user['api_key'],
        "secret_key": user['secret_key'],
        "price": user['price'],
        "status": user['status']
    }