import csv
import datetime
import eel

#レシートファイル名作成
dt_now = datetime.datetime.now()
file_name = "./" + dt_now.strftime('%Y-%m-%d-%H-%M-%S') + ".csv"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_code_list=[]
        self.item_name_list=[]
        self.item_price_list=[]
        self.item_count_list = []
        self.item_total_amount_list=[]
        self.item_master=item_master
    
    def add_item_order(self,item_code,item_name,item_value,item_count,total_amount):
        self.item_code_list.append(item_code)
        self.item_name_list.append(item_name)
        self.item_price_list.append(item_value)
        self.item_count_list.append(item_count)
        self.item_total_amount_list.append(total_amount)
    
    def view_item_list(self): 
        for code,name,price,count,total_amount in \
            zip(self.item_code_list,self.item_name_list,self.item_price_list,self.item_count_list,self.item_total_amount_list):
            #結果表示
            print(f"商品コード:{code} 商品名:{name} 価格:{price} 個数:{count} 商品金額{total_amount}")
            eel.view_log_js(f"商品コード:{code} 商品名:{name} 価格:{price} 個数:{count} 商品金額{total_amount}")

        #合計金額と合計個数の計算
        self.result_total_amount = sum(self.item_total_amount_list)
        self.item_count_list = [int(i) for i in self.item_count_list] #int型に変換
        self.result_total_price = sum(self.item_count_list)

        print(f"合計金額は{self.result_total_amount}で、合計個数は{self.result_total_price}です")
        eel.view_log_js(f"合計金額は{self.result_total_amount}で、合計個数は{self.result_total_price}です")

    def return_name_value(self, input_code, input_count):
        for rist in self.item_master:
            if input_code == rist.item_code:
                total_amount = self.total_amount_calculation(rist.price, input_count)
                self.add_item_order(rist.item_code, rist.item_name, rist.price, input_count, total_amount)       
        
    def total_amount_calculation(self, price, input_count):
        total_amount = int(price) * int(input_count)
        return total_amount

    def change_money(self,input_money):    
            result_change_money = int(input_money) - self.result_total_amount
            if result_change_money > 0:
                print(f"おつりは{result_change_money}円です")
                eel.view_log_js(f"おつりは{result_change_money}円です")
            elif result_change_money == 0:
                print("おつりはありません")
                eel.view_log_js("おつりはありません")
            elif result_change_money < 0:
                print("お預かり金額が不足しています")
                eel.view_log_js("お預かり金額が不足しています")
    
    def output_receipt(self,result):
        f = open(file_name, 'a', encoding="utf-8_sig")
        f.write(result)
        f.close()


### マスタークラス
class make_master:
    def __init__(self):
        self.item_code_temp=[]
        self.item_name_temp=[]
        self.item_value_temp=[]
        self.item_master=[]
        self.order = "初期化"
        
    def get_item_csv(self, CSVPATH):
        f = open(CSVPATH, 'r' , encoding="utf-8_sig")
        reader = csv.reader(f)
        for row in reader:
            self.item_code_temp.append(row[0])
            self.item_name_temp.append(row[1])
            self.item_value_temp.append(row[2])
            
        f.close()

        #ヘッダー削除
        del self.item_code_temp[0]
        del self.item_name_temp[0]
        del self.item_value_temp[0]

        #マスターへ登録
        return self.create_master(self.item_code_temp, self.item_name_temp, self.item_value_temp)
        
    def create_master(self, item_code_temp, item_name_temp, item_value_temp):
        for code,name,value in zip(item_code_temp, item_name_temp, item_value_temp):        
            self.item_master.append(Item(code,name,value))
        return self.item_master

    def create_instance(self):
        self.order = Order(self.item_master)
 