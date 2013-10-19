"""
Find the optimized number of feeds to show in a limited windows size. The program uses 0-1 knapsack problem solving to find out
the items to fit in, in every reload event. Dynamic programming method used for solving the knapsack.
"""
def find_feed_optimization():
    N, W, H = 0, 0, 0
    start_index, scount = 0, 0
    latest_story_time = 0
    v, w = [], []
    time_check = {}

    lines = __get_input()
    for i, line in enumerate(lines):
        if i==0:
            first_line = line.split()
            N = int(first_line[0])
            W = int(first_line[1])
            H = int(first_line[2])
            
        elif line.startswith('S'):
            story_info = line.split()
            time_check[story_info[1]] = scount
            latest_story_time = max(latest_story_time, int(story_info[1]))
            v.append(int(story_info[2]))
            w.append(int(story_info[3]))
            scount += 1
            
        elif line.startswith('R'):
            reload_info = line.split()
            reload_time = int(reload_info[1])
            lookup_key = max(0, reload_time - W)
            
            if lookup_key>0:
                while not str(lookup_key) in time_check and lookup_key <= latest_story_time:
                    lookup_key += 1
                start_index = time_check.get(str(lookup_key), None)
            if start_index == None:
                print 'Can\'t find story for this reload at ' + str(reload_time)
                continue

            total_value, used_items = __knapsack(v[start_index:], w[start_index:], H)
            count_used_items = 0
            items_string = ''

            used_items = [0]*start_index + used_items
            for i, x in enumerate(used_items):
                if x>0:
                    count_used_items += 1
                    items_string += str(i+1) + ' '
            print '%s %s %s' % (total_value, count_used_items, items_string)
            
def __get_input():
    i = 0
    N = 0
    lines = []
    while True:
        s = raw_input('=>')
        if s.strip() == '':
            continue
        if i==0:
            info = s.split()
            N = int(info[0])
        lines.append(s)
        if i==N:
            break
        i += 1
    return lines

def __knapsack(v, w, W):
    n = len(v)
    c = [[0]*(W+1) for _ in range(n)]
    for i in range(n):
        for j in range(W+1):
            if w[i]>j:
                c[i][j] = c[i-1][j]
            else:
                c[i][j] = v[i] if i==0 else max(c[i-1][j], v[i]+c[i-1][j-w[i]])
    return c[n-1][W], __get_used_items(c, w)

def __get_used_items(c, w):
    i = len(c)-1
    cweight = len(c[0])-1
    marked = [0 for _ in range(len(c))]
    while (i>=0 and cweight>=0):
        if (i==0 and c[i][cweight]>=w[i]) or (i>0 and c[i][cweight] != c[i-1][cweight]):
            marked[i] = 1
            cweight = cweight-w[i]
        i = i-1
    return marked

if __name__ == "__main__":
    find_feed_optimization()
