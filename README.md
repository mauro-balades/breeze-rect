# breeze-rect
A breeze plugin for the Rect programming language

## instalation

```
pip3 install breeze-build breeze-rect

cd your_rect_project
touch breeze.toml
```

then, in your configuration file, type the following contents:

```toml
[project]
name = "hello"
lang = "rect"

[config.rect-lang]
type = "exec"
compiler = "g++"
sources = ["./src/**/*.cc"]
include = "./include"
```

and finally,

```
breeze build
```
