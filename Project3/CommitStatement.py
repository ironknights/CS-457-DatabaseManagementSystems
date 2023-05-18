
# Author : Deeptanshu Das
# Date : November 12, 2019

from Query import Query 


class CommitStatement(Query):

    def __init__(self):
        pass 

    def execute(self): 

        if self.database is not None:
            self.database.transactionInProgress = False 
            self.database.save() 

            if self.database.successfulTransactions > 0:
                print("Transaction commited.")
            else: 
                print("Transaction abort.")