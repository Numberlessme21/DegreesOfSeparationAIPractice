import csv
# Maps personIds to a dictionary of: name, birth, movies (a set of movieIds)
people = {}

# Maps movieIds to a dictionary of: title, year, stars (a set of personIds)
movies = {}


def loadData(directory):
    """
    Load data from CSV files into memory.
    """
    peopleList = []
    movieList = []
    with open(f'{directory}/movies.csv', mode='r', encoding='utf8') as m:
        mo = csv.reader(m, delimiter=',')
        for i in mo:
            movieList.append(i)    
    with open(directory+"/people.csv", mode='r', encoding='utf8') as p:
        pe = csv.reader(p, delimiter=',')
        for i in pe:
            peopleList.append(i)
    for i in peopleList:
        people[str(i[0])] = {'name':i[1].strip(), 'movies':[]}
    for i in movieList:
        movies[str(i[0])] = {'title':i[1].strip(), 'stars':[]}
    with open(directory+"/stars.csv", mode='r', encoding='utf8') as s:
        st = csv.reader(s, delimiter=',')
        for i in st:
            try:
                people[i[0].strip()]['movies'].append(i[1].strip())
            except:
                people[i[0].strip()] = {'movies':i[1].strip()}
            try:
                movies[i[1].strip()]['stars'].append(i[0].strip())
            except:
                movies[i[1].strip()] = {'stars':i[0].strip()}
    return None

def main():
    startBool = True
    while startBool:
        start = personIdForName(input('Enter the first person: '))
        if start in people.keys():
            startBool = False
        else:
            print('Not found')
    targetBool = True
    while targetBool:
        target = personIdForName(input('Enter the second person: '))
        if target in people.keys():
            targetBool = False
        else:
            print('Not found')
    degrees = shortestPath(start,target)
    if degrees == None:
        print('No link')
    else:
        if len(degrees) == 2:
            print(len(degrees)-1, 'degree of separation')
        else:
            print(len(degrees)-1, 'degrees of separation')
        for i in range(1,len(degrees)):
            print(people[degrees[i-1][1]]['name'],'was in',movies[degrees[i][0]]['title'],'with',people[degrees[i][1]]['name'])

def shortestPath(source, target):
    """
    Returns the shortest list of (movieId, personId) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    past = []
    pastids = []
    frontier = []
    frontierids = []
    found = False
    class node():
        def __init__(self, id, parent, film):
            self.id = id
            self.parent = parent
            self.actions = self.actions()
            self.film = film
        def actions(self):
            actions = []
            actions = list(people[self.id]['movies'])
            return actions
        def children(self):
            past.append(self.id)
            for i in self.actions:
                stars = movies[i]['stars']
                for j in stars:
                    n = node(j, self,i)
                    if not (n in past):
                        frontier.append(n)   
                        frontierids.append(n.id)
    n = node(source, None, None)
    frontier.append(n)
    frontierids.append(n.id)
    count = 1
    while True:
        count +=1
        try:
            if not (frontierids[0] in pastids):
                if frontier[0].id == target:
                    connection = []
                    n = frontier[0]
                    while n.parent != None:
                        connection.insert(0,(n.film, n.id))
                        n = n.parent
                    connection.insert(0, (None,source))
                    return connection
                frontier[0].children()
                past.append(frontier[0])
                pastids.append(frontier[0].id)
        except:
            return None
        frontier.pop(0)
        frontierids.pop(0)


def personIdForName(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    names = []
    ids = []
    keys = list(people.keys())
    for i in keys:
        try:
            names.append(people[i]['name'])
        except:
            pass
    keys = list(keys)
    for i in range(names.count(name)):
        x = names.index(name)
        ids.append(keys[x])
        names.pop(x)
        keys.pop(x)
    if len(ids) == 1:
        return ids[0]
    elif len(ids) == 0:
        return None
    else:
        print('Which \''+name+'\'?')
        while True:
            for i in range(len(ids)):
                print('ID: '+ids[i]+', Name: '+name)
            inp = input('Intended Person ID: ')
            if inp in ids:
                return inp



directory = 'large'

    # Load data from files into memory
print("Loading data...")
loadData(directory)
print("Data loaded.")
runAgain = True        
while runAgain:
    main()
    i = input('Would you like to play again (y/n)? ')
    authError = True
    while authError:
        if i == 'y':
           authError = False
        elif i == 'n':
            runAgain = False
            authError = False
        else:
            print('Didn\'t understand input')
            authError = True
