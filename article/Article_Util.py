import os


class Article_Util(object):
    def __init__(self):
        self.dir = ""
        print("init ...")

    # 获取其他目录标题
    @staticmethod
    def get_other_list(path=None, list_name=None):

        other_list = []
        files = os.listdir(path)
        for file in files:
            if file.find("目录") > 0 and file != list_name:
                # print(file)
                for f_file in open(os.path.join(path, list_name), "r"):
                    # print(i.strip())
                    other_list.append(f_file.split(",")[0])
        return other_list


    # 获取本目录标题_作者
    @staticmethod
    def get_list(path=None, list_name=None):
        files_m = []
        for f_file in open(os.path.join(path, list_name), "r"):
            # print(i.strip())
            files_m.append(f_file.split(",")[0])
        return files_m


if __name__ == '__main__':
    c = common()
    c.get_other_list(path=r"D:\文档", list_name="维普网目录.txt")

