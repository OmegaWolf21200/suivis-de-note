import sqlite3 as sql

class Data:
    def __init__(self,data_path):
        self.conn = sql.connect(data_path)
        
    def request(self,command):
        cur = self.conn.cursor()
        response = cur.execute(command)
        list_response = list(response)
        cur.close()
        self.conn.commit()
        return list(list_response)
    
    def close(self):
        self.conn.close()

class Register:
    def __init__(self, id, id_link, name, cat):
        self.id = id
        self.id_link = id_link
        self.name = name
        self.cat = cat
        
class Rate:
    def __init__(self,id,id_link,name,value,coef,cat):
        self.id = id
        self.id_link = id_link
        self.name = name
        self.value = value
        self.coef = coef
        self.cat = cat
        

class App:
    def __init__(self, data:Data, user_list = None, year_list = None, trimester_list = None, matter_list = None, rate_list =None):
        
        self.data = data
        
        self.user_list = user_list if user_list != None else []
        self.year_list = year_list if year_list != None else []
        self.trimester_list = trimester_list if trimester_list != None else []
        self.matter_list = matter_list if matter_list != None else []
        self.rate_list = rate_list if rate_list != None else []
        
        self.dict_table = {
            "U" : "user",
            "Y" : "year",
            "T" : "trimester",
            "M" : "matter",
            "R" : "rate"
        }
        
        self.all_lists = [self.user_list, self.year_list, self.trimester_list, self.matter_list, self.rate_list]
        
    #---Méthode SQL---
    def get_table(self,table,condition=None):
        return self.data.request(f"SELECT * FROM {table} WHERE {condition}" if condition != None else f"SELECT * FROM {table}")
    
    def add_table(self,objects):
        if objects.cat == "U":
            id = self.data.request(f"INSERT INTO user (name) VALUES ('{objects.name}') RETURNING id;")
        elif objects.cat == "Y":
            id = self.data.request(f"INSERT INTO year (id_user, name) VALUES ('{objects.id_link}', '{objects.name}') RETURNING id;")
        elif objects.cat == "T":
            id = self.data.request(f"INSERT INTO trimester (id_year, name) VALUES ('{objects.id_link}', '{objects.name}') RETURNING id;")
        elif objects.cat == "M":
            id = self.data.request(f"INSERT INTO matter (id_trimester, name) VALUES ('{objects.id_link}', '{objects.name}') RETURNING id;")
        elif objects.cat == "R":
            id = self.data.request(f"INSERT INTO rate (id_matter, name, value, coef) VALUES ('{objects.id_link}', '{objects.name}', '{objects.value}', '{objects.coef}') RETURNING id;")
        
        app.update()
        return id[0][0]
    
    def sup_table(self, objects):
        app.data.request(f"DELETE FROM {app.dict_table[objects.cat]} WHERE id = '{objects.id}'")
        
    
    #---Méthode général---
    def update(self):
        [group.clear for group in self.all_lists]
        for user_data in self.get_table("user"):
            self.user_list.append(Register(user_data[0],None, user_data[1],"U"))
        for year_data in self.get_table("year"):
            self.year_list.append(Register(*(year_data[i] for i in range(3)), "Y"))
        for trimester_data in self.get_table("trimester"):
            self.trimester_list.append(Register(*(trimester_data[i] for i in range(3)), "T"))
        for matter_data in self.get_table("matter"):
            self.matter_list.append(Register(*(matter_data[i] for i in range(3)), "M"))
        for rate_data in self.get_table("rate"):
            self.rate_list.append(Rate(*(rate_data[i] for i in range(5)), "R"))            

db = Data("data.db")

app = App(db)
app.update()

db.close()
    
        

