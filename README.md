### Installition

    pip install saika.path

### Usage

Example, how to delete .pyc files in a project (use Unix globbing)

    import saika.path
    
    folder = saika.path.Folder('e:/project'):
    for pyc in folder.allfiles(name='*.pyc'):
        pyc.delete()
    
`saika.path` also accepts a function

    def condition_size_lt_1024(file):
        return True if file.size < 1024 else False
        
    for pyc in folder.allfiles(name='*.pyc', key=condition_size_lt_1024):
        pyc.delete()
        
`saika.path` provides some command line tools to clean project cache files:

    saika.path.clean --type=python /home/mohanson
    
this deletes all *.pyc, *.egg-info, dist and other cache files
