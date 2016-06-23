from content.models import Category
from library.models import Library

def get_catchain(t):
    ts = [t.name]
    while t.parent:
        ts.insert(0, t.parent.name)
        t = t.parent
    return ts

def get_categories():
    cats = Category.objects.all()
    #heads = []
    #for c in cats:
    #    if not c.parent:
    #        heads.append(c)            
    tails = []
    for c in cats:
        isLeaf = True
        for c1 in cats:
           if c1.parent == c:
               isLeaf = False
               break
        if isLeaf:
            tails.append(c)
    all_ts = {}
    for t in tails:
        ts = get_catchain(t)
        all_ts['->'.join(ts)] = t.id
    return sorted(all_ts.items())
    
def save_chunk(category,chunk):
    if len(chunk)>=3:
	title=chunk[0]
	author=chunk[1]
	body='\n'.join(chunk[2:])

        article = Article.objects.get_or_create(
                category = category,
                author = author,
                title = title,
                body = body
            )
        return 0
    return -1

def get_libchain(t):
    ts = [t.name]
    while t.parent:
        ts.insert(0, t.parent.name)
        t = t.parent
    return ts

def get_libraries(type):
    libs = Library.objects.filter(type=type)
    #heads = []
    #for c in libs:
    #    if not c.parent:
    #        heads.append(c)            
    tails = []
    for c in libs:
        isLeaf = True
        for c1 in libs:
           if c1.parent == c:
               isLeaf = False
               break
        if isLeaf:
            tails.append(c)
    all_ts = {}
    for t in tails:
        ts = get_libchain(t)
        all_ts['->'.join(ts)] = t.id
    return sorted(all_ts.items())

