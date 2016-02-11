from setuptools import setup

setup(
    name='django-smooth-perms',
    version=__import__('smooth-perms').VERSION,
    description='Smooth Permissions system for Django.',
    author='Jean-Baptiste Munieres (mek4nr)',
    author_email='info@djangosuit.com',
    url='http://djangosuit.com',
    packages=['smooth_perms'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Django :: 1.8',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: Permissions Features',
    ]
)
