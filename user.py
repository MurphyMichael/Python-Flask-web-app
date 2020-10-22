#planning to hash passwords for the users with hashlib 
import hashlib
class User:

    def __init__(self, username, password, firstName, lastName, watchedList):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.watchedList = []

        #set new username
        def setUsername(self, username):
            self.username = username

        #get username
        def getUsername(self, username):
            return self.username

        #set new password
        def setPassword(self, newPassword):
            self.password = newPassword

        '''
        This fucntion will be for a user loggin in to the system.
        We will eventually hash the passwords and when a user inputs
        a password we will hash it and check to see if they are the same
        resulting in a sucessful login.
        '''
        def getPassword(self, password):
            return self.password

        #set first name for the user
        def setFirstName(self, firstName):
            self.firstName = firstName

        #get user first name
        def getFirstName(self, firstName):
            return self.firstName
            
        #set last name for the user
        def setLastName(self, lastName):
            self.lastName = lastName

        #get user last name
        def getLastName(self, lastName):
            return self.lastName
        
        #user appending a new show or movie to their watched list
        def addToWatchedList(self, watchedList):
            self.watchedList.append(watchedList)

        #get the user's watched list
        def getWatchedList(self, watchedList):
            return self.watchedList