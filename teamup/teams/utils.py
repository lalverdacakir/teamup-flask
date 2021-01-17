

def filter_by_course(course_tuple_id_list,course_tuple_list,team_dict_list):
    res = list()

    for team in team_dict_list:
        for each in course_tuple_id_list:
            print(team['courseCode'],"---",course_tuple_list[each][1])
            if(team['courseCode'] == course_tuple_list[each][1]):
                res.append(team)
    print('res: ',res)
    return res

def filter_by_isAccepting(accepting,team_dict_list):
    if(accepting==1):
        accepting  = True
    else:
        accepting = False
    res = list()
    if(team_dict_list):
        for team in team_dict_list:
            if(team['isAccepting'] == accepting):
                res.append(team)
    return res

def filter_by_name(search_text,team_dict_list):
    res = list()
    if(team_dict_list):
        for team in team_dict_list:
            if(team['teamName'].find(search_text)!=-1):
                res.append(team)

    return res