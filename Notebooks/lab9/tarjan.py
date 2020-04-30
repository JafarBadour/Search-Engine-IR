cnt = 1
SCCs = []
def dfs(x, cnt, low_link, index, on_stack, S, in_SCC):
    index[x] = cnt
    low_link[x] = cnt
    cnt+=1
    S.append(x)
    on_stack[x] = True
    for u in adj[x]:
        if index[u] == 0:
            dfs(u,cnt, low_link, index, on_stack, S, in_SCC)
            low_link[x] = min(low_link[x], low_link[u])
        elif on_stack[u]:
            low_link[x] = min(low_link[x], low_link[u])

    if in_SCC[x]:
        return
    in_SCC[x] = True
    if low_link[x] == index[x]:
        SCCs.append([])
        while S[-1] != x:
            w = S[-1]
            in_SCC[w] = True
            on_stack[w] = False
            SCCs[-1].append(w)
            S.pop()
        S.pop()
        SCCs[-1].append(x)
    return

def get_list(N, initial=0):
    return [initial for i in range(N)]
adj = [[1], [0]]
nodes = [0,1]
N = len(nodes)
low_link = get_list(N)
index = get_list(N)
S = get_list(N)
on_stack = get_list(N, False)
in_SCC = get_list(N, False)
for node in nodes:
    if index[node] != 0:
        continue
    cnt = 1
    dfs(node,cnt, low_link, index, on_stack, S, in_SCC)
print(len(SCCs))