import numpy  as np

class Register:
    def __init__(self, value=None):
        self.cur_st = value
        self.nxt_st = value
        
        if value is not None:
            self.psum_row_cnt = True
        else:
            self.psum_row_cnt = False
    
    # sets the next state of the register with a value
    def set(self, value):
        if self.psum_row_cnt is True:
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
        if self.psum_row_cnt is True:
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
        self.psum_row_cnt = 0
        
    def run_cycle(self, result, i):
        self.act_reg.set(self.act_in.get())
        

        
        if self.psum_reg.get() != 0:
            self.psum_reg.reset()
            print("current result row", self.psum_row_cnt)
            print("current result col", i)            
            result[self.psum_row_cnt][i] = self.psum_reg.get()
            self.psum_row_cnt += 1
            if self.act_reg.get() is not None:
                self.multiply()
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
        self.act_col        = len(activation[0])
        self.act_row        = len(activation)
        self.wgt            = weight
        self.wgt_col        = len(self.wgt[0])
        self.wgt_row        = len(self.wgt)
        self.result         = [[0 for _ in range(self.wgt_col)] for _ in range(self.act_row)]
    
    def create(self):                
        # makes a systolic array
        self.systolic_array = [[ProcessingUnit() for _ in range(self.wgt_col)] for _ in range(self.wgt_row)]

        # updates the given weight
        for i in range(self.wgt_col):
            for j in range(self.wgt_row):
                self.systolic_array[j][i].update_wgt(self.wgt[j][i])
        
        # links each ports with others
        for i in range(self.wgt_col):
            for j in range(self.wgt_row):
                if i == 0:
                    self.systolic_array[j][i].link(None)
                else:
                    self.systolic_array[j][i].link(self.systolic_array[j][i-1].act_out)    
                
    def simulate(self):
        self.create()
        rotate_cnt = 1
        
        # PE0의 in port가 가르키는 act 변경
        for j in range(self.wgt_row):
            self.systolic_array[j][0].link(activation[0][0])
            self.systolic_array[j][0].run_cycle(self.result, 0)
            
        while self.result[self.act_row-1][self.wgt_col-1] == 0:
            # rising edge
            for i in range(self.wgt_col):
                for j in range(self.wgt_row):
                    self.systolic_array[j][i].rising_edge()                

            print("after rising")
            for i in range(self.wgt_col):
                for j in range(self.wgt_row):
                    print("#{}\tact_nxt {}\tact_cur {}\tpsum_nxt {}\tpsum_cur {}".format(i, self.systolic_array[j][i].act_reg.nxt_st, self.systolic_array[j][i].act_reg.cur_st, self.systolic_array[j][i].psum_reg.nxt_st, self.systolic_array[j][i].psum_reg.cur_st))
            # inputs activation
            for j in range(self.wgt_row):
                if rotate_cnt < self.act_row:
                    self.systolic_array[j][0].link(activation[rotate_cnt][j])
                    rotate_cnt += 1
                else :
                    self.systolic_array[j][0].link(None)

            # clock cycle : 이때 in -> act가 된다.
            for i in range(self.wgt_col):
                for j in range(self.wgt_row):
                    self.systolic_array[j][i].run_cycle(self.result, i)
                    
            print("after cycle")
            for i in range(self.wgt_col):
                for j in range(self.wgt_row):
                    print("#{}\tact_nxt {}\tact_cur {}\tpsum_nxt {}\tpsum_cur {}".format(i, self.systolic_array[j][i].act_reg.nxt_st, self.systolic_array[j][i].act_reg.cur_st, self.systolic_array[j][i].psum_reg.nxt_st, self.systolic_array[j][i].psum_reg.cur_st))
            print()
        return self.result

if __name__ == "__main__":
    activation     = [[1],
                      [2], 
                      [3],
                      [4]]
    weight         = [[1]]
    systolic_array = SystolicArray(activation, weight)
    result = np.array(systolic_array.simulate())
    print(result)