"""
Searching nearest point given a query x,y position is done through finding nearest neighbors of the grid in which the query point is located.
Initially, the plan is divided into equal-size grid and the topics are assigned with respective grid. In search time, the grid which
contains query point will look for nearest neighbors layer by layer until the required number of topics/questions is detected.
Layer by layer means, in first level of neighbors, the grids around the current grid (containing query point) are considered. If the number
of results is not satisfied yet, increase layer and consider the similar around the resulting grid from the 1st level neighbors. This
repeats until either number of results reach the desired point or it is no longer possible to get more topic/question because all
are detected.
"""
class Topic:
    """
    Object of this class represents a topic in the input
    """
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

def find_nearby():
    """
    Main method of the program to find the nearby points according to the query using the strategy provided in question
    """
    T, Q, N = 0, 0, 0
    topic_lines, question_lines, query_lines = [], [], []
    max_x, max_y = 0, 0
    window_size = 25 #the width/height of each square grid on the xy-plane

    #Getting input lines
    lines = __get_input()
    for i, line in enumerate(lines):
        if i==0:
            first_line = line.split()
            T = int(first_line[0])
            Q = int(first_line[1])
            N = int(first_line[2])
        elif T>0:
            topic_line = line.split()
            topic_lines.append(line)
            x = float(topic_line[1])
            max_x = max(x, max_x)
            y = float(topic_line[2])
            max_y = max(y, max_y)
            T -= 1
        elif Q>0:
            quest_line = line.split()
            question_lines.append(line)
            Q -= 1
        elif N>0:
            query_line = line.split()
            query_lines.append(line)
            x = float(query_line[2])
            max_x = max(x, max_x)
            y = float(query_line[3])
            max_y = max(y, max_y)
            N -= 1

    #Add 5 as a padding
    max_x = int(max_x) + 5
    max_y = int(max_y) + 5
    grid = [[None]*int(max_x/window_size) for _ in range(int(max_y/window_size))] #Populate the grid

    #Find xpoints and ypoints with respect to grid number so that incoming topics can be determined their respective grid
    x_points = [0]*max_x
    index = 0
    bound = window_size
    for i in range(len(x_points)):
        if i>=(max_x-5):
            x_points[i] = x_points[i-1]
        elif i<bound:
            x_points[i] = index    
        else:
            index += 1
            x_points[i] = index
            bound = window_size * (index+1)

    y_points = [0]*max_y
    index = 0
    bound = window_size
    for i in range(len(y_points)):
        if i>=(max_y-5):
            y_points[i] = y_points[i-1]
        elif i<bound:
            y_points[i] = index
        else:
            index += 1
            y_points[i] = index
            bound = window_size * (index+1)

    #Go through each topic, create Topic object and assign related grid number
    for i in range(len(topic_lines)):
        topic_line = topic_lines[i].split()
        x = int(float(topic_line[1]))
        y = int(float(topic_line[2]))
        topic = Topic(float(topic_line[1]), float(topic_line[2]), int(topic_line[0]))
        if not grid[y_points[y]][x_points[x]]:
            grid[y_points[y]][x_points[x]] = {'topics':[topic]}
        else:
            grid[y_points[y]][x_points[x]]['topics'].append(topic)

    #Go through each question, create mapping between topic and question, so that later on, during searching program can determine the
    #number of results in searching neighbors
    topics_to_question = {}
    for i in range(len(question_lines)):
        q_line = question_lines[i].split()
        qid = int(q_line[0])
        num_topic = int(q_line[1])
        for i in range(2, 2+num_topic):
            topic_id = int(q_line[i])
            if topic_id in topics_to_question:
                lst = topics_to_question[topic_id]
                lst.append(qid)
                lst = sorted(lst)
                lst.reverse()
                topics_to_question[topic_id] = lst
            else:
                topics_to_question[topic_id] = [qid]

    #Process query lines
    for i in range(len(query_lines)):
        query_line = query_lines[i].split()
        grids_to_find = []
        topics_found = []

        if query_line[0]=='t' or query_line[0]=='q':
            result_count = int(query_line[1])
            total_num_possible = len(topic_lines)
            if query_line[0]=='q':
                total_num_possible = len(question_lines)
            result_count = min (result_count, total_num_possible) #update result count to ensure termination of the upcoming while loop

            #query point (x,y)
            x = int(float(query_line[2]))
            y = int(float(query_line[3]))
            
            qx, qy = x_points[x], y_points[y]
            neighbors_level = 1

            while result_count>0:
                temp = __update_info_by_neighbor(qy, qx, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                result_count -= temp

                #Consider the grid in north east direction, and all the grids (vertically) located in between north east grid and south east grid
                temp = __update_info_by_neighbor(qy+neighbors_level, qx+neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                result_count -= temp
                for i in range(qy-neighbors_level+1, qy+neighbors_level):
                    temp = __update_info_by_neighbor(i, qx+neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                    result_count -= temp

                #Consider the grid in south east direction, and all the grids (horizontally) located in between south east grid and south west grid
                temp = __update_info_by_neighbor(qy-neighbors_level, qx+neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                result_count -= temp
                for i in range(qx-neighbors_level+1, qx+neighbors_level):
                    temp = __update_info_by_neighbor(qy-neighbors_level, i, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                    result_count -= temp
                    
                #Consider the grid in south west direction, and all the grids (vertically) located in between south west grid and north west grid
                temp = __update_info_by_neighbor(qy-neighbors_level, qx-neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                result_count -= temp
                for i in range(qy-neighbors_level+1, qy+neighbors_level):
                    temp = __update_info_by_neighbor(i, qx-neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                    result_count -= temp

                #Consider the grid in north west direction, and all the grids (horizontally) located in between north west grid and north east grid
                temp = __update_info_by_neighbor(qy+neighbors_level, qx-neighbors_level, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                result_count -= temp
                for i in range(qx-neighbors_level+1, qx+neighbors_level):
                    temp = __update_info_by_neighbor(qy+neighbors_level, i, grids_to_find, topics_found, grid, query_line[0], topics_to_question)
                    result_count -= temp
                    
                neighbors_level += 1
                
            result_count = int(query_line[1]) #Get original number of results required
            grids_to_find = list(set(grids_to_find))
            result_string = __find_topics(topics_found, result_count, x, y, query_line[0], topics_to_question) #Find topics or questions
            print result_string
        

def __update_info_by_neighbor(x, y, found_grids, topics_found_sofar, gd, query_type, mem):
    """
    Got to the specified position, find topics/questions and update the respective auxiliary datas including results count
    """
    points_detect_count = 0
    if x<len(gd[0]) and y<len(gd) and x>=0 and y>=0:
        found_grids.append((x,y))
        if gd[x][y] != None:
            topics_found_sofar += gd[x][y]['topics']
            points_detect_count = len(gd[x][y]['topics'])
            if query_type == 'q':
                points_detect_count = 0
                for topic in gd[x][y]['topics']:
                    points_detect_count += len(mem.get(topic.name, []))
    return points_detect_count

def __find_topics(topics_found_sofar, N, qx, qy, query_type, mem):
    """
    Once the topics are set, this function calculate the distance and find the nearest topic/question.
    The distance calculation is according to the distance between two points of 2D place from wikipedia.
    """
    import math
    dt_topic = {}
    for topic in topics_found_sofar:
        tx = topic.x
        ty = topic.y
        dist = math.sqrt(math.pow((qx-tx), 2) + math.pow((qy-ty), 2)) #Find distance betwee two points on xy-plane
        if dist in dt_topic:
            lst = dt_topic[dist]
            lst.append(topic.name)
            lst = sorted(lst)
            lst.reverse()
            dt_topic[dist] = lst
        else:
            dt_topic[dist] = [topic.name]
    res_required = N
    res_str = ''
    shown_aldy = set()
    if query_type == 'q':
        for k in sorted(dt_topic.keys()):
            if res_required<1:
                break
            lst = dt_topic[k]
            for item in lst:
                questions = mem.get(item, [])
                for question in questions:
                    if question not in shown_aldy:
                        shown_aldy.add(question)
                        res_str += str(question) + ' '
                        res_required -= 1
                        if res_required<1:
                            break
    else:
        for k in sorted(dt_topic.keys()):
            if res_required<1:
                break
            lst = dt_topic[k]
            for item in lst:
                if item not in shown_aldy:
                    shown_aldy.add(item)
                    res_str += str(item) + ' '
                    res_required -= 1
                    if res_required<1:
                        break
    return res_str

def __get_input():
    i = 0
    T, Q, N = 0, 0, 0
    total = 0
    lines = []
    while True:
        s = raw_input('=>')
        if s.strip() == '':
            continue
        if i==0:
            first_line = s.split()
            T = int(first_line[0])
            Q = int(first_line[1])
            N = int(first_line[2])
            total = T+Q+N
        lines.append(s)
        if i==total:
            break
        i += 1
    return lines

if __name__ == "__main__":
    find_nearby()
