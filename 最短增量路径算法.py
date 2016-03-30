#算法设计与分析基础（第三版）P282算法
#最短增量路径算法
from collections import deque
from copy import deepcopy
class edge:
    u = 0 #容量
    x = 0 #流量
    def __init__(self,source,target,u,x=0):
        self.u = u
        self.target = target #目标节点
        self.source = source #源节点
        self.x = x
    def pp(self):
        print self.target,self.u,self.x
class vetrex:
    #neighbor = []      #不能这样写，会公用地址 
    def __init__(self,num):   
        self.forward_edges = []  # 存储前向边
        self.backward_edges = [] # 存储后向边
        self.sign = 0   #标记,0无,1为向前,2为向后
        self.num  = num   #节点编号
        self.pre = -1 #前驱的编号,-1表示还没有前驱,前驱可以是通过前向边也可以是后向边
    def pp(self):
        for edge in self.forward_edges:
            edge.pp()
class Graph:
    def __init__(self,N,input_list):
        self.N =N
        M = len(input_list)/3  #N为节点数，M为边数
        self.vetrex_list = [vetrex(i)for i in range(N)] #存储图的所有节点的列表
        #读取数据，数据用列表按照从i到j容量为x(i,j,x)的方式存储，每三个数据为1组
        for i in range(M):
            a_edge = edge(input_list[3*i],input_list[3*i+1],input_list[3*i+2])
            self.vetrex_list[input_list[3*i]].forward_edges.append(a_edge) #注意下面插入的是同一条边，地址相同
            self.vetrex_list[input_list[3*i+1]].backward_edges.append(a_edge)
    def pp(self):
        for vetrex in self.vetrex_list:
            vetrex.pp()
            print '-'*70
            print self.vetrex_list[2].backward_edges[0].source
        
    def  ShorestAugmentingPath(self):
        #广度搜索，寻找增量路径
        N = self.N
        self.vetrex_list[0].sign = 2 #源点标负号
        r = 10**8   #r为路径的流量，初识化为无穷大
        queue = deque([])  #
        queue.append(self.vetrex_list[0])  #源点入队
        while len(queue)!=0: 
            v = queue[0]
            queue.popleft()  #队尾出队
            for edge in v.forward_edges:  #寻找满足条件的前向边
                if self.vetrex_list[edge.target].sign==0:  
                    new_r = edge.u-edge.x
                    if new_r>0:
                        print v.num,self.vetrex_list[edge.target].num,edge.x
                        r = min(new_r,r)
                        self.vetrex_list[edge.target].sign = 1  #对下个节点标记1，表示通过前向边到达
                        self.vetrex_list[edge.target].pre  = v.num  #记录前驱，找到汇点后要反向寻找路径
                        queue.append(self.vetrex_list[edge.target])  #下个节点入队
            for edge in v.backward_edges:  #寻找满足条件的后向边
                if self.vetrex_list[edge.source].sign==0:
                    if edge.x > 0:
                        print v.num,self.vetrex_list[edge.source].num,edge.x
                        r = min(r,edge.x)
                        self.vetrex_list[edge.source].sign = 2  #对下个节点标记2，表示通过前向边到达
                        self.vetrex_list[edge.source].pre  = v.num  #记录前驱，找到汇点后要反向寻找完整路径
                        queue.append(self.vetrex_list[edge.source])  #下个节点入队
            if  self.vetrex_list[N-1].sign == 1:  #如果已经到达汇点
                j = N-1
                print '-'*70
                print r,'************'
                print '-'*70
                #更新流量
                while j!=0:  #反向寻找完整路径，由于路径上的节点都标有前驱，速度很快
                    if self.vetrex_list[j].sign == 1:
                        pre_num = self.vetrex_list[j].pre
                        for edge in self.vetrex_list[j].backward_edges:
                            if edge.source ==pre_num:
                                edge.x = edge.x+r  #前向边增加流量
                                j = pre_num
                                #print j
                                break
                    elif self.vetrex_list[j].sign == 2:
                        pre_num = self.vetrex_list[j].pre
                        for edge in self.vetrex_list[j].forward_edges:
                            if edge.target ==pre_num:
                                edge.x = edge.x-r #后向边减少流量
                                j = pre_num
                                #print j
                                break
                #重新寻找路径，对G的标记初始化
                for vetrex in self.vetrex_list:
                    vetrex.sign = 0
                    vetrex.pre  = -1
                self.vetrex_list[0].sign = 2 #源点标负号
                queue.clear()
                queue.append(self.vetrex_list[0])
                r = 10**8
        total_flow = 0  #返回总流量
        for edge in self.vetrex_list[0].forward_edges:
            total_flow += edge.x
        return total_flow

if __name__=='__main__':
    #测试示例，为简单起见，源点编号为0，汇点为N-1，N为节点总数
    input_list = [
        0,1,2,
        1,2,5,
        1,4,3,
        3,2,1,
        0,3,3,
        4,5,4,
        2,5,2
        ]
    '''
    input_list = [
        0,1,3,
        0,2,2,
        1,3,3,
        1,4,4,
        2,4,2,
        3,5,2,
        4,5,3
        ]
    input_list = [
        0,1,8,
        0,2,14,
        2,1,5,
        1,3,3,
        2,3,3,
        1,4,6,
        2,5,8,
        3,4,4,
        5,3,3,
        4,6,7,
        3,6,10,
        5,6,6
        ]
        '''
    G  = Graph(6,input_list)
    #G.pp()
    print G.ShorestAugmentingPath()
    
