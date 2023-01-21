conf = configuration_data()
conf.set('LOCALEDIR', localedir)
conf.set('ISMESONTOUCHED', true)

configure_file(
    input: '__init__.py',
    output: '__init__.py',
    configuration: conf,
    install: true,
    install_dir: join_paths(moduledir, 'wallchange')
)

run_conf = configuration_data()
run_conf.set('PYTHON', py_inst.full_path())
run_conf.set('pkgdatadir', moduledir)

if target_machine.system() == 'windows'
    out = '@0@.pyw'.format(app_id)
else
    out = '@0@'.format(app_id)
endif

configure_file(
    input: '@0@.in'.format(app_id),
    output: out,
    configuration: run_conf,
    install: true,
    install_dir: get_option('bindir')
)

sources = [
    '__main__.py',
    'callbacks.py',
    'mainwindow.py',
    'setwallpaper.py'
]

install_data(
    sources,
    install_dir: join_paths(moduledir, 'wallchange')
)