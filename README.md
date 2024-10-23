# Visual Studio Project Generator 🚀

A powerful and user-friendly tool for generating Visual Studio C++ projects with both GUI and CLI interfaces. Say goodbye to compulsory Visual Studio projects by lecturers and project directors.
# GUI Version
![image](https://github.com/user-attachments/assets/f1505286-94a7-481a-b342-8325dd835d67)

## ✨ Features

- 🖥️ Intuitive GUI interface built with CustomTkinter
- 🎯 Support for multiple Visual Studio versions (2017, 2019, 2022)
- 💻 x86 and x64 architecture support (GUI)
- 📁 Automatic project structure generation
- 🛠️ Configurable file extensions (.cpp, .cxx)
- 💡 Built-in C++ tips and motivational messages in generated code
- 🎨 Dark mode interface

## 🚀 Quick Start

### Prerequisites

```bash
pip install customtkinter
```

### GUI Version

1. Run the GUI version:
```bash
python vs_project_generator_gui.py
```

2. Fill in the project details:
   - Project Name
   - Visual Studio Version
   - Architecture (x86/x64)
   - File Extension
   - Save Location

3. Click "Generate Project" and you're done! 🎉

### CLI Version

Generate a project using command-line arguments:

```bash
python vs_project_generator_cli.py --name MyProject --vs-version "Visual Studio 2022" --arch x64 --ext .cpp --path C:\Projects
```

## 📂 Generated Project Structure

```
ProjectName/
├── ProjectName/
│   ├── main.cpp
│   ├── ProjectName.vcxproj
│   ├── ProjectName.vcxproj.filters
│   └── ProjectName.vcxproj.user
├── x64/
│   └── Debug/
└── ProjectName.sln
```

## 🛠️ Project Configuration

The generator supports:

- **Visual Studio Versions**
  - Visual Studio 2017
  - Visual Studio 2019
  - Visual Studio 2022

- **Architectures**
  - x86 (32-bit)
  - x64 (64-bit)

- **File Extensions**
  - .cpp
  - .cxx

## 💡 Generated Code Features

- Pre-configured project settings
- Standard C++ includes
- Random motivational messages
- Helpful C++ programming tips
- Modern C++ practices
- Ready-to-build configuration

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
MIT License
## 🙏 Acknowledgments

- CustomTkinter for the modern GUI elements
- Visual Studio for the project templates
- Python community for inspiration and support

## 📞 Contact

For questions, suggestions, or issues, please:
1. Open an issue in this repository
2. Submit a pull request
3. Start a discussion in the Discussions tab

---

Made with ❤️ by [Euclidae]

*Remember to star ⭐ this repository if you find it helpful!*
