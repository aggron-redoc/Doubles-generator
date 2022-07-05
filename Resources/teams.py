import random
import time

random.seed(time.perf_counter())
'''
This class contains all the methods for applying the appropriate backend services. eg. randomize, add player, delete player etc.
Main concept used in the development of these services: Adjacency matrix and bit manipulation
particpants list for storing the name list of all the participants
Each player is indicated by a number and each bit in the number indicates whether they have partnered with the corresponding person or not
The above format followed for data members: manipulate, reset_to <fallback state when all combinations are exhausted or new combination couldnt be arrived on>,
check_matrix <for checking whether all combinations are exhausted. Here all bits(wrt to no. of participants) will be set except the bit of the participant themselves(wrt to the index of the participant)
For odd number of players, a new dummy entity pairing is introduced for even pairing, allowing us to use the same algorithm and making the code robust
The presence of the same in the participants list is indicated by boolean value pairing.
manipulate is the class which stores the actual state after each possible action mentioned above
'''
'''
why bit manipulation? Instead of using an integer for each and every pair, having only one integer per player and using the bits inside the number saves storage
what is better? having a boolean value for each and every pair in terms of space complexity
why prefer the former?
This is a migration process wherein, I have updated from my previous file manipulation approach and it also used bit manipulation
bit manipulation is faster and the state storing matrices are easily represented as integer lists, hence construction is faster and codebase is smaller(no nested loops) and hence, time complexity is less
'''

#pairing issue corner case on adding and deleting
class Teams:
    def __setCheckMatrix(self):
        each_row_bitwise_indicator = ((1 << len(self.participants)) - 1)
        check_matrix = []
        for i in range(len(self.participants)):
            temp = each_row_bitwise_indicator ^ (1 << i)
            check_matrix.append(temp)
        self.check_matrix = check_matrix

    def __init__(self, participants, manipulate=[], coupling=[]):
        self.participants = participants
        self.pairing = False

        no_of_participants = len(participants)
        if no_of_participants % 2 == 1:
            self.participants.append('pairing')
            self.pairing = True
            no_of_participants += 1
        main_matrix = [0] * no_of_participants

        self.reset_to = main_matrix[:]
        if manipulate == []:
            self.manipulate = main_matrix[:]
            self.coupling = []
        else:
            self.manipulate = manipulate[:]
            self.coupling = coupling[:]

        self.__setCheckMatrix()

#Tournament Planner spits out the order of matches between teams after the teams have been obtained from saaBooThree
#Only order of the teams are changed. Eg. [1,2,3,4,5] are the teams and the randomized results are [3,4,1,2,5], then 3 and 4 first match, 1 and 2 second match and so on, and the last one is bye. The teams should be pretty formatted and sent in the block where this method is called

    def __TournamentPlanner(self, teamlist):
        random.shuffle(teamlist)
        teamlist = [[self.participants[team[0]], self.participants[team[1]]]
                    for team in teamlist]
        return teamlist

# Formation of teams based on previous teams formed and constrained randomization (constraints based on previous teams formed) pairs are generated in this method
# Simple Idea: pick 2 players, check in manipulate if already been a team, if so, put them back into the list, try again, else update the matrix, remove them from the list permanently(list refers to temporary list used in the method for keeping track of peeps who havent formed pairs yet)

    def __Saa_boo_Three(self, checkmatrix, pno, fteamlist):
        teamlist = fteamlist[:]
        length = len(pno)
        for i in range((length * (length - 1)) * 4):
            j = 0
            while pno != [] and j < (length * (length - 1) * 4):
                p1 = random.choice(pno)
                pno.remove(p1)
                p2 = random.choice(pno)
                pno.remove(p2)
                if (checkmatrix[p1] & (1 << p2) == 1 << p2):
                    if (pno == []):
                        for team in teamlist:
                            pno.append(team[0])
                            pno.append(team[1])
                        teamlist = []
                        checkmatrix = self.manipulate[:]
                    pno.append(p1)
                    pno.append(p2)
                else:
                    teamlist.append([p1, p2])
                    checkmatrix[p1] |= 1 << p2
                    checkmatrix[p2] |= 1 << p1
                j += 1
            if (pno == []):
                break
        else:
            return False, []
        fteamlist = teamlist[:]
        self.manipulate = checkmatrix[:]
        return True, fteamlist

    # Calls saaBooThree and returns the generated teams with matchups
    def randomizer(self):
        #The following loop is for checking whether all combinations are exhausted
        for i in range(len(self.participants)):
            if self.manipulate[i] == self.check_matrix[i]:
                self.manipulate = self.reset_to[:]
                break
        else:
            teamlist = []
            pno = list(range(len(self.participants)))
            checkmatrix = self.manipulate[:]
            result = self.__Saa_boo_Three(checkmatrix, pno, teamlist)
            if (result[0] == True):
                teamlist = result[1]
                return self.__TournamentPlanner(teamlist)
            else:
                return []

    def Clear(self):
        self.manipulate = self.reset_to[:]
        self.coupling = [0] * len(self.manipulate)

