import math
import time

fileNames = [
    'a_example.txt',
    'b_read_on.txt',
    'c_incunabula.txt',
    'd_tough_choices.txt',
    'e_so_many_books.txt',
    'f_libraries_of_the_world.txt'
]

def main(file):
    print('starting:', file)
    (total_books, total_libraries, tot_days, book_scores, libraries) = readConfig(file)
    #Every library looks like --> [index, books_in_libray, signup_days, books_per_day, [bookArray]]
    libraries = sortLibrariesBySignup(libraries)
    signed_libraries = []
    used_books = set()
    day = 0

    for library in libraries:
        (library_index, books_in_libray, signup_days, books_per_day, bookArray) = library
        if(day + signup_days < tot_days):
            # libraries that can be fully scanned
            if(day+daysToScanAllBooks(books_in_libray, signup_days, books_per_day) < tot_days):
                day = day + signup_days
                signed_libraries.append([library_index, bookArray])
                used_books.update(bookArray)
            else:
                amount_to_select = (tot_days-signup_days)*books_per_day
                books_with_score = []
                for book in bookArray:
                    if(book not in used_books):
                        books_with_score.append([book,book_scores[book]])
                books_with_score = sorted(books_with_score, key=lambda x: x[1], reverse=True)
                books_with_score = books_with_score[:amount_to_select]
                selected_books = []
                for book in books_with_score:
                    selected_books.append(book[0])
                    used_books.add(book[0])
                if(len(selected_books)>0):
                    signed_libraries.append([library_index,selected_books])
                    day = day + signup_days

    generateOutput(file, signed_libraries)

    print('completed:', file)



def readConfig(file):
    with open('./in/'+file) as f:
        line1 = f.readline().rstrip('\n').split(' ')
        line1 = list(map(int,line1))
        (total_books, total_libraries, tot_days) = line1

        book_scores = f.readline().rstrip('\n').split(' ')
        book_scores = list(map(int,book_scores))

        #array of libraries
        #[index, books_in_library, signup_days, books_per_day, [bookArray]]
        libraries = []
        for i in range(0, total_libraries):
            #set library index at pos[0]
            library = []
            library.append(i)

            #append library with config
            library_config = f.readline().rstrip('\n').split(' ')
            library_config = list(map(int,library_config))
            library = library + library_config

            #append library with booklist
            library_books = f.readline().rstrip('\n').split(' ')
            library_books = list(map(int,library_books))
            library.append(library_books)

            libraries.append(library)

    return (total_books,total_libraries,tot_days, book_scores, libraries)

def sortLibrariesBySignup(libraries):
    return sorted(libraries, key=lambda x:x[2])

def daysToScanAllBooks(books_in_library, signup_days, books_per_day):
    return math.ceil(((books_in_library/books_per_day)+signup_days))

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
    for file in fileNames:
        main(file)
    print('Completed all files in: ', time.time() - start)