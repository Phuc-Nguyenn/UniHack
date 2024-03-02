# Monkey Run

## Development

- `extern` contains subdirectories that hold dependencies such as the `godot-cpp` library necessary for using GDExtension.
- `project` is the actual Godot project.
- `src` contains all C++ source code. It uses Godot's GDExtension API so that the C++ code can be used to interface with Godot.

For building, use the provided `build.py` file. By default, it will build in debug mode but you can specify `release` to build in release mode.
