
class Register:
    def __init__(self):
        self.cur_st = None
        self.nxt_st = None
    
    def set(self, value):
        self.nxt_st = value

    def get(self):
        return self.cur_st

class ProcessingUnit:
    def __init__(self):
        self.act_reg = Register()
        self.act_in  = Register()   # input port
        self.act_out = Register()   # output port
        self.wgt_reg     = Register()
        self.psum_reg    = Register()
        self.psum_in = Register()
        self.psum_out = Register()
        self.link    = None
        
    def multiply(self, activation):
        pass
    
    def run_cycle(self):
        self.act_reg.set(self.act_in.get())
        
        if self.link != None:
            self.link.act_in.set(self.act_out.get())

    def rising_edge(self):
        self.act_reg.cur_st  = self.act_reg.nxt_st
        self.act_out.cur_st  = self.act_reg.nxt_st
        self.psum_reg.cur_st = self.psum_reg.nxt_st
        self.psum_out.cur_st = self.psum_reg.nxt_st

    def link_pe(self, pe):
        self.link = pe

class SystolicArray:
    def __init__(self, activation, weight):
        self.systolic_array = None
        self.activation     = activation                
        self.wgt            = weight
        self.act_row        = len(activation)
        pass
    
    def creator(self):
        # makes a systolic array
        self.systolic_array = [ProcessingUnit() for _ in range(self.act_row)]
        
        # initializes the array with the weights and links        
        for i in range(self.act_row):
            self.systolic_array[i].wgt.cur_st = self.wgt[i]
            
            if i < self.act_row-1:
                self.systolic_array[i].link_pe(self.systolic_array[i+1])
            
            
    def simulator(self):
        self.creator()
        act_cnt = 0
        
        while self.systolic_array[self.act_row-1].act_out.cur_st != self.activation[self.act_row-1]:
            if act_cnt < len(activation):
                self.systolic_array[0].act_in.set(activation[act_cnt])
                act_cnt += 1
            else :
                self.systolic_array[0].act_in.set(None)
                
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].rising_edge()
                
                # st dbg
                print("after rising edge, re{}, act_in_nxt:{}, act_in_cur:{}, act_reg_nxt:{}, act_reg_cur:{}, act_out_nxt:{}, act_out_cur:{}".format(i, self.systolic_array[i].act_in.nxt_st,
                    self.systolic_array[i].act_in.cur_st, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].act_out.nxt_st, self.systolic_array[i].act_out.cur_st))
                # ed dbg
            
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].run_cycle()

            # st dbg        
            for i in range(len(self.systolic_array)):            
                print("after cycle, re{}, act_in_nxt:{}, act_in_cur:{}, act_reg_nxt:{}, act_reg_cur:{}, act_out_nxt:{}, act_out_cur:{}".format(i, self.systolic_array[i].act_in.nxt_st,
                    self.systolic_array[i].act_in.cur_st, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st, self.systolic_array[i].act_out.nxt_st, self.systolic_array[i].act_out.cur_st))
            print()
            # ed dbg        
        
        
    
        

if __name__ == "__main__":
    activation     = [1, 2, 3, 4]
    weight         = [1, 2, 3, 4]
    systolic_array = SystolicArray(activation, weight)
    systolic_array.simulator()