import sqlite3
from data import config

class DataBase:
    
    
    
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()



    def user_exists(self,chat_id,gender):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE (chat_id,gender) = (?,?)",(chat_id,gender)).fetchmany(1)
            return bool(len(result))



    def select_users_count(self):
        self.cursor.execute('SELECT COUNT(chat_id) FROM users')
        result = self.cursor.fetchone()
        return result[0] if result else 0



    # def add_user(self, user_id):
    #     with self.connection:
    #         return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)",(user_id,))



    def set_gender(self,chat_id,gender):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM 'users' WHERE chat_id = (?)",(chat_id,)).fetchmany(1)
            if bool(len(user)) == False:
                self.cursor.execute("INSERT INTO 'users' ('chat_id','gender') VALUES (?,?)",(chat_id,gender,))
                return True
            else:
                return False
            
            
            
    def users_count(self,active):
        with self.connection:
            return self.cursor.execute("SELECT COUNT('id') as count FROM 'users' WHERE active = (?)",(active,)).fetchone()[0]    
     
     
     
    def male_count(self,gender):
        with self.connection:
            return self.cursor.execute("SELECT COUNT('id') as count FROM 'users' WHERE gender = (?)",(gender,)).fetchone()[0]
        
        
        
    def female_count(self,gender):
        with self.connection:
            return self.cursor.execute("SELECT COUNT('id') as count FROM 'users' WHERE gender = (?)",(gender,)).fetchone()[0]   
        
        
        
    def gender_update(self,chat_id,gender):
        self.cursor.execute("UPDATE Users SET gender = (?) WHERE chat_id = (?)",(gender,chat_id))
        self.connection.commit()
            
            
            
    def get_gender(self,chat_id):
        with self.connection:
            self.cursor.execute("SELECT gender FROM users WHERE chat_id = ?", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
            
            
            
    def get_age(self,chat_id):
        with self.connection:
            self.cursor.execute("SELECT yosh FROM users WHERE chat_id = ?", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
            


    def get_region(self,chat_id):
        with self.connection:
            self.cursor.execute("SELECT region FROM users WHERE chat_id = ?", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None


            
    def set_gen(self, chat_id, gender):
        self.cursor.execute('UPDATE users SET gender = ? WHERE chat_id = ?', (gender, chat_id))
        self.connection.commit()
        
        
        
    def set_active(self,user_id,active):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET active = (?) WHERE chat_id = (?)",(active,user_id,))
            
            
            
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT chat_id, active FROM 'users' ").fetchall()



    def get_gender_chat(self,gender):
        with self.connection:
            chat =  self.cursor.execute("SELECT * FROM `queue` WHERE gender = (?)",(gender,)).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    user_info = row[1],row[2]
                    return user_info
            else:
                return [0]



    def add_queue(self,chat_id,gender):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` ('chat_id','gender') VALUES (?,?)",(chat_id,gender,))



    def delate_chats(self,id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE id = (?)",(id_chat,))
            
            

    def delete_queue(self,chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE chat_id = (?)",(chat_id,))



    def get_chats(self):
        with self.connection:
            chat =  self.cursor.execute("SELECT * FROM `queue`",()).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    user_info = row[1],row[2]
                    return user_info
            else:
                return [0]
    
    
    
    def create_chat(self,chat_one,chat_two):
        with self.connection:
            if chat_two != 0:
                self.cursor.execute("DELETE FROM `queue` WHERE chat_id = (?)",(chat_two,))
                self.cursor.execute("INSERT INTO `chats` ('chat_one','chat_two') VALUES (?,?)",(chat_one,chat_two,))
                return True
            else:
                return False

    
    
    def get_active_chat(self,chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE chat_one = (?)",(chat_id,))
            id_chat = 0

            for row in chat:
                id_chat = row[0]
                chat_info = [row[0],row[2]]

            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE chat_two = (?)",(chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0],row[1]]

                    if id_chat == 0:
                        return False
                    else:
                        return chat_info
            else:
                return chat_info



    def get_all_chat_ids(self):
        self.cursor.execute('SELECT chat_id FROM users')
        result = self.cursor.fetchall()
        return [row[0] for row in result]



    def get_balance(self, chat_id):
        self.cursor.execute('SELECT balance FROM users WHERE chat_id = ?', (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None



    def add_balance_demo(self, chat_id, balance):
        current_balance = self.get_balance(chat_id)
        updated_balance = current_balance + balance  # balance'ni int ga o'zgartirish
        self.cursor.execute('UPDATE users SET balance = ? WHERE chat_id = ?', (updated_balance, chat_id))
        self.connection.commit()



    def update_age(self, chat_id, age):
        current_age = self.get_age(chat_id)
        if current_age is not None:
            updated_age = current_age - current_age  # ageni int ga o'zgartirish
            self.cursor.execute('UPDATE users SET yosh = ? WHERE chat_id = ?', (age, chat_id))
        else:
            self.cursor.execute('INSERT INTO users (chat_id, yosh) VALUES (?, ?)', (chat_id, int(age)))
        self.connection.commit()



    def add_balance(self, chat_id, balance):
        current_balance = self.get_balance(chat_id)
        if current_balance is not None:
            updated_balance = current_balance + balance  # balance'ni int ga o'zgartirish
            self.cursor.execute('UPDATE users SET balance = ? WHERE chat_id = ?', (updated_balance, chat_id))
        else:
            self.cursor.execute('INSERT INTO users (chat_id, balance) VALUES (?, ?)', (chat_id, int(balance)))
        self.connection.commit()



    def rm_balance(self, chat_id, amount):
        current_balance = self.get_balance(chat_id)
        if current_balance is not None and current_balance >= amount:
            updated_balance = current_balance - amount
            self.cursor.execute('UPDATE users SET balance = ? WHERE chat_id = ?', (updated_balance, chat_id))
            self.connection.commit()
            return True  # Yechildi
        else:
            return False  # Yechilmadi yoki yetarli mablag' yo'q



    def update_custom_balance(self):
        all_chat_ids = self.get_all_chat_ids()
        for chat_id in all_chat_ids:
            current_balance = self.get_balance(chat_id)
            if current_balance is not None and current_balance < config.DAILY_LIMIT:
                self.add_balance(chat_id, config.DAILY_LIMIT)



    def select_all(self, database="database.db", jadval="chat_id", table="users"):
        conn = sqlite3.connect(database)
        try:
            cursor = conn.cursor()
            cursor.execute(f'SELECT {jadval} FROM {table}')
            selected = cursor.fetchall()
            result_list = [item[0] for item in selected]
            return result_list
        except sqlite3.Error as e:
            return f"Sqlite3 xatosi: {e}"
        finally:
            conn.close()
   
    
    
    def execute(query, values=None, db_name="database.db"):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
    
    
    
    
    
def execute(query, values=None, db_name="database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()
    
    