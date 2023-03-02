import xml.etree.ElementTree as ET
import json

import os


# 将VOC格式的数据集转换为YOLO格式

class Basic:
    def __init__(self, src_path, target_path):
        """
        src_path: 源数据集的保存地址
        target_path: 目标数据集的保存地址
        """
        self.src = src_path
        self.target = target_path

    # 获取源数据集路径
    def get_src_path(self):
        return self.src

    # 获取目标数据路径
    def get_target_path(self):
        return self.target



# VOC数据集转换为YOLO格式
class Voc2Yolo(Basic):
    def __init__(self, src_path, target_path, class_name) -> None:
        """
        src_path: 源数据集的保存地址
        target_path: 目标数据集的保存地址
        class_name: 包含的类别名称
        """
        super(Voc2Yolo, self).__init__(src_path, target_path)
        self.cname = class_name

    def convert(self, size, box):
        dw = 1. / (size[0])
        dh = 1. / (size[1])
        x = (box[0] + box[1]) / 2.0 - 1
        y = (box[2] + box[3]) / 2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return x, y, w, h
    
    def convert_annotation(self, image_id):
        in_file = open(self.src+ "%s.xml" % (image_id[:-4]), encoding="UTF-8")
        out_file = open(self.target + "%s.txt" % (image_id[:-4]), "w")
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in self.cname or int(difficult) == 1:
                continue
            cls_id = self.cname.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = self.convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


    def transfer(self):
        file = os.listdir(self.src)
        for image_id in file:
            self.convert_annotation(image_id)
        return "Finish"
    
# COCO数据集格式转换为YOLO数据集格式
class Coco2Yolo(Basic):
    def __init__(self, src_path, target_path, class_name):
        super(Coco2Yolo, self).__init__(src_path, target_path)
        self.cname = class_name

    # 转换
    def convert(self, size, box):
        dw = 1. / (size[0])
        dh = 1. / (size[1])

        x = box[0] + box[2] / 2.0
        y = box[1] + box[3] / 2.0
        w = box[2]
        h = box[3]

        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh

        return (x, y, w, h)

    # 转换
    def convert_annotation(self, json_file):

        id_map = {}
        data = json.load(open(json_file, "r"))
        # 解析目标类别
        with open(os.path.join(self.target_path, "classes.txt"), "w") as  f:
            for i, category in enumerate(data['categories']):
                f.write(f"{category['name']}\n")
                id_map[category['id']] = i

        # 解析images字段
        for img in data['images']:
            filename = img["file_name"]
            img_width = img['width']
            img_height = img['height']
            img_id = img["id"]
            head, tail = os.path.splitext(filename)
            
            # 构造txt文件
            ana_txt_name = head + ".txt"
            f_txt = open(os.path.join(self.target_path, ana_txt_name), "w")
            for ann in data['annotation']:
                if ann['image_id'] == img_id
                box = convert((img_width, img_height), ann["bbox"])
            f_txt.close()


    def transfer(self):
        file = os.listdir(self.src)
        for jsonfile in file:
            self.convert_annotation(jsonfile)
        return "Finish"






# src_path = "D:/目标检测/数据集/SCTD声呐数据集/VOC2007/Annotations/"
# target_path = "D:/目标检测/数据集/SCTD声呐数据集/VOC2007/YOLO/"
# voc2yolo = Voc2Yolo(src_path=src_path, 
#                     target_path=target_path,
#                     class_name=["aircraft", "human", "ship"])
# print(voc2yolo.transfer())
