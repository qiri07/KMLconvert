#pip install xml
#pip install mysql-connector-python
import xml.etree.ElementTree as ET
import re
import mysql.connector

# INSERT INTO coordinate , 替换为您的表名 coordinate
kml_file_path = "doc.kml"  # 替换为您的KML文件路径
def insert_intodb(mylist):
    try:
        cursor=None
        # 连接MySQL数据库
        conn = mysql.connector.connect(
            host='111.111.111.111',     # MySQL服务器地址
            user='root', # MySQL用户名
            password='password', # MySQL密码
            database='store', # 要使用的数据库名称
            port=3306
        )
        # 创建游标对象
        cursor = conn.cursor()
        # 示例数据字典
        #record1 = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
        #newlist=[]
        for item in mylist:
            name, lon, lat = item
            if find_kw(name):
                namefirst=name
            if find_num(name):
                name=namefirst+'+'+name+'00'
            dict={'dk': name, 'longitude': lon, 'latitude': lat}
            print(dict)
            #newlist.append(name,lon,lat)
            # 插入数据到数据库
            insert_query = "INSERT INTO coordinate (longitude, latitude, dk) VALUES (%s, %s, %s)"
            values = (lon, lat, name)
            #print(insert_query)
            # 插入第一条记录
            cursor.execute(insert_query, values)

        # 提交更改到数据库
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('except',str(e))       

def find_kw(main_string,substrings=['dk','ck','dik','diik']):
    pattern = re.compile(r'(?i)' + '|'.join(re.escape(substring) for substring in substrings))
    return bool(pattern.search(main_string))

def find_num(text):
    pattern = r'^[0-9]$'
    if re.match(pattern, text):
        return True

def swap_key_value(dictionary):
    return {value: key for key, value in dictionary.items()}

def parse_kml(kml_file):
    # 使用ElementTree解析KML文件
    tree = ET.parse(kml_file)
    root = tree.getroot()
    # 命名空间前缀（如果有的话）
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    # 存储名称和经纬度信息的列表
    data = []
    # 在KML中，标签Placemark表示一个地点
    for placemark in root.findall(".//kml:Placemark", ns):
        # 提取名称信息
        name = placemark.find(".//kml:name", ns).text
        if find_kw(name) or  find_num(name):
            if placemark.find(".//kml:Point", ns):
                # 提取经纬度信息
                coordinates_str = placemark.find(".//kml:coordinates", ns).text
                coordinates = [coord.strip() for coord in coordinates_str.split(",")]

                # KML文件中经度在前，纬度在后，这里将它们交换为（纬度，经度）形式
                latitude = float(coordinates[1])
                longitude = float(coordinates[0])

                # 将名称和经纬度信息存储为元组，并添加到data列表中
                data.append((name,longitude,latitude))
    return data

if __name__ == "__main__":
    #kml_file_path = "doc.kml"  # 替换为您的KML文件路径
    extracted_data = parse_kml(kml_file_path)
    #print(extracted_data)
    insert_intodb(extracted_data)

    # # 创建一个空字典用于存储数据
    # data_dict = {}
    # namefirst=''
    # nameend=''
    # # 将数据存储在字典中
    # for item in extracted_data:
    #     name, longitude, latitude = item
    #     if find_kw(name):
    #         namefirst=name
    #         data_dict[name] = (longitude, latitude)
    #     if find_num(name):
    #         name=namefirst+'+'+name+'00'
    #         data_dict[name] = (longitude, latitude)
    # print('key value in DK : lon,lat')
    # for key, value in data_dict.items():
    #     print(f"{key}: {value}")

    # print('key value in lon,lat : DK ')
    # new_data_dict=swap_key_value(data_dict)
    # for key, value in new_data_dict.items():
    #     print(f"{key}: {value}")