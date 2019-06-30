from gitupdated import *

def main():
    rootLocation = ""
    argLength = len(sys.argv)
    if(len(sys.argv) > 1):
        # Check argument length. If path specified as argument, use that
        rootLocation = sys.argv[1]
    else:
        # Else, prompt user for root folder location
        rootLocation = promptForLocation()

    shouldFF = promptForFF()
    print(bcolors.HEADER, "Root file location is: ", bcolors.ENDC, rootLocation)
    printSpace()

    try:
        folderList = os.listdir(rootLocation)
        for folder in folderList:
            currentLocation = rootLocation + folder
            try:
                repo = git.Repo(currentLocation)
                assert not repo.bare
                printRepo(repo, currentLocation, shouldFF)
            except git.exc.NoSuchPathError as exception:
                continue
                # print("NoSuchPathError: ", exception)
                # printSpace()
            except git.exc.InvalidGitRepositoryError as exception:
                continue
                # print("InvalidGitRepositoryError: ", exception)
                # printSpace()    
    except FileNotFoundError as exception:
        print(bcolors.FAIL + "File location: \"" + rootLocation + "\" not valid. Please try again." + bcolors.ENDC)


# Call the main method and run GitUpdated
main()