import sys
import itertools

#   On burrow.soic.indiana.edu use this command to run: python ./assign.py input.txt k m n
#   The given problem is to minimize the amount of grading time for the number of teams to be formed given the survey
#   of user inputs.
#   Goal state: In the approach below, the goal state is to assign students in teams such that the amount of grading time
#   is minimized and students get their favored team partners.
#   Assumptions: In my approach, I have tried to minimize the total teams by assigning them partners they wanted. In case of
#   wanted partners more than 3, the first 2 will be assigned to the given student. The students with preferences of working in
#   a team of two, will also be satisfied. The remaining teams have been formed based on the students who were not assigned a team
#   before. The user_assigned dictionary checks where each student has been assigned a team and if it is assigned a team, it
#   discards considering any teams in which an already assigned user has been found. Thus, the search space is restricted to only
#   those teams in which there were no students been assigned yet.
#   This code gives the best teams which the user asked for. So, there is a minor tradeoff between the best grading time and the best
#   teams.
#   Simplifications: Team preferences for team size 2,3 are taken into consideration. For team size 1, because of minimizing the
#   grading time, the teams with team size 1 have been assigned to teams with size 3.

#Read the input file in a dictionary format
def readFileDict(dict):
    input_file = str(sys.argv[1])
    data = open(input_file, 'r')
    for line in data:
        line = map(str, line.split())
        key, value = line[0], line[1:]
        dict[key] = value
    data.close()

#Function that displays the output of the grading time required to grade all the teams
def usernames_list(dict, k, m, n):
    teams = []
    for key, value in dict.iteritems():
        usernames.append(key)

    #Initialize the user assigned dictionary
    for user in usernames:
        key, value = user, False
        user_assigned[key] = value

    #Initialize the teams array with making teams of 1 member each
    team_size_1 = list(itertools.permutations(usernames,1))
    for team in team_size_1:
        teams.append(team)

    for team in teams:
        key, value = team, total_time(dict,team,k,m,n)
        grading_time[key] = value

    total_grading_time = 0
    final_teams = team_formation(dict,teams,grading_time)
    for team in final_teams:
        key, value = team, total_time(dict, team, k, m, n)
        grading_time[key] = value
        total_grading_time = total_grading_time + grading_time[team]
        display(team)
    print total_grading_time

#Function to display the output in the prescribed format
def display(team):
    for member in team:
        print member,
    print ""

#Function that forms teams
def team_formation(dict,teams,grading_time):
    final_teams = []
    new_team = ()
    #max_value = max(grading_time.iteritems(), key=operator.itemgetter(1))[0]    #https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    #sorted_grading_time = sorted(grading_time.items(), key=operator.itemgetter(1), reverse=True) #https://stackoverflow.com/questions/613183/how-to-sort-a-dictionary-by-value
    for user in user_assigned:
        flag = 'False'
        if not(user_assigned[user]):
            can_add = []
            members_wanted = dict[user][1].split(",")
            if (dict[user][1]=='_'):
                number_of_members_wanted = 0
            else:
                number_of_members_wanted = len(members_wanted)
            for i in range(0,min(2,number_of_members_wanted)):
                if not(user_assigned[members_wanted[i]]):
                    can_add.append(members_wanted[i])
                user_assigned[members_wanted[i]]='True'
            user_assigned[user]='True'
            new_team = new_team+tuple([user])+tuple(can_add)
            final_teams.append(new_team)
            new_team = ()

    answer = []
    combo_team = []
    count = 0
    final_teams.sort(lambda x, y: cmp(len(x), len(y)),reverse=True) #https://stackoverflow.com/questions/2587402/sorting-python-list-based-on-the-length-of-the-string
    for team in final_teams:
        count = count + 1
        if(len(combo_team)==3):
            answer.append(combo_team[0] + combo_team[1] + combo_team[2])
            del combo_team[:]
        if(len(team)<3):
            if(len(combo_team)<3):
                if (len(team) == 2):
                    answer.append(team)
                else:
                    combo_team.append(team)
                    if (count == len(final_teams)):
                        if (len(combo_team) == 1):
                            answer.append(combo_team[0])
                        else:
                            answer.append(combo_team[0] + combo_team[1])
            else:
                del combo_team[:]
        else:
            combo_team = []
            answer.append(team)

    return answer

#Function that calculates the total time required to grade the team
def total_time(dict,team,k,m,n):
    members = []
    no_of_complaint_emails = 0
    no_of_meetings = 0
    team_size_ambiguity = 0
    for i in range(len(team)):
        members.append(team[i])
    #print "Team:",team
    #print "Members:",members
    for member in members:
        members_wanted = dict[member][1].split(",")
        if(members_wanted[0]=='_'):
            no_of_complaint_emails = no_of_complaint_emails + 0
        else:
            #print "Intersection:",set(members).intersection(set(members_wanted))
            no_of_complaint_emails = no_of_complaint_emails + len(members_wanted)-len(set(members).intersection(set(members_wanted)))
    #print "No of complaint emails:",no_of_complaint_emails
    for member in members:
        members_unwanted = dict[member][2].split(",")
        if(members_unwanted[0]=='_'):
            no_of_meetings = no_of_meetings + 0
        else:
            no_of_meetings = no_of_meetings + len(set(members).intersection(set(members_unwanted)))
    #print "No of meetings:",no_of_meetings
    for member in members:
        team_size = int(dict[member][0])
        if(team_size==0):
            team_size_ambiguity = team_size_ambiguity + 0
        elif(team_size!=len(members)):
            team_size_ambiguity = team_size_ambiguity + 1
    #print "Team size ambiguity:",team_size_ambiguity
    grading_time = k+team_size_ambiguity+(n*no_of_complaint_emails)+(m*no_of_meetings)
    #print "Grading Time:",grading_time
    return grading_time

dict = {}
username_list = []
team_size_pref = []
members_wanted = []
members_unwanted = []
time = 0
grading_time = {}
user_assigned = {}
usernames = []
readFileDict(dict)
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
usernames_list(dict, k, m, n)

