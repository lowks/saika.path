### Installition

    pip install saika.path

### Usage

Example, How delete .pyc files in a project(use Unix globbing)

    import saika.path
    
    folder = saika.path.Folder('e:/project'):
    for pyc in folder.allfiles(name='*.pyc'):
        pyc.delete()
    
Also, it could accept a function

    def condition_size_lt_1024(file):
        return True if file.size < 1024 else False
        
    for pyc in folder.allfiles(name='*.pyc', key=condition_size_lt_1024):
        pyc.delete()
        
It provide some command line tools to clean project cache files:

    saika.path.clean --type=python /home/mohanson
    
this will delete all *.pyc, *.egg-info, dist and other cache files