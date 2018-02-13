from sys import argv

if __name__ == '__main__':
    fname = 'term_menu.pickle'

    if not os.path.isfile(fname):
        print(fname, "does not exist in current directiory.")
        return

    with open(fname, 'rb') as pfile:
        foods = pickle.load(pfile)
