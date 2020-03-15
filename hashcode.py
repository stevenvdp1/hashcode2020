import math
import time
import itertools
from operator import itemgetter, methodcaller

fileNames = [
    # 'a_example.txt',
    # 'b_read_on.txt',
    # 'c_incunabula.txt',
    # 'd_tough_choices.txt',
    'e_so_many_books.txt',
    # 'f_libraries_of_the_world.txt'
]

def main(fileName):
    print('starting:', fileName)
    
    (total_days, libraries) = readConfig(fileName)

    signed_libraries = []
    day = 0

    start = time.time()
    # print(libraries)
    while len(libraries)>0:
        if(len(libraries)%100==0):
            print(len(libraries),time.time()-start)
        best_library_index = sorted(libraries, key=lambda x: (libraries[x][1]))[0]
        # best_library_index = sorted(libraries, key=lambda x: (-getLibraryScore(total_days,day,libraries[x]), getLibraryIdleTime(total_days,day,libraries[x])))[0]
        # best_library_index = max(libraries, key=lambda x: getLibraryScore(total_days, day, libraries[x]))
        best_library = libraries.pop(best_library_index)
        (books_in_library, signup_days, books_per_day, book_dict) = best_library

        if(day+signup_days<=total_days):
            if(day + signup_days + len(book_dict)/books_per_day > total_days):
                amount_of_books = int((total_days-signup_days-day)/books_per_day)
                book_dict = dict(itertools.islice(book_dict.items(), amount_of_books))
            if(len(book_dict)>0):
                signed_libraries.append([best_library_index, book_dict.keys()])
                for lib in libraries.values():
                    [lib[-1].pop(key, None) for key in book_dict]
                day += signup_days
                if(day>=total_days):
                    break

    generateOutput(fileName, signed_libraries)


def score(total_days, day, library):
    return sum()


def getLibraryScore(total_days, day, library):
    (books_in_library, signup_days, books_per_day, book_dict) = library

    library_score = 0
    if(day+signup_days<=total_days):
        if(day+signup_days+len(book_dict)/books_per_day > total_days):
            amount_of_books = int((total_days-signup_days-day)/books_per_day)
            best_books = dict(itertools.islice(book_dict.items(), amount_of_books))
            library_score= sum(best_books.values())
        else:
            library_score = sum(book_dict.values())
    
    return (library_score*(total_days-(day+signup_days)))/signup_days

def getLibraryIdleTime(total_days, day, library):
    (books_in_library, signup_days, books_per_day, book_dict) = library
    return (total_days - day - signup_days - len(book_dict)/books_per_day)

def readConfig(fileName):
    with open('./in/'+fileName) as f:
        line1 = f.readline().rstrip('\n').split(' ')
        line1 = list(map(int,line1))
        (total_books, total_libraries, total_days) = line1

        book_scores = f.readline().rstrip('\n').split(' ')
        book_scores = list(map(int,book_scores))

        libraries = dict()
        for i in range(0, total_libraries):
            #set library index at pos[0]
            library = []

            #append library with config
            library_config = f.readline().rstrip('\n').split(' ')
            library_config = list(map(int,library_config))
            library = library + library_config

            #append library with booklist
            library_books = f.readline().rstrip('\n').split(' ')
            library_books = set(map(int,library_books))
            library_books = {element:book_scores[element] for element in library_books}
            library_books = {k: v for k, v in sorted(library_books.items(), key=lambda item: item[1], reverse=True)}
            library.append(library_books)

            libraries[i]=(library)
        
    return (total_days, libraries)

def generateOutput(file, signed_libraries):
    with open('./out/'+file, 'w') as f:
        print(len(signed_libraries), file=f)
        for library in signed_libraries:
            (index, books) = library
            print(index, len(books), file=f)
            for book in books:
                print(book, file=f, end=' ')
            print('', file=f)

if __name__ =="__main__":
    start = time.time()
    for fileName in fileNames:
        main(fileName)
    print('Completed all files in: ', time.time() - start)