
tact_life_client_1 = 64
tact_life_client_2 = 32

tact_start_process_client_1 = 10
tact_start_process_client_2 = 4


class SystemMemory:
    # [8,8,8,8,8,8,8,8, 16,16,16,16, 32,32] блоки памяти

    def __init__(self, memory   = [8,8,8,8,8,8,8,8, 16,16,16,16, 32,32],
         memory_occupied        = [0,0,0,0,0,0,0,0, 0,0,0,0, 0,0],
         tact_memory_occupied   = [0,0,0,0,0,0,0,0, 0,0,0,0, 0,0],
         memory_is_available = True):

        self.memory = memory  
        self.memory_occupied = memory_occupied
        self.tact_memory_occupied = tact_memory_occupied
        self.memory_is_available = memory_is_available

    def check_memory_full(self, client):        
        if client == 1:
            mem_for_client_1 = self.memory_occupied[8:] # для процесса 1 клиента подходят только ячейки по 16 и 32 Мб
            self.memory_is_available = True if 0 in mem_for_client_1 else False   
        else:
            mem_for_client_2 = self.memory_occupied # процесс 2 клиента помещается в любую ячейку
            self.memory_is_available = True if 0 in mem_for_client_2 else False            


    def select_block_of_memory_start_process(self, client, tact):
        if client == 1:
            self.check_memory_full(1)
            if self.memory_is_available:
                for i in range(len(self.memory)):
                    if (self.memory[i] > 12) and (self.memory_occupied[i] == 0):
                        self.memory_occupied[i] = 1
                        self.tact_memory_occupied[i] = tact
                        print("start 1 client process")
                        break                
            else:
                print("no memory for 1 client, tact = ", tact)


        else:
            self.check_memory_full(2)            
            if self.memory_is_available:
                for i in range(len(self.memory)):
                    if (self.memory[i] > 4) and (self.memory_occupied[i] == 0):
                        self.memory_occupied[i] = 2
                        self.tact_memory_occupied[i] = tact
                        print("start 2 client process")                       
                        break                
            else:
                print("no memory for 2 client, tact = ", tact)


        
    def clear_memory_after_end_of_process(self, num_block_of_memory):
        self.memory_occupied[num_block_of_memory] = 0
        self.tact_memory_occupied[num_block_of_memory] = 0


if __name__ == "__main__":

    Session = SystemMemory()

    #появление процесса на первом такте
    tact = 1
    Session.select_block_of_memory_start_process(1, tact)
    Session.select_block_of_memory_start_process(2, tact)
    
    while Session.memory_is_available:

        if ((tact-1) % tact_start_process_client_1 == 0) and (tact !=1):   #появление процесса от 1 клиента
            Session.select_block_of_memory_start_process(1, tact)
        if ((tact-1) % tact_start_process_client_2 == 0) and (tact !=1):   #появление процесса от 2 клиента
            Session.select_block_of_memory_start_process(2, tact)

        # проверка не закончился ли какой-нибудь процесс 
        for i in range(len(Session.memory_occupied)):

            if Session.memory_occupied[i] == 1:
                if (tact - Session.tact_memory_occupied[i]) == tact_life_client_1:
                    Session.clear_memory_after_end_of_process(i)
                    print("i = ", i)
                    print("stop client 1 process")
            elif Session.memory_occupied[i] == 2:
                if (tact - Session.tact_memory_occupied[i]) == tact_life_client_2:
                    Session.clear_memory_after_end_of_process(i)
                    print("i = ", i)
                    print("stop client 2 process")   


           
        #print("tact ", tact)
        print("memory ",Session.memory_occupied, " tact =  ", tact)
        #print("tact ", Session.tact_memory_occupied)
        print(" \n")
    
        tact = tact + 1
    
    
