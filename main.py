import numpy  as np

class Register:
    def __init__(self, value=None):
        self.cur_st = value
        self.nxt_st = value
        
        if value is not None:
            self.psum_flag = True
        else:
            self.psum_flag = False
    
    # sets the next state of the register with a value
    def set(self, value):
        if self.psum_flag is True:
            self.nxt_st += value
        else:
            self.nxt_st = value

    # gets the current state of the register
    def get(self):
        return self.cur_st
    
    # transfers the next state to the current state
    def transfer(self):
        self.cur_st = self.nxt_st
        
    def reset(self):
        if self.psum_flag is True:
            self.nxt_st = 0

class Port:
    def __init__(self):
        self.link_st = None
    
    def get(self):
        if isinstance(self.link_st, Port):
            return self.link_st.get()
        elif isinstance(self.link_st, Register):
            return self.link_st.get()
        else:
            return self.link_st
        
    def link(self, element):
        self.link_st = element

class ProcessingUnit:
    def __init__(self):
        self.act_in   = Port()
        self.act_reg  = Register()        
        self.act_out  = Port()
        self.wgt_reg  = Register()
        self.psum_in  = Port()
        self.psum_reg = Register(0)
        self.psum_out = Port()
        
    def run_cycle(self):
        self.act_reg.set(self.act_in.get())
        
        if self.psum_reg.get() != 0:
            self.psum_reg.reset()
            if self.act_reg.get() is not None:
                self.multiply()
            return self.psum_reg.get()
        else:
            if self.act_reg.get() is not None:
                self.multiply()

    def rising_edge(self):
        self.act_reg.transfer()
        self.psum_reg.transfer()
        
    def link(self, other):
        self.act_out.link(self.act_reg)
        self.act_in.link(other)

    def get(self):
        return self.act_reg.get()
    
    def update_wgt(self, weight):
        self.wgt_reg.set(weight)
        self.wgt_reg.transfer()

    def multiply(self):
        self.psum_reg.set(self.act_reg.get() * self.wgt_reg.get())

class SystolicArray:
    def __init__(self, activation, weight):
        self.systolic_array = None
        self.activation     = activation                
        self.act_row        = len(activation)
        self.wgt            = weight
        self.result         = []
    
    def create(self):
        # makes a systolic array
        self.systolic_array = [ProcessingUnit() for _ in range(self.act_row)]

        # updates the given weight
        for i in range(self.act_row):
            self.systolic_array[i].update_wgt(self.wgt[i])
        
        # links each ports with others
        for i in range(self.act_row):
            if i == 0:
                self.systolic_array[i].link(None)
            else:
                self.systolic_array[i].link(self.systolic_array[i-1].act_out)    
                
    def simulate(self):
        self.create()
        rotate_cnt = 1
        
        # PE0의 in port가 가르키는 act 변경            
        self.systolic_array[0].link(activation[0])
        self.systolic_array[0].run_cycle()        
        
        while len(self.result) < self.act_row ** 2:
            # rising edge
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].rising_edge()                

            print("after rising")
            for i in range(len(self.systolic_array)):
                print("#{}\tact_nxt {}\tact_cur {}\tpsum_nxt {}\tpsum_cur {}".format(i, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].psum_reg.nxt_st, self.systolic_array[i].psum_reg.cur_st))

            if rotate_cnt < len(activation):
                self.systolic_array[0].link(activation[rotate_cnt])
                rotate_cnt += 1
            else :
                self.systolic_array[0].link(None)

            # clock cycle : 이때 in -> act가 된다.
            for i in range(len(self.systolic_array)):
                result = self.systolic_array[i].run_cycle()
                if result is not None:
                    self.result.append(result)
                    
            print("after cycle")
            for i in range(len(self.systolic_array)):
                print("#{}\tact_nxt {}\tact_cur {}\tpsum_nxt {}\tpsum_cur {}".format(i, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].psum_reg.nxt_st, self.systolic_array[i].psum_reg.cur_st))
            print()                            
            
        a = np.array(self.result)
        a.reshape(self.act_row, self.act_row)
        return a
        
                

if __name__ == "__main__":
    activation     = [1, 2, 3]
    weight         = [1, 2, 3]
    systolic_array = SystolicArray(activation, weight)
    systolic_array.create()
    a = systolic_array.simulate()
    
    r = [[0 for _ in range(len(activation))] for _ in range(len(activation))]    