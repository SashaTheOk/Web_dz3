from setuptools import setup, find_namespace_packages

setup(
    name="FriendlyHandbook",
    version="0.1",
    description="«FriendlyHandbook» - це корисна програма з інтерфейсом командного рядка, яка містить контактну книгу, нотатки, калькулятор та може аналізувати папки.",
    url="https://github.com/filinmbg/FriendlyHandbook",
    author="JustPython",
    author_email="filinmbg@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["helloworld = FriendlyHandbook.main:main"]},
)
