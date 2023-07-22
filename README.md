##What is this project?
A hunter of hard drive space. It finds files that are needlessly duplicated 
    and takes action.

##Who is it for?
People with a disorganized collection of files, that would like to organize 
    them but don't want to spend their time searching through endless 
    folders.

##: Getting Started :
This project currently has no dependencies except Python and the Linux 
    operating system, I haven't tested it against multiple versions, but 
    I would expect it to run on anything above Python3.7.

Here are the steps to run it on a new computer.

###Requirements
1. Python3.7+
2. A Linux Operating System

#Warning
Do not point this at important operating system files, it will identify
    duplicates in those files and relocate them to the staging/un-staging
    area respectively. This would be bad for the health of your operating
    system.

###Steps to First-Time Run
Note that while archive name can be any valid string in Python3, the paths
that you set should already exist. The archive/source paths should contain 
files, and the graveyard/stage/un-staging paths should be empty.
1. Clone the repository
2. Create your virtual environment and activate it
3. Open the ./config/config.py and do the following :
    1. Set your archive_name, it will be located :
        1. config[Archives][archive_name]
    2. If you intend to evaluate an archive
       2. Set at least these two paths :
          1. The archive path, located :
             1. config[Archives][archive_name] = archive_path
          2. The un-staging path, located :
             1. config[Archives][archive_name] = un_staging_path
    3. If you intend to evaluate a source
       1. Set at least these three paths :
           1. The graveyard path, located :
               1. config[Archives][archive_name] = graveyard_path
           2. The source path, located :
               1. config[Archives][archive_name] = source_path
           3. The staging area, located :
               1. config[Archives][archive_name] = staging_path

### Program Flow
1. TODO 

### Project Structure and Module Breakdown
1. TODO

