import os
import sys
import git
from git import Repo
from collections import OrderedDict 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Creates a map of the suggested paths. Key=path, Value=environment_type
def createSuggestedPathList():
    env_work = "Work-Laptop"
    env_personal_desktop = "Personal-Desktop"
    env_personal_devbox = "Personal-Devbox"
    pathMap = OrderedDict([
        ("/sample/repository/folder/Python-Projects/", env_work), 
        ("/sample/repository/folder/Java-Projects/", env_personal_desktop),
        ("/sample/repository/folder/Android-Projects/", env_personal_devbox) 
    ])
    return pathMap


# Prints a space in the console
def printSpace():
    print("\n")


# Lists out the different pre-chosen paths, and prompts for a choice (or to enter a different path alltogether)
def promptForLocation():
    rootLocation = ""
    location_list = createSuggestedPathList()
    print(bcolors.HEADER, "Choose from common destionations, or enter your path manually:", bcolors.ENDC)
    
    # List all of the path options - formatted with colors / type
    index = 0
    for location, locationType in location_list.items():
        print(bcolors.WARNING, str(index+1) + ": " + bcolors.ENDC, "(" + locationType + ") " + location)
        index+= 1

    userInput = input(bcolors.HEADER + " Your choice: " + bcolors.ENDC)
    userInputInt = int(userInput) - 1
    if(userInputInt >= 0 and userInputInt <= (len(location_list)-1)):
        # Use pre-selected path location
        rootLocation = list(location_list.keys())[userInputInt]
    else:
        # Use whatever path the user typed in as input
        rootLocation = userInput
    return rootLocation


# Ask if the user wants GitUpdated to automatically ff branches when possible
def promptForFF():
    userInput = input(bcolors.HEADER + " Automatically fast forward branches when possible? (y/n): " + bcolors.ENDC).lower()
    if(userInput == "y" or userInput == "Y" or userInput == "yes" or userInput == "YES" or userInput == "YEAH"):
        return True
    else:
        return False


def printRepo(repo, repoLocation, shouldFF):
    repoPath = str(repo).split("/")
    repoName = repoPath[len(repoPath)-2] + ".git"
    print (bcolors.OKBLUE + "Repository Name: ",repoName, bcolors.ENDC)
    print (repoLocation)
    
    url = getRepositoryUrl(repo)
    print (url)
    # Fetch update each remote in the repo
    print ("# Remotes: ", len(repo.remotes))
    for remote in repo.remotes:
        remote.fetch()

    branches, anyBranchBehind = listBranches(repo, url)
    printUncommittedChanges(repo)

    # Only FF if a) user said yes, and b) if any branch is behind HEAD
    if(shouldFF and anyBranchBehind==True):
        print("Now fast-forwarding", len(branches) ,"branches in this repository:")
        updateBranches(repo, branches)
        printSpace()
    # If the shouldFF flag is on, but none of the branches are behind, then no need to FF.
    elif (shouldFF and anyBranchBehind==False):
        print("No need to fast-forward. No branches are behind in this repository.")
        printSpace()


def updateBranches(repo, branches):
    git = repo.git
    result = ""
    for branch in branches:
        try:    
            result = git.pull('origin', branch, "--ff-only")
            print("\t" + bcolors.HEADER, str(branch).strip(),bcolors.ENDC, "pulled: " + result)
        except Exception as e:
            message = e.stderr
            if ("Couldn't find remote ref" in message):
                # Local branch only, this branch DNE in remote repository
                print("\t" + bcolors.HEADER, str(branch).strip() + ":",bcolors.ENDC, bcolors.FAIL, "Couldn't find remote ref.", bcolors.ENDC)
            else:
                # Some other kind of issue. Use more generic message for debugging.
                print("\t", bcolors.FAIL, "There was a problem fast-forwarding ", str(branch), ": ", e, bcolors.ENDC)


def printUncommittedChanges(repo):
    uncommitted = repo.is_dirty()
    if uncommitted:
        # Current repository has uncommitted changes... retrieve a list of changed files
        changed_files = [item.a_path for item in repo.index.diff(None) ]
        print ([len(changed_files)] , "Modified Files:")
        for x in changed_files:
            # Just print out each changed file
            print (bcolors.FAIL + '\t',x + bcolors.ENDC)
        
        # Print "untracked" files
        untracked_files = repo.untracked_files

        if(len(untracked_files) > 0):
            print ([len(untracked_files)] , "Untracked Files:")
            for x in untracked_files:
                # Just print out each changed file
                print (bcolors.FAIL + '\t',x + bcolors.ENDC)
        else:
            print ("[0] Untracked Files.")
    else:
        print ("[0] Uncommitted changes." + bcolors.OKGREEN + "\n\tRepository is clean." + bcolors.ENDC)
    printSpace()
        

def getRepositoryUrl(repo):
    git = repo.git
    # Command to get URL for repository: (your_remote)
    # git config --get remote.origin.url
    remoteUrl = git.config('--get', 'remote.origin.url')
    return remoteUrl


# Git commands used for this:
    # git remote show origin | grep "HEAD branch" | cut -d ":" -f 2
    # git remote show https://github.com/ricemitc/Public-GitUpdated.git
# Gets the default branch of the current repository. 
def getDefaultBranch(repo, url):
    git = repo.git
    defaultBranchInfo = git.remote('show', url).split("\n")
    defaultBranch = ""
    for info in defaultBranchInfo:
        if("HEAD branch" in info):
            defaultBranch = info.split(':')[1].strip()
            break
    if(defaultBranch == ""):
        defaultBranch = "master"
    # print("defaultBranch:", defaultBranch)
    return defaultBranch
    

# Prints out all of the branches in the repository, along with how far ahead/behind they are to the HEAD branch
def listBranches(repo, url):
    anyBranchBehind = False
    branchList = repo.branches
    defaultBranch = getDefaultBranch(repo, url)

    print ([len(branchList)] , "Branches:")
    for branch in branchList:
        branchDiffModifier = "origin/" + defaultBranch + "..." + str(branch)
        output = repo.git.rev_list('--left-right', '--count', branchDiffModifier).split()
    
        behind = output[0]
        ahead = output[1]
        behindLabel = ("-" + behind) if behind == "0" else (bcolors.WARNING + "-" + behind + bcolors.ENDC)
        aheadLabel = ("+" + ahead) if ahead == "0" else (bcolors.OKGREEN + "+" + ahead + bcolors.ENDC)
        commitDifLabel = "[" + behindLabel + "\t" + aheadLabel + " to origin/master]"

        if behind != "0":
            anyBranchBehind = True
        if repo.active_branch == branch:
            print ("\t", commitDifLabel, "\t", bcolors.HEADER, branch, bcolors.ENDC, bcolors.WARNING, "(*)", bcolors.ENDC)
        else:
            print ("\t", commitDifLabel, "\t", bcolors.HEADER, branch, bcolors.ENDC)
    return branchList, anyBranchBehind;    
