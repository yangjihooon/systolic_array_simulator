
class Register:
    def __init__(self):
        self._cur_st = None
        self._nxt_st = None
    
    # sets the next state of the register with a value
    def set(self, value):
        self._nxt_st = value

    # gets the current state of the register
    def get(self):
        return self._cur_st
    
    # transfers the next state to the current state
    def transfer(self):
        self._cur_st = self._nxt_st

class Port:
    def __init__(self):
        self._link_st = None
    
    def get(self):
        if isinstance(self._link_st ,Port):
            # st dbg
            print("Port")
            # ed ddg
            self._link_st.get()
        elif isinstance(self._link_st, Register):
            # st dbg
            print("Register")
            # ed ddg            
            self._link_st.get()
        else:
            return self._link_st
        
    
    def link(self, element):
        self._link_st = element

class ProcessingUnit:
    def __init__(self):
        self._act_reg  = Register()
        self._act_in   = Port()
        self._act_out  = Port()
        
    def run_cycle(self):
        self._act_reg.set(self._act_in.get())

    def rising_edge(self):
        self._act_reg.transfer()

class SystolicArray:
    def __init__(self, activation):
        self.systolic_array = None
        self.activation     = activation                
        self.act_row        = len(activation)
    
    def create(self):
        # makes a systolic array
        self.systolic_array = [ProcessingUnit() for _ in range(self.act_row)]
        
        # links each ports with others
        for i in range(self.act_row):
            if i != 0:
                self.systolic_array[i]._act_in.link(self.systolic_array[i-1]._act_out)            
            self.systolic_array[i]._act_out.link(self.systolic_array[i]._act_reg)
            
            
    def simulate(self):
        self.create()
        act_cnt = 0
        cnt = 0
        
        for i in range(10):
            if i < len(activation):
                self.systolic_array[0]._act_in.link(activation[i])
                print("#{}\t act_in {}".format(i, self.systolic_array[0]._act_in.get()))
            else:
                self.systolic_array[0]._act_in.link(None)
                print("#{}\t act_in {}".format(i, self.systolic_array[0]._act_in.get()))
        
        
                
        # self.systolic_array[self.act_row-1]._act_reg._cur_st != self.activation[self.act_row-1]
        
        while cnt != 10:
            cnt += 1
            
            if act_cnt < len(activation):
                self.systolic_array[0]._act_in.link(activation[act_cnt])
                act_cnt += 1
            else :
                self.systolic_array[0]._act_in.link(None)
                
            # st dbg
            print("after rising edge")
            # ed dbg
            
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].rising_edge()
                
            # st dbg
                print("#{}\treg_nxt {}\treg_cur {}".format(i, self.systolic_array[i]._act_reg._nxt_st, self.systolic_array[i]._act_reg._cur_st))                
            print()
                                    
            print("after clock cylce")
            # ed dbg
            
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].run_cycle()

            # st dbg        
            for i in range(len(self.systolic_array)):            
                print("#{}\treg_nxt {}\treg_cur {}".format(i, self.systolic_array[i]._act_reg._nxt_st, self.systolic_array[i]._act_reg._cur_st))
            print()
            # ed dbg
        print(cnt)    

if __name__ == "__main__":
    activation     = [1, 2, 3, 4]
    weight         = [1, 2, 3, 4]
    systolic_array = SystolicArray(activation)
    systolic_array.create()
    # systolic_array.simulate()
    
    # for i in range(len(activation)):
    #     print("#{}\tin_pt {}\tout_pt {}".format(i, type(systolic_array.systolic_array[i]._act_in._link_st), type(systolic_array.systolic_array[i]._act_out._link_st)))
    
    processing_element = ProcessingUnit()
    input_port = Port()
    output_port = Port()
    
    output_port.link(processing_element._act_reg)
    input_port.link(output_port)
    
    processing_element._act_reg._cur_st = 100
    
    print(output_port._link_st._cur_st)
    
        
        
    
