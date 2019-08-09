# Public-GitUpdated

GitUpdated: A Python script for easily managing, updating, and checking the status of multiple git repos at once. 

This project is part of my Side Project Time Hack series on my blog at:
    https://mnmapplications.com/blog-posts/

Read along with the blog post here:
    https://mnmapplications.com/2019/07/19/gitupdated-automating-git-repository-maintenance/


![GitUpdated Demo](https://i1.wp.com/mnmapplications.com/wp-content/uploads/2019/07/GitUpdated-Demo.gif?zoom=2&resize=600%2C600&ssl=1)


I frequently switch between different machines to work, and I find it tedious to constantly call commands like "git status" on each repository I have checked out to make sure everything is synced. I also didn't need a full fledged out of the box repository manager, so I decided to just build my own CLI tool with Python.

The main information I want to know about each project are:

- Repository name
- Folder location
- Number of local branches, and for each branch:
    - Number of commits ahead is it from the default branch
    - Number of commits behind is it from the default branch
    - Branch name
    - Whether the branch is currently checked out
- Repository status which can be either:
    - “Clean” (no changed files, no new files)
    - “Dirty”- and if so:
        - Number of modified files (+ names)
        - Number of untracked files (+ names)

Here is a sample snippet of GitUpdated's output when run on one of my Android apps:

![GitUpdated Sample Output](https://i0.wp.com/mnmapplications.com/wp-content/uploads/2019/07/GitUpdated-Example-Output.png?w=1010&ssl=1)



Required to Run:
    - Python3
    - Pip
    - GitPython 
        If you're on MacOS Mojave, you'll also need Xcode developer tools:
            - xcode-select --install