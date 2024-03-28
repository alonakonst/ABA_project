import os
import pandas as pd
import folium
from folium import plugins

# 文件夹路径
folder_path = 'E:/study/master2/advanced ba/project/portugal/sheet'

# 读取文件夹中所有CSV文件
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# 读取并合并数据
df_list = [pd.read_csv(file, parse_dates=['acq_date']) for file in csv_files]
df_combined = pd.concat(df_list, ignore_index=True)

# 确保日期格式正确
df_combined['date'] = pd.to_datetime(df_combined['acq_date'], format='%d/%m/%Y')

# 创建地图对象
map = folium.Map(location=[39.5, -8.0], zoom_start=6)

# 添加图层控制器
layer_control = folium.LayerControl()

for month in range(1, 13):
    # 筛选出该月份的数据
    df_month = df_combined[df_combined['date'].dt.month == month]
    heat_data = [[row['latitude'], row['longitude']] for index, row in df_month.iterrows()]
    
    if heat_data:
        # 创建该月份的热力图图层
        heat_layer = plugins.HeatMap(heat_data, name=f'Month {month}')
        
        # 将热力图图层添加到地图上
        heat_layer.add_to(map)

# 必须在添加所有图层后再添加图层控制器
layer_control.add_to(map)

# 创建保存热力图的文件夹
output_folder_path = 'E:/study/master2/advanced ba/project/portugal/heatmap per month'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 保存地图
file_path = os.path.join(output_folder_path, 'dynamic_portugal_heatmap.html')
map.save(file_path)
