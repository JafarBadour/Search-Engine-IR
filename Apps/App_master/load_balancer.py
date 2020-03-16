class LoadBalancer:
    def __init__(self):
        self.slaves = ['http://127.0.0.1:5500/', 'http://127.0.0.1:6500/']
        self.slave_names = ['A', 'B']
        self.name_to_slave = {'A': self.slaves[0], 'B': self.slaves[1]}
        self.slave_load = [0 for i in range(len(self.slaves))]

    def get_free_slave(self):
        temp = list(zip(self.slave_load, self.slaves, [i for i in range(len(self.slaves))]))
        _, mini, ind = min(temp)
        self.slave_load[ind] += 1
        return mini

    def get_slave(self, name):
        return self.name_to_slave[name]
