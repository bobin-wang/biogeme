import os, shutil
import fileinput
import time
import fnmatch
import ast
import pathlib


urlbinder = ('https://mybinder.org/v2/gh/michelbierlaire/biogeme/master'
             '?filepath=')

urlnoto = ('https://noto.epfl.ch/hub/user-redirect/git-pull?'
           'repo=https://github.com/michelbierlaire/biogeme'
           '&urlpath=tree/biogeme/')

urlgithub = 'https://github.com/michelbierlaire/biogeme/blob/master/'


def replaceInFile(fileName, keyword, content):
    for line in fileinput.input(fileName, inplace=True):
        print(line.replace(keyword, content), end='')
    
def copyFile(name, dir='sources'):
    orig = f'{dir}/{name}'
    dest = f'website/{name}'
    shutil.copy(orig, dest)

def copyExample(name, dir, hfiles):
    notebook_fname = f'{name.split(".")[0]}.ipynb'
    destdir = f'website/examples/{dir}'
    orig = f'../examples/{dir}/{name}'
    dest = f'{destdir}/{name}'
    orig_notebook = f'../examples/{dir}/{notebook_fname}'
    dest_notebook = f'{destdir}/{notebook_fname}'
    if not os.path.exists(destdir):
        pathlib.Path(destdir).mkdir(parents=True, exist_ok=True)
    shutil.copy(orig, dest)
    shutil.copy(orig_notebook, dest_notebook)
    for h in hfiles:
        orig_html = f'../examples/{dir}/{h}'
        dest_html = f'{destdir}/{h}'
        shutil.copy(orig_html, dest_html)
    print(f'Copied to {dest}')

def generateMenu(items):
    file = 'sources/menu.html.orig' 
    f = open(file, 'w')
    print('<ul class="biomenu">',file=f)
    for ff, tt in items.items():
        print(f'<li class=\'biomenu\'><a class=\'{ff}ACTIVE\' href=\'{ff}.html\'>{tt}</a></li>',file=f)
    print('</ul>',file=f)
    f.close()

def generatePage(name):
    orig = f'sources/{name}.html.orig' 
    dest = f'website/{name}.html' 
    shutil.copy(orig, dest)
    menu = 'sources/menu.html.orig'
    menudata = open(menu, 'r').read()
    replaceInFile(dest, 'INCLUDEMENU', menudata)
    banner = 'sources/banner.html.orig'
    bannerdata = open(banner, 'r').read()
    replaceInFile(dest, 'BANNER', bannerdata)
    header = 'sources/header.html.orig'
    headerdata = open(header, 'r').read()
    replaceInFile(dest, 'HEADER', headerdata)
    footer = 'sources/footer.html.orig'
    footerdata = open(footer, 'r').read()
    replaceInFile(dest, 'FOOTER', footerdata)
    replaceInFile(dest, '__DATE', time.strftime('%c'))
    replaceInFile(dest, f'{name}ACTIVE', 'active')
    return


def generateAllPages(pages):
    for f in pages:
        generatePage(f)
    generateExamples()

    
# Save the current website just in case
shutil.rmtree('website.old', ignore_errors=True)
if (os.path.isdir('website')):
    os.rename('website', 'website.old')
os.mkdir('website')

#Copy the PythonBiogeme distribution
shutil.copytree('otherFiles/distrib', 'website/distrib')

#Copy the sphinx documentation
shutil.copytree('../sphinx/_build/html', 'website/sphinx')

imageFiles = ['pandasBiogemeLogo.png',
              'up-arrow.png',
              'github.png',
              'jupyter.png',
              'binder.png',
              'background.jpg',
              'youtube.png',
              'getacrobat.png',
              'pdf-icon.png',
              'dataIcon.png']

for f in imageFiles:
    copyFile(f, '/Users/michelbierlaire/GoogleDrive/webpages/images') 

cssFiles = ['biomenu.css', 'biopanel.css', 'biobacktotop.css']
for f in cssFiles:
    copyFile(f,'/Users/michelbierlaire/GoogleDrive/webpages/css') 

jsFiles = ['backtotop.js', 'os.js', 'menu.js']
for f in jsFiles:
    copyFile(f,'/Users/michelbierlaire/GoogleDrive/webpages/js')

def cleanDoc(doc):
    if doc is None:
        return ''
    doc = doc.replace(':author:', 'Author:')
    doc = doc.replace(':date:', 'Date:')
    doc = doc.replace('\n', '<br>')
    return doc

def tableOfContents(allExamples):
    result = ''
    result += '<div class="panel panel-default">'
    result += f'<div class="panel-heading">Categories of examples</div>'
    result += '<div class="panel-body">'
    result += '<p>The examples are grouped into the following categories:</p>'
    result += '<ul>'
    
    for i in allExamples:
        result += f'<li><a href="#{i[1]}">{i[0]}</a></li>'
    result += f'<li><a href="#jupyter">Modules illustrations</a></li>'
    result += '</ul>'
    result += '<p>For each example, you have access to the following resources:</p>'
    result += '<ul>'
    result += '<li>A short description extracted from the file comments.</li>'
    result += '<li>Click on the name of the <code>.py</code> file to access the source code.</li>'
    result += '<li>Click on <img src="github.png" height="30"> to see the notebook on Github.</li>'
    result += '<li>Click on <img src="jupyter.png" height="30"> to run the notebook on <a href="http://noto.epfl.ch">noto.epfl.ch</a> (registration required).</li>'
    result += '<li>Click on <img src="binder.png" height="30"> to run the notebook on <a href="http://mybinder.org">binder</a> (no registration required).</li>'
    result += '<li>When available, estimation results are available in one or several html files.</li>'
    result += '</ul>'
    result += '</div>'
    result += '<div class="panel-footer">'
    result += 'Download the data files from <a href="data.html">here</a>'
    result += '</div>'
    result += '</div>'
    
    return result
    

