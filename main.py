class Register:
    def __init__(self, cur_st=None, nxt_st=None):
        self.cur_st = cur_st
        self.nxt_st = nxt_st
    
    # sets the next state of the register with a value
    def set(self, value):
        self.nxt_st = value

    # gets the current state of the register
    def get(self):
        return self.cur_st
    
    # transfers the next state to the current state
    def transfer(self):
        self.cur_st = self.nxt_st

class Port:
    def __init__(self):
        self.link_st = None
    
    def get(self):
        if isinstance(self.link_st ,Port):
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

    def rising_edge(self):
        self.act_reg.transfer()
        
    def link(self, other):
        self.act_out.link(self.act_reg)
        self.act_in.link(other)

    def get(self):
        return self.act_reg.get()
    
    def update_wgt(self, weight):
        self.wgt_reg.set(weight)
        self.wgt_reg.transfer()

    def multiply(self):
        pass

class SystolicArray:
    def __init__(self, activation, weight):
        self.systolic_array = None
        self.activation     = activation                
        self.act_row        = len(activation)
        self.wgt            = weight
    
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
        
        # debuging current weight and link
        # st dbg
        # print("weight updating state")
        # for i in range(self.act_row):
        #     print("PE{}\twgt {}".format(i, self.systolic_array[i].wgt_reg.get()))
        # print()
        # print("linking state")
        # for i in range(self.act_row):
        #     print("PE{}\tinp {}\toutp {}".format(i, self.systolic_array[i].act_in.link_st, self.systolic_array[i].act_out.link_st))
        # ed dbg

        
            
    def simulate(self):
        self.create()
        rotate_cnt = 0
        cnt = 0
        
        # for i in range(10):
        #     if i < len(activation):
        #         self.systolic_array[0].link(activation[i])
        #         print("#{}\t input_port {}".format(i, self.systolic_array[0].act_in.get()))
        #     else:
        #         self.systolic_array[0].act_in.link(None)
        #         print("#{}\t input_port {}".format(i, self.systolic_array[0].act_in.get()))
        
        while self.systolic_array[self.act_row-1].get() != self.activation[self.act_row-1]:
            cnt += 1
            
            # links input activation to PE01
            if rotate_cnt < len(activation):
                self.systolic_array[0].link(activation[rotate_cnt])
                rotate_cnt += 1
            else :
                self.systolic_array[0].link(None)
                
            # st dbg
            print("after rising edge")
            # ed dbg
            
            # rising edge
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].rising_edge()
                
            # st dbg
                print("#{}\treg_nxt {}\treg_cur {}".format(i, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st))                
            print()
                                    
            print("after clock cylce")
            # ed dbg
            
            # clock cycle
            for i in range(len(self.systolic_array)):
                self.systolic_array[i].run_cycle()

            # st dbg        
            for i in range(len(self.systolic_array)):            
                print("#{}\treg_nxt {}\treg_cur {}".format(i, self.systolic_array[i].act_reg.nxt_st, self.systolic_array[i].act_reg.cur_st))
            print()
            # ed dbg
        print("totla cycle {}".format(cnt))

if __name__ == "__main__":
    activation     = [i for i in range(10)]
    weight         = [i for i in range(2, 12)]
    systolic_array = SystolicArray(activation, weight)
    systolic_array.create()
    systolic_array.simulate()
