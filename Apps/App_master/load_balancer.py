class LoadBalancer:
    def __init__(self):
        self.slaves = ['http://127.0.0.1:5500/post_query/', 'http://127.0.0.1:6500/post_query/']
        self.slave_load = [0 for i in range(len(self.slaves))]

    def get_free_slave(self):
        temp = list(zip(self.slave_load, self.slaves, [i for i in range(len(self.slaves))]))
        _, mini, ind = min(temp)
        self.slave_load[ind] += 1
        return mini
