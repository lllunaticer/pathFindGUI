# -*- coding: utf-8 -*-
import tkinter as tk
import re
from PIL import ImageTk, Image
import tkinter.font as tkFont

import Dijkstras as dj
import Floyd as fd
import Draw as dr

# 实例化object，建立窗口window
window = tk.Tk()

# 给窗口的可视化起名字
window.title('路由选择程序Version 0.0 @Author 龙行健')

#设定窗口的大小(长 * 宽)
window.geometry('1000x800')  # 这里的乘是小x

# 设置背景图片
canvas = tk.Canvas(window, width=2000,height=1600,bd=0, highlightthickness=0)
imgpath = 'bg.gif'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)

canvas.create_image(500,400,image=photo)
canvas.place(x=0,y=0)

# 基准坐标点
base_point_x = 210
base_point_y = 50


# 输入网络中节点的个数
tk.Label(window, text='请输入网络中节点个数').place(x=base_point_x, y=20)
point_number_entry = tk.Entry(window)
point_number_entry.place(x=base_point_x + 130, y=20)
points = point_number_entry.get()

# 多行文本输入框，输入网络无向图（带权边集数组）
input_prop = tk.Label(window,bg='green', width=80,height = 3,text='请在下面输入网络中的边及其权重（带权边集数组），输入格式为[(a1,b1,w1),(a2,b2,w2)...(ax,bx,wx)],\n(a1,b1,w1)表示节点a1和节点b1之间有连接且连接延迟为w1')
input_prop.place(x=base_point_x,y =base_point_y )
graph_input = tk.Text(window, height=4, width=80)
graph_input.place(x=base_point_x, y=base_point_y+60)
# 用以下方法获取text框内容
graph = graph_input.get("0.0", "end")
# print(graph)

# 输入信息再提示，以及程序信息等
input_view = tk.Text(window, height=15, width=80)
input_view.place(x=base_point_x, y=base_point_y + 500)
input_view.insert(tk.END,'下面是您的输入信息，请仔细检查您，以确保您的输入节点数目、网络信息、路由的起点终点等正确:')
ft1 = tkFont.Font(size=19, slant=tkFont.ITALIC)
information = tk.Label(window,text='路由路径选择程序Version 0.0 @author 龙行健',font = ft1)
information.place(x=base_point_x+8,y=base_point_y+710)



# 输入路由起点
tk.Label(window, text='请输入路由起点').place(x=base_point_x, y=base_point_y + 130)  # 将`User name:`放置在坐标（10,10）。
start_point_entry = tk.Entry(window)  # 创建一个注册名的`entry`，变量为`new_name`
start_point_entry.place(x=base_point_x + 100, y=base_point_y + 130)  # `entry`放置在坐标（150,10）.
start = start_point_entry.get()

# 输入路由终点
tk.Label(window, text='请输入路由终点').place(x=base_point_x + 320, y=base_point_y + 130)  # 将`User name:`放置在坐标（10,10）。
end_point_entry = tk.Entry(window)  # 创建一个注册名的`entry`，变量为`new_name`
end_point_entry.place(x=base_point_x + 420, y=base_point_y + 130)  # `entry`放置在坐标（150,10）.
end = end_point_entry.get()
# 第4步，在图形界面上设定标签

# 算法选择框
var_algorithm_selection = tk.StringVar()
label_select_algorithm = tk.Label(window, bg='yellow', width=40, text="路由算法选择")
label_select_algorithm.place(x=base_point_x+150, y=base_point_y + 170)
algorithm_flag = 'Dijkstras Algorithm'

# 选择框handler函数
def selection():
    global algorithm_flag
    label_select_algorithm.config(text='你选择了' + var_algorithm_selection.get() + '进行计算',bg='red')
    algorithm_flag = var_algorithm_selection.get()

#     根据value选取对应的算法执行  var_algorithm_selection.get() 获取value
r1 = tk.Radiobutton(window, text='Floyd Algorithm', variable=var_algorithm_selection, value='Floyd Algorithm',
                    command=selection).place(x=base_point_x, y=base_point_y + 210)
r2 = tk.Radiobutton(window, text='Dijkstras Algorithm', variable=var_algorithm_selection, value='Dijkstras Algorithm',
                    command=selection).place(x=base_point_x + 420, y=base_point_y + 210)

# 结果显示label
tk.Label(window, bg='yellow', width=20, text="最优路径为:").place(x=base_point_x, y=base_point_y + 280)
var_path = tk.StringVar()
l = tk.Label(window, textvariable=var_path, bg='white', fg='black', font=('Arial', 12), width=62, height=2).place(
    x=base_point_x, y=base_point_y + 310)
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

tk.Label(window, bg='yellow', width=20, text="最短距离为:").place(x=base_point_x, y=base_point_y + 370)
var_distance = tk.StringVar()  # 将label标签的内容设置为字符类型，用var_path来接收hit_me函数的传出内容用以显示在标签上
l = tk.Label(window, textvariable=var_distance, bg='white', fg='black', font=('Arial', 12), width=62, height=2).place(
    x=base_point_x, y=base_point_y + 400)

on_hit_calculate = False
graph_list = []
path = []

# 计算按钮handler函数
def calculate():
    global on_hit_calculate
    global graph_list
    global path

    if on_hit_calculate == False:
        on_hit_calculate = True
        graph_content = graph_input.get("0.0", "end")#获取边集数组内容

        # 用正则将用户输入的字符串形式的边集数组转换为list
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
        ps = re.findall(p1, graph_content)
        for str in ps:
            l_tmp = []
            s_tmp = str.split(',')
            for s in s_tmp:
                l_tmp.append(int(s))
            graph_list.append(l_tmp)

        # 其他参数
        point_number = point_number_entry.get()
        start_point = start_point_entry.get()
        end_point = end_point_entry.get()

        # 获取的graph_list等参数作为参数传递给不同的算法
        if algorithm_flag == 'Dijkstras Algorithm':
            res = dj.Dijkstras(int(point_number), graph_list, int(start_point), int(end_point))
        else:
            res = fd.Floyd(int(point_number), graph_list, int(start_point), int(end_point))
        path = res[0]
        distance = res[1]
        # 结果显示
        var_path.set(path)
        var_distance.set(distance)
        str = '\n\n' + '节点数目为：' + point_number + '\n' + '网络带权边集数组为：' +'\n'+ graph_content + '路由起点为：' + start_point + '\n' + '路由终点为：' + end_point
        input_view.insert(tk.END, str)


    else:
        on_hit_calculate = False
        var_path.set('')


# 放置计算按钮
calculate_button = tk.Button(window, text='执行计算', font=('Arial', 12), width=10, height=1, command=calculate).place(
    x=base_point_x + 230, y=base_point_y + 240)
# 第5步，放置标签

on_hit_draw = False


def draw_network():
    global on_hit_draw
    if on_hit_draw == False:
        on_hit_draw = True
        dr.draw(graph_list, path)
    else:
        on_hit_draw = False
        var_distance.set('')


draw_button = tk.Button(window, text='显示网格', font=('Arial', 12), width=10, height=1, command=draw_network).place(
    x=base_point_x + 230, y=base_point_y + 455)
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。