def oneExample(name, dir, all, html):
    result = f'<a id="{dir}"></a>'
    result += '<div class="panel panel-default">'
    result += f'<div class="panel-heading">{name}</div>'
    result += '<div class="panel-body">'
    files = sorted(all[dir])
    htmlFiles = html[dir]
    result += '<table border="1">'
    for i, doc in files:
        main = i.split(".")[0]
        print(f'Example {i}')
        if main.endswith('allAlgos'):
            hfiles = [h for h in htmlFiles if h.startswith(main)]
        else:
            hfiles = [h for h in htmlFiles if h.split(".")[0] == main]
        print(f'HTML for {main}: {hfiles}')
        copyExample(i, dir, hfiles)
        fname = f'examples/{dir}/{i}'
        notebook_fname = f'examples/{dir}/{main}.ipynb'
        result += '<tr>'
        result += f'<td style="text-align:left; background-color:lightgrey"><a href="{fname}" target="_blank"><strong>{i}</strong></a></td>'
        result += '<td>'
        result += f'<a href="{urlgithub}examples/{dir}/{main}.ipynb" target="_blank"><img src="github.png" height="30"></a>&nbsp;'
        result += f'<a href="{urlnoto}examples/{dir}/{main}.ipynb" target="_blank"><img src="jupyter.png" height="30"></a>&nbsp;'
        result += f'<a href="{urlbinder}examples/{dir}/{main}.ipynb" target="_blank"><img src="binder.png" height="30"></a>'
        result += '</td>'
        result += '</tr>'
        if not hfiles:
            result += '<tr>'
            result += f'<td></td>'
            result += f'<td>{cleanDoc(doc)}</td>'
            result += '</tr>'
        for k, h in enumerate(hfiles):
            h_fname = f'examples/{dir}/{h}'
            result += '<tr>'
            result += f'<td><a href="{h_fname}" target="_blank">{h}</a></td>'
            if k == 0:
                result += f'<td rowspan="{len(hfiles)}">{cleanDoc(doc)}</td>'
            result += '</tr>'
    result += '</table>'
    result += '</div>'
    result += '</div>'
    return result

def jupyterExamples():
    exclude = ['.DS_Store','notebooks.zip']
    result = f'<a id="jupyter"></a>'
    result += '<div class="panel panel-default">'
    result += f'<div class="panel-heading">Modules illustrations</div>'
    result += '<div class="panel-body">'
    result += '<p>The following Jupyter notebooks contain illustrations of the use of the different modules available in the Biogeme package. They are designed for programmers who are interested to exploit the functionalities of Biogeme.</p>'
    result += '<p>Consult also the <a href="sphinx/index.html" target="_blank">documentation of the code</a>.</p>'
    result += '<table>'
    with os.scandir('../examples/notebooks') as root_dir:
        for file in root_dir:
            if file.is_file() and file.name not in exclude and file.name.endswith('ipynb'):
                print(f'Notebook: {file.name}')
                result += '<tr>'
                result += f'<td>{file.name}</td>'
                result += f'<td style="text-align:center"><a href="{urlgithub}examples/notebooks/{file.name}" target="_blank"><img src="github.png" height="30"></a></td>'
                result += f'<td style="text-align:center"><a href="{urlnoto}examples/notebooks/{file.name}" target="_blank"><img src="jupyter.png" height="30"></a></td>'
                result += f'<td style="text-align:center"><a href="{urlbinder}examples/notebooks/{file.name}" target="_blank"><img src="binder.png" height="30"></a></td>'
    result += '</table>'
    result += '<div class="panel-footer">'
    result += '<p>Register on noto.epfl.ch <a href="http://noto.epfl.ch">here</a></p>'
    result += '</div>'
    result += '</div>'
    return result
    
def generateExamples():
    dest = 'website/examples.html' 
    i = 0
    all = {}
    html = {}
    ignoreDirectory = ['workingNotToDistribute']
    ignore = ['.DS_Store']
    with os.scandir('../examples') as root_dir:
        for path in root_dir:
            if path.is_dir(follow_symlinks=False):
                i += 1
                with os.scandir(path.path) as local:
                    if not path.path in ignoreDirectory:
                        print(f'----- {path.path} -----')
                        f = []
                        h = []
                        for file in local:
                            if file.name.endswith('html'):
                                h += [file.name]
                            if file.is_file() and file.name.endswith('py'):
                                if not file.name in ignore:
                                    print(f'Parse {file.name}')
                                    # Parse the docstrings
                                    with open(file.path) as fd:
                                        sourceCode = fd.read()
                                    parsedCode = ast.parse(sourceCode)
                                    f += [(file.name, ast.get_docstring(parsedCode))]

                        def firstElem(x):
                            return x[0]
                        all[path.name] = f
                        html[path.name] = h

    allExamples = [('Swissmetro', 'swissmetro'),
                   ('Calculating indicators', 'indicators'),
                   ('Monte-Carlo integration', 'montecarlo'),
                   ('Choice models with latent variables', 'latent')]

    result = tableOfContents(allExamples)

    for i in allExamples:
        result += oneExample(i[0], i[1], all, html)

    result += jupyterExamples()
    
    replaceInFile(dest, 'THEEXAMPLES', result)
    
    
    
pages = {'index': 'Home',
         'start': 'Start',
         'help': 'Help',
         'install': 'Install',
         'data': 'Data',
         'videos': 'Videos',
         'documents': 'Documentation', 
         'examples': 'Examples',
         'courses': 'Courses',
         'software': 'Other softwares',
         'archives': 'Archives'}

generateMenu(pages) 
generateAllPages(pages)
