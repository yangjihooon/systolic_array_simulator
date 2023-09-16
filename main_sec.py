
class Register:
    def __init__(self):
        self.cur_st = None
        self.nxt_st = None
    
    # sets the next state of the register with a value
    def set(self, value):
        self.nxt_st = value

    # gets the current state of the register
    def get(self):
        return self.cur_st
    
    # transfers the next state to the current state
    def transfer(self):
        self.cur_st = self.nxt_st

class ProcessingUnit:
    def __init__(self):
        self.act_reg  = Register()
        self.act_in   = Register()
        self.act_out  = Register()
        self.wgt_reg  = Register()
        self.psum_reg = Register()
        self.psum_in  = Register()
        self.psum_out = Register()
        self.link     = None
        
    def multiply(self, activation):
        self.psum_reg.nxt_st += self.act_reg.get() * self.wgt_reg.cur_st
    
    def run_cycle(self):
        # activation
        self.act_reg.set(self.act_in.get())
        self.act_out.set(self.act_reg.get())
        
        self.psum_reg.set(self.psum_in.get())
        self.psum_out.set(self.psum_reg.get())
        
        if self.link != None:
            self.link.act_in.set(self.act_out.get())
            self.link.psum_in.set(self.psum_out.get())

    def rising_edge(self):
        self.act_in.transfer()
        self.act_reg.transfer()
        self.act_out.transfer()
        self.psum_in.transfer()
        self.psum_reg.transfer()
        self.psum_out.transfer()

    def link_st(self, pe):
        self.link = pe

class SystolicArray:
    def __init__(self, activation, weight):
        self.systolic_array = None
        self.activation     = activation                
        self.wgt            = weight
        self.act_row        = len(activation)
        self.wgt_row        = len(weight)
        pass
    
    def creator(self):
        # makes a systolic array
        self.systolic_array = [ProcessingUnit() for _ in range(self.act_row)]
        
        # initializes the array with the weights
        for i in range(self.wgt_row):
            self.systolic_array[i].wgt_reg.cur_st = self.wgt[i]
             
        for i in range(self.act_row-1):
            self.systolic_array[i].link_st(self.systolic_array[i+1])
            
            
    def simulator(self):
        self.creator()
        act_cnt = 0
        cnt = 0
        
        while self.systolic_array[self.act_row-1].act_out.cur_st != self.activation[self.act_row-1]:
            cnt += 1
            if act_cnt < len(activation):
                self.systolic_array[0].act_in.set(activation[act_cnt])
                act_cnt += 1
            else :
                self.systolic_array[0].act_in.set(None)
                
            # st dbg
            print("after rising edge")
            # ed dbg
            
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].rising_edge()
                
            # st dbg
                print("re{}, act_in_nxt:{}, act_in_cur:{}, act_reg_nxt:{}, act_reg_cur:{}, act_out_nxt:{}, act_out_cur:{}".format(i, self.systolic_array[i].act_in.nxt_st,
                    self.systolic_array[i].act_in.cur_st, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].act_out.nxt_st, self.systolic_array[i].act_out.cur_st))                
            print()
            
            
            print("after clock cylce")
            # ed dbg
            
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].run_cycle()

            # st dbg        
            for i in range(len(self.systolic_array)):            
                print("re{}, act_in_nxt:{}, act_in_cur:{}, act_reg_nxt:{}, act_reg_cur:{}, act_out_nxt:{}, act_out_cur:{}".format(i, self.systolic_array[i].act_in.nxt_st,
                    self.systolic_array[i].act_in.cur_st, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].act_out.nxt_st, self.systolic_array[i].act_out.cur_st))
            print()
            # ed dbg
        print(cnt)    
        
        
    
    
def sum_all(lst):
    sum = 0
    for i in lst:
        sum += i
    return sum

def reverse_lst(lst):
    res = []
    for i in range(1, len(lst)+1):
        res.append(lst[-i])        
    return res

if __name__ == "__main__":
    activation     = [1, 2, 3, 4]
    weight         = [1, 2, 3, 4]
    systolic_array = SystolicArray(activation, weight)
    systolic_array.simulator()
    