import pandas as pd
from datetime import datetime, timedelta

# 初始化变量
loan_principal = 640000  # 初始贷款本金
monthly_principal = 2222  # 每月固定还款本金
monthly_interest_rate = 0.0315 / 12  # 月利率
annual_extra_payment = 40000  # 每年1月1日的额外还款金额
month = 0
month_data = []  # 用于存储每月还款明细

# 设置初始日期
start_date = datetime(2025, 1, 20)  # 还款开始日期，每月20日
annual_prepayment_year = 2025  # 第一年提前还款年份
repayment_date = start_date  # 当前还款日期

# 记录每个月的还款明细
def record_monthly_payments():
    global loan_principal, month, annual_prepayment_year, repayment_date  # 声明为全局变量

    while loan_principal > 0:
        # 检查是否到达下一年的1月1日，进行提前还款
        if repayment_date.month == 1:
            # 计算提前还款前的未来利息
            future_interest_before = calculate_future_interest(loan_principal)

            # 在本年度的开始插入提前还款数据
            month_data.insert(len(month_data) - (12 - month), [month, loan_principal, annual_extra_payment, 0, annual_extra_payment, f"{annual_prepayment_year}-01-01"])
            # 执行提前还款
            loan_principal -= annual_extra_payment
            annual_prepayment_year += 1  # 更新到下一年

            # 计算提前还款后的未来利息
            future_interest_after = calculate_future_interest(loan_principal)

            # 计算节省的利息
            interest_saved = future_interest_before - future_interest_after
            month_data[-1].append(interest_saved)  # 将节省的利息添加到数据中

        # 每月还款前记录
        month += 1
        interest_payment = loan_principal * monthly_interest_rate  # 每月利息
        total_payment = monthly_principal + interest_payment  # 每月总还款额

        month_data.append([month, loan_principal, monthly_principal, interest_payment, total_payment, repayment_date.strftime('%Y-%m-%d')])

        # 更新本金和剩余贷款
        loan_principal -= monthly_principal

        # 停止条件：本金还清
        if loan_principal <= 0:
            break

        # 更新还款日期
        repayment_date += timedelta(days=30)  # 每月加30天

# 计算未来还款期内的总利息
def calculate_future_interest(principal):
    total_interest = 0
    remaining_months = (295 - (month % 12))  # 计算剩余还款期数
    for _ in range(remaining_months):
        interest = principal * monthly_interest_rate
        total_interest += interest
        principal -= monthly_principal  # 每月还款固定本金
        if principal <= 0:
            break
    return total_interest

# 主函数，执行逻辑并生成 CSV
def main():
    # 调用函数记录还款明细
    record_monthly_payments()

    # 转换为DataFrame
    columns = ['Month', 'Remaining Principal', 'Principal Payment', 'Interest Payment', 'Total Payment', 'Date', 'Interest Saved']
    df = pd.DataFrame(month_data, columns=columns)

    # 格式化数据，只保留一位小数
    df = df.round(1)

    # 导出为CSV文件
    df.to_csv('loan_repayment_details_with_interest_saved.csv', index=False)
    print("CSV 文件 'loan_repayment_details_with_interest_saved.csv' 已生成")

# 判断是否作为脚本运行
if __name__ == "__main__":
    main()