#spits out the current single status of each player in the form of a single number(matching format of `manipulate`)

    def __SingleStatus(self, l):
        status = 0
        for i in range(len(l)):
            status |= l[i] << i
        return status
#Updating status of pairing i.e those people who have been single in case of odd number of players and pairing dummy into the participants list

    def __SingleStatusUpdater(self, add=False):
        if (self.coupling == []):
            coupling = [0] * len(self.manipulate)
            self.coupling = coupling[:]
        self.participants.append('pairing')
        self.pairing = True
        for i in range(len(self.manipulate)):
            self.manipulate[i] |= (self.coupling[i] <<
                                   (len(self.participants) - 1))
        if (add):
            self.manipulate.append(0)
        self.manipulate.append(self.__SingleStatus(self.coupling))

#private method for updating resetTo and checkmatrix lists after any addition or removal operations

    def __setResetAndCheck(self):
        self.reset_to = [0] * len(self.participants)
        self.__setCheckMatrix()

#pairing comes into play when it comes to add and remove. pairing true means, on adding or removing even no. of participants are obtained and vice versa, so set pairing

    def add(self, player):
        if self.pairing == True:
            self.coupling = []
            for i in range(len(self.participants)):
                self.coupling.append(self.manipulate[i] >>
                                     (len(self.participants) - 1))
                self.manipulate[i] &= ((1 << (len(self.participants) - 1)) - 1)
            self.coupling.append(0)
            self.pairing = False
            self.manipulate[-1] = 0
            self.participants[-1] = player
        else:
            self.participants.append(player)
            self.__SingleStatusUpdater(add=True)
        self.__setResetAndCheck()


#get lssmask and mssmask, so get the info for a particular player wrt their pairing history and remove the history of one particular player alone. step of finer granularity in remove process

    def __removeFromMatrix(self, x, y):
        leastSignificantSideMask = (1 << x) - 1
        mostSignificantSideMask = (1 << (len(self.manipulate) - 1 - x))
        mostSignificantSideMask <<= (x + 1)
        leastSignificantSide = y & leastSignificantSideMask
        mostSignificantSide = y & mostSignificantSideMask
        return leastSignificantSide | mostSignificantSide

    def remove(self, player):
        plTbRemoved = self.participants.index(player)
        if (self.pairing == True):
            self.coupling = []
            for i in range(len(self.participants)):
                self.coupling.append(self.manipulate[i] >>
                                     (len(self.participants) - 1))
                self.manipulate[i] &= ((1 << (len(self.participants) - 1)) - 1)
                self.manipulate[i] = self.__removeFromMatrix(
                    plTbRemoved, self.manipulate[i])
            self.coupling.pop(plTbRemoved)
            self.participants.pop(plTbRemoved)
            self.participants.pop(-1)
            self.manipulate.pop(plTbRemoved)
            self.manipulate.pop(-1)
            self.pairing = False

        else:
            self.__SingleStatusUpdater()
            for i in range(len(self.participants)):
                self.manipulate[i] = self.__removeFromMatrix(
                    plTbRemoved, self.manipulate[i])
            self.participants.pop(plTbRemoved)
            self.manipulate.pop(plTbRemoved)
        self.__setResetAndCheck()
