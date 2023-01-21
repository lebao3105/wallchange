project(
    'me.lebao3105.wallchange',
    version: '0.1.0',
    meson_version: '>=0.59.0'
)

# Imports
app_id = meson.project_name()
py = import('python')

py_inst = py.find_installation('python3')

if not py_inst.found()
    error('Python installation not found!')
endif

if not py_inst.language_version().version_compare('>= 3.8')
    error('Please use Python 3.8 or higher')
endif

# Dirs
prefix = get_option('prefix')
localedir = join_paths(prefix, get_option('localedir'))
moduledir = join_paths(prefix, get_option('datadir'), app_id)

subdir('icons')
subdir('po')
subdir('wallchange')