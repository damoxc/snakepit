try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='wiki',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'wiki': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,
    entry_points="""
    [snakepit.modules]
    wiki = wiki.wiki:WikiModule
    """,
)
