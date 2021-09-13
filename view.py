import eel
import desktop
import datetime
from pos_system import make_master


app_name="html"
end_point="index.html"
size=(700,600)

CSVPATH = "./master.csv"

@ eel.expose
def add_item(item_code,item_count):
    #最初に出力ボックスをクリア
    eel.view_log_clear()
    if master.order == "初期化":
        master.create_instance()
        master.order.return_name_value(item_code,item_count)
        master.order.view_item_list() 
    else:
        master.order.return_name_value(item_code,item_count)
        master.order.view_item_list() 

#おつりの計算
@ eel.expose
def change_calculation(customer_money):
    master.order.change_money(customer_money)

#レシート出力
@ eel.expose
def output_receipt(result):
    master.order.output_receipt(result)


master = make_master()
item_master = master.get_item_csv(CSVPATH)

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)