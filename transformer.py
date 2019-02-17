import os
import sys
from objectmapper import ObjectMapper
from reader import Reader


class Transformer(object):
    def __init__(self, xml_dir, out_dir):
        self.xml_dir = xml_dir
        self.out_dir = out_dir

    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        get_classes = reader.get_classes
        object_mapper = ObjectMapper()
        annotations = object_mapper.bind_files(xml_files)
        self.write_to_txt(annotations, get_classes)

    def write_to_txt(self, annotations, get_classes):
        for annotation in annotations:
            with open(os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename)), "w+") as f:
                f.write(self.to_darknet_format(annotation, get_classes))

    def to_darknet_format(self, annotation, get_classes):
        result = []
        classes = get_classes()
        for obj in annotation.objects:
            if obj.name not in classes:
                # print(f'class "{obj.name}" is missing in classes.txt, want to add it? [Y/n]')
                sys.stdout.write(f'class "{obj.name}" is missing in classes.txt, want to add it? [Y/n] ')    
                if prompt_yes_no() :
                    self.add_class(obj.name)
                else:
                    exit()
            
            classes = get_classes()
            x, y, width, height = self.get_object_params(obj, annotation.size)
            result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))
        return "\n".join(result)

    @staticmethod
    def get_object_params(obj, size):
        image_width = 1.0 * size.width
        image_height = 1.0 * size.height

        box = obj.box
        absolute_x = box.xmin + 0.5 * (box.xmax - box.xmin)
        absolute_y = box.ymin + 0.5 * (box.ymax - box.ymin)

        absolute_width = box.xmax - box.xmin
        absolute_height = box.ymax - box.ymin

        x = absolute_x / image_width
        y = absolute_y / image_height
        width = absolute_width / image_width
        height = absolute_height / image_height

        return x, y, width, height

    @staticmethod
    def darknet_filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre
    
    @staticmethod
    def add_class(newclass):
        with open(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'classes.txt'), "a") as f:
            f.write('\n' + newclass)
    


def prompt_yes_no():
    # raw_input returns the empty string for "enter"
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}

    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")