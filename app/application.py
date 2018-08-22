from flask import session

class App:
    users = []                        
        
    ## Login method.
    def login(self, username, password):        
        if (username and password):
            for user in self.users:                
                if (user['username'] == username and user['password'] == password):
                    ## store the user id in a session.
                    session['user_id'] = user['id']
                    return True            

        return False

    ## registering a new account.
    def signup(self, first_name, sur_name, username, password, email= None):
        #return first_name + ' ' + sur_name + ' ' + username + ' ' +password + ' ' +email
        if (first_name and sur_name and username and password):
            for user in self.users: 
                if user['username'] == username:
                    return 'user exists'
                    #return 'user exits'
                    
            id = 1
            if len(self.users):
                id = len(self.users)

            dict = {'id': id, 'first_name': first_name, 'sur_name': sur_name, 'username': username,
                'password': password, 'email': email}
            
            self.users.append(dict)

            #return 'added to the users.'
            return 'user added'
        else: 
            return 'empty fields'

    ## List out users.
    def list_users(self):
       return self.users