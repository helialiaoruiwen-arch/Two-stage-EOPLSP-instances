# import pandas as pd
# import numpy as np

# # 1. 读取 CSV 文件
# df = pd.read_csv('initial/d3p3_100scen/entree_1.csv')

# n_scenario = int(df.n_scenario[0])
# J = int(df.J[0])
# T = int(df.Period_T[0])
# columns_to_average = []
# D = {}

# # 2. 指定要合并的列
# for j in range(J):
#     columns_to_average.append(f'D{j,i}' for i in range(n_scenario))
#     for i in range(n_scenario):
#         demand_name = f'D{j,i}'
#         D[j,i+1] = list(df[demand_name][0:T])
#     D[j] = [np.mean([D[j,n][t] for n in range(1,n_scenario+1)]) for t in range(T)]


# for j in range(J):
#     if j == 0:
#         insert_pos = df.columns.get_loc('energy_product') + 1
#     else:
#         insert_pos = df.columns.get_loc(f'D_{j-1}') + 1
#     # 3. 计算平均值并创建新列
#     new_values = pd.Series(np.round(D[j]), index=df.index[:len(D[j])])
#     df.insert(loc=insert_pos, column=f'D_{j}', value=new_values)
#     # df[f'D_{j}'] = pd.Series(D[j], index=df.index[:len(D[j])])

#     # 4. 删除原来的旧列
#     df = df.drop(columns=columns_to_average[j])
    

# df.drop(columns=['Unnamed: 0'], inplace=True)
# # 5. 保存文件
# df.to_csv('result_merged.csv', index=False, encoding='utf-8-sig')


import os
import pandas as pd
import numpy as np

# ==================== 配置区域 ====================
# 1. 统一的源根目录
INPUT_ROOT_FOLDER = 'initial'

# 2. 新生成文件的总输出根目录
OUTPUT_BASE_FOLDER = 'Entries'
# ==================================================

def process_single_csv(file_path, output_path):
    try:
        # 1. 读取 CSV 文件
        df = pd.read_csv(file_path)
        
        # 安全删除 Unnamed 列
        unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
        if unnamed_cols:
            df.drop(columns=unnamed_cols, inplace=True)

        df.drop(columns='energy_offer_price', inplace=True)
        df['energy_purchase_price'] = (df['energy_purchase_price'] / 5).round(2)

        # 提取核心参数
        n_scenario = int(df.n_scenario[0])
        J = int(df.J[0])
        T = int(df.Period_T[0])
        
        all_columns_to_drop = []
        D = {}

        # 2. 计算平均值并记录需要删除的旧列
        for j in range(J):
            # 正确生成当前 j 的所有场景列名
            scen_cols = [f'D{j,i}' for i in range(n_scenario)]
            all_columns_to_drop.extend(scen_cols) 
            
            for i in range(n_scenario):
                demand_name = f'D{j,i}'
                D[j, i+1] = list(df[demand_name].iloc[0:T])
                
            # 计算场景间的平均值
            D[j] = [np.mean([D[j, n][t] for n in range(1, n_scenario + 1)]) for t in range(T)]

        # 3. 按顺序动态插入新列
        for j in range(J):
            if j == 0:
                insert_pos = df.columns.get_loc('energy_product') + 1
            else:
                insert_pos = df.columns.get_loc(f'D_{j-1}') + 1
                
            # 转换为 Series 并对齐 index，防止长度不匹配
            new_values = pd.Series(np.round(D[j]), index=df.index[:len(D[j])])
            df.insert(loc=insert_pos, column=f'D_{j}', value=new_values)

        # 4. 在所有新列插入完毕后，一次性删除旧列
        df.drop(columns=all_columns_to_drop, errors='ignore', inplace=True)
        
        # 5. 保存文件
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"  ✅ 成功处理并保存: {os.path.basename(output_path)}")

    except Exception as e:
        print(f"  ❌ 处理文件 {file_path} 时出错: {e}")


def main():
    # 检查 initial 根目录是否存在
    if not os.path.exists(INPUT_ROOT_FOLDER):
        print(f"❌ 错误：找不到源根目录 '{INPUT_ROOT_FOLDER}'，请检查路径是否正确！")
        return

    # 确保总输出目录存在
    if not os.path.exists(OUTPUT_BASE_FOLDER):
        os.makedirs(OUTPUT_BASE_FOLDER)

    # 动态获取 initial 目录下的所有子内容
    for item in os.listdir(INPUT_ROOT_FOLDER):
        folder_path = os.path.join(INPUT_ROOT_FOLDER, item)
        
        # 过滤：确保处理的只是文件夹（比如 d3p3_100scen 等）
        if os.path.isdir(folder_path):
            print(f"\n📂 正在扫描文件夹: {folder_path}")
            
            # 在输出根目录下创建对应的同名新文件夹
            new_output_folder = os.path.join(OUTPUT_BASE_FOLDER, item)
            if not os.path.exists(new_output_folder):
                os.makedirs(new_output_folder)
                
            # 遍历处理该文件夹下的所有 CSV 文件
            csv_count = 0
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.csv'):
                    input_file_path = os.path.join(folder_path, file_name)
                    output_file_path = os.path.join(new_output_folder, file_name)
                    
                    process_single_csv(input_file_path, output_file_path)
                    csv_count += 1
            
            if csv_count == 0:
                print("  (该文件夹下没有找到任何 CSV 文件)")

if __name__ == '__main__':
    main()