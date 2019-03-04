# engi

`engi` is a dumb source-install manager.

## Usage

Type `python3 engi.py install` and follow the on-screen instructions to add a
program. In the commands given, you can use the variables `{stow_dir}` and
`{package_name}` for the stow directory (usually `/usr/local/stow/`) and the
program name.

Type `python3 engi.py upgrade` to actually install & update every program.

Usage example:
```shell
$ python3 engi.py install
Enter the name of the program.
> neovim
Enter the URL of the program.
> https://github.com/neovim/neovim.git
Enter the commands you want to run to install the program, terminated by an empty line.
> sudo apt install -y autoconf automake cmake g++ gettext libtool libtool-bin ninja-build pkg-config unzip
> rm -rf build
> make CMAKE_BUILD_TYPE=RelWithDebInfo CMAKE_EXTRA_FLAGS=\"-DCMAKE_INSTALL_PREFIX={stow_dir}/{package_name}\" -j8
> sudo make install
> sudo stow -d {stow_dir} {package_name}
$ python3 engi.py upgrade
Checking neovim
Downloading neovim
# zip
Downloaded neovim
Installing neovim
# zip
Installed neovim
$ nvim --version
NVIM v0.4.0-333-gbcbb96e31
# zip
```
