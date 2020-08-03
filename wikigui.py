import PySimpleGUI as sg
import random
import wikipediaapi
import wikipedia

# The depth of this is just 1. I think this is better for vizualization.
def SubCategories(categorymembers): 
    subcategories = dict()
    for c in categorymembers:
        if categorymembers[c].ns == 14:
            subcategories[c] = categorymembers[c]
    return subcategories

def Titles(categorymembers):
    titles = []
    for c in categorymembers:
        title = categorymembers[c].title
        if title.startswith("Category:"):
            title = title[9:]
        titles.append(title)
    return titles

def RandomArticle(categorymembers):
    subarticles = dict()
    for c in categorymembers:
        if categorymembers[c].ns == 0:
            subarticles[c] = categorymembers[c]
    subarticles = list(subarticles.values())
    return (random.choice(subarticles)).title

category_list_column = [
    [
        sg.Text("Category"),
        sg.In(size=(25, 1), enable_events=True, key="-CATEGORY-"),
        #sg.FolderBrowse(),
        sg.Button("Get")
    ],
    [
        sg.Text(size=(40, 1), key="-CURRENT-")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-SUBCAT LIST-"
        )
    ],
    [
        sg.Button("Random Article"),
        sg.Button("Go Back")
    ]
]


text_viewer_column = [
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Text(size=(40, 24), key="-DESCRIPTION-")],
    [sg.Text("Full article: ")],
    [sg.Text(size=(40,1), key="-LINK-")]
]

layout = [
    [
        sg.Column(category_list_column),
        sg.VSeperator(),
        sg.Column(text_viewer_column),
    ]
]

window = sg.Window("Random Wikipedia Article", layout)
wiki_wiki = wikipediaapi.Wikipedia('en')

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Get":
            mycat = [values["-CATEGORY-"]]
            ourpath = mycat[0]
            
            try:
                mycat = wiki_wiki.page("Category:" + mycat[0])
            except:
                mycat = wiki_wiki.page("Category:Physics")    
            fnames = Titles(SubCategories(mycat.categorymembers))
            
            window["-CURRENT-"].update(ourpath)
            window["-SUBCAT LIST-"].update(fnames)
            
    elif event == "-SUBCAT LIST-":
        mycat = values["-SUBCAT LIST-"]
        ourpath = ourpath + ": " + mycat[0]
        
        window["-CURRENT-"].update(ourpath)
        
        newcat = wiki_wiki.page("Category:" + mycat[0])
        fnames = Titles(SubCategories(newcat.categorymembers))
        window["-SUBCAT LIST-"].update(fnames)
    
    elif event == "Go Back":
        try:
            ourpath = ourpath.split(": ")
            ourpath = ourpath[:-1]
            mycat = ourpath[-1]
            ourpath = ": ".join(ourpath)
            mycat = wiki_wiki.page("Category:" + mycat)
            fnames = Titles(SubCategories(mycat.categorymembers))
            
            window["-CURRENT-"].update(ourpath)
            window["-SUBCAT LIST-"].update(fnames)
        except:
            None
    
    elif event == "Random Article":
        try:
            newpath = ourpath.split(": ")
            newpath = newpath[:-1]
            mycat = newpath[-1]
            mycat = wiki_wiki.page("Category:" + mycat)
            title = RandomArticle(mycat.categorymembers)
            
            window["-TOUT-"].update(title)
            article = wikipedia.page(title)
            window['-DESCRIPTION-'].update(article.content)
            
            link = "http://en.wikipedia.org/?curid="
            link = link + str(article.pageid)
            window["-LINK-"].update(link)
            
        except:
            try:
                title = RandomArticle(mycat.categorymembers)
                window["-TOUT-"].update(title)
                article = wikipedia.page(title)
                window['-DESCRIPTION-'].update(article.content)
                
                link = "http://en.wikipedia.org/?curid="
                link = link + str(article.pageid)
                window["-LINK-"].update(link)
            except:
                None
                
window.close()
