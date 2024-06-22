from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'waitress',
    'pytest',
    'cryptography',
    'pyramid_retry',
    'pyramid_jwt',
    'webtest',
    'bcrypt',
    'alembic',
    'pymysql',  # Add the pymysql dependency
]

setup(
    name='fylinde',
    version='0.0',
    description='fylinde',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = user_service:main',
        ],
        'console_scripts': [
            'initialize_user_service_db = user_service.scripts.initialize_db:main',
        ],
    },
)
