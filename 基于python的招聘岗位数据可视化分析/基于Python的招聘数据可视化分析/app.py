from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# 准备数据
data = pd.read_csv('./data.csv')


# 清洗数据开始
def data_cleaning(df):
    # 清洗数据
    df = df.drop_duplicates()
    wan = 10000
    qian = 1000
    def clear_data(data):
        try:
            if '万/年' in data:
                min_salary, max_salary = data.replace('万/年', '').split('-')
                data_list = [float(min_salary) * wan, float(max_salary) * wan]
            elif ('千' in data) and ('万' in data) and ('薪' in data):
                xin_list = data.replace('万', '').replace(
                    '千', '').replace('薪', '').split('·')
                # 根据多少薪计算平均每月领到工资的比例
                number = float(xin_list[1]) / 12
                min_salary, max_salary = xin_list[0].split('-')
                data_list = [float(min_salary) * qian * number,
                            float(max_salary) * wan * number]
            elif ('千' in data) and ('薪' in data):
                xin_list = data.replace('千', '').replace('薪', '').split('·')
                # 根据多少薪计算平均每月领到工资的比例
                number = float(xin_list[1]) / 12
                min_salary, max_salary = xin_list[0].split('-')
                data_list = [float(min_salary) * qian * number,
                            float(max_salary) * qian * number]
            elif ('万' in data) and ('薪' in data):
                xin_list = data.replace('万', '').replace('薪', '').split('·')
                # 根据多少薪计算平均每月领到工资的比例
                number = float(xin_list[1]) / 12
                min_salary, max_salary = xin_list[0].split('-')
                data_list = [float(min_salary) * wan * number,
                            float(max_salary) * wan * number]
            elif ('千' in data) and ('万' in data):
                min_salary, max_salary = data.replace(
                    '万', '').replace('千', '').split('-')
                data_list = [float(min_salary) * qian, float(max_salary) * wan]
            elif '元/天' in data:
                salary = data.replace('元/天', '')
                data_list = [float(salary) * 30, float(salary) * 30]
            elif '千/天' in data:
                salary = data.replace('千/天', '')
                data_list = [float(salary) * 30 * qian, float(salary) * 30 * qian]
            elif '万' in data:
                min_salary, max_salary = data.replace('万', '').split('-')
                data_list = [float(min_salary) * wan, float(max_salary) * wan]
            elif '千' in data:
                min_salary, max_salary = data.replace('千', '').split('-')
                data_list = [float(min_salary) * qian, float(max_salary) * qian]
        except Exception as e:
            print(data)
            data_list = [3000, 4000]
        return data_list

    # 提取城市名


    def get_cityString(data):
        try:
            data = eval(data)
            return data['cityString']
        except Exception as e:
            print(data)


    # 提取城市名
    df['cityString'] = df.jobAreaLevelDetail.apply(get_cityString)
    # 清洗工资数据
    provideSalary = df.provideSalaryString.apply(clear_data)
    # 最低工资
    df['min_salary'] = [int(i[0]) for i in provideSalary]
    # 最高工资
    df['max_salary'] = [int(i[1]) for i in provideSalary]
    # 平均工资
    df['mean_salary'] = [round((int(i[0])+int(i[1]))/2, 2) for i in provideSalary]
    return df
# 清洗数据结束


# 数据分析与处理开始
def all_data(df):
    all_data = {}
    # 岗位平均薪资情况
    # 按岗位名分类求平均
    job_map_data = df.groupby('jobName')['min_salary', 'max_salary'].mean().round(
        2).reset_index().values
    # 岗位名数组
    all_data['job_salary_name'] = job_map_data[:, 0].tolist()
    # 岗位最低工资数组
    all_data['job_min_salary'] = job_map_data[:, 1].tolist()
    # 岗位最高工资数组
    all_data['job_max_salary'] = job_map_data[:, 2].tolist()


    # 根据城市名分组，计算平均工资
    city_map_data = df.groupby('cityString')[
        'mean_salary'].mean().round(2).reset_index().values
    # 提取城市名数组
    all_data['city_name'] = city_map_data[:, 0].tolist()
    # 提取城市平均工资数组
    all_data['city_values'] = city_map_data[:, 1].tolist()


    # 热门岗位
    job_value_counts = df.jobName.value_counts()
    all_data['job_name'] = job_value_counts.index.to_list()[:10][::-1]
    all_data['job_values'] = job_value_counts.to_list()[:10][::-1]
    

    # 学历占比
    all_data['degree_dict'] = [{'value': v, 'name': n} for v, n in zip(
        df.degreeString.value_counts(), df.degreeString.value_counts().index)]
    # 工作经验占比
    all_data['work_year_dict'] = [{'value': v, 'name': n} for v, n in zip(
        df.workYearString.value_counts(), df.workYearString.value_counts().index)]
    # 公司类型占比
    all_data['company_type_dict'] = [{'value': v, 'name': n} for v, n in zip(
        df.companyTypeString.value_counts(), df.companyTypeString.value_counts().index)]

    # 左侧三个数据
    # 岗位数量
    all_data['job_count'] = str(len(df))
    # 城市数量
    all_data['city_count'] = str(len(city_map_data))
    # 公司数量
    all_data['company_count'] = str(len(df.companyName.value_counts()))
    
    return all_data

# 定义路由和视图函数
@app.route('/')
def index():
    # 调用函数获取数据
    df = data_cleaning(data)
    table_data = all_data(df)
    # print(table_data)
    # 渲染模板并传递数据
    return render_template('index.html', table_data=table_data)


if __name__ == '__main__':
    app.run(debug=True)
    # index()