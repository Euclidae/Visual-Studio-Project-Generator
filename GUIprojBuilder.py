import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import random
import xml.etree.ElementTree as ET
import uuid

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VSProjectGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visual Studio Project Generator")
        self.geometry("500x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.project_name = ctk.CTkEntry(self.main_frame, placeholder_text="Project Name")
        self.project_name.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.vs_version = ctk.CTkOptionMenu(self.main_frame, values=["Visual Studio 2017", "Visual Studio 2019", "Visual Studio 2022"])
        self.vs_version.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.architecture = ctk.CTkOptionMenu(self.main_frame, values=["x86", "x64"])
        self.architecture.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.file_type = ctk.CTkOptionMenu(self.main_frame, values=[".cpp", ".cxx"])
        self.file_type.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.save_location = ctk.CTkButton(self.main_frame, text="Select Save Location", command=self.select_save_location)
        self.save_location.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.generate_button = ctk.CTkButton(self.main_frame, text="Generate Project", command=self.generate_project)
        self.generate_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.main_frame, text="")
        self.status_label.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.save_path = ""

    def select_save_location(self):
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.status_label.configure(text=f"Save location: {self.save_path}")

    def generate_project(self):
        project_name = self.project_name.get()
        vs_version = self.vs_version.get()
        architecture = self.architecture.get()
        file_type = self.file_type.get()

        if not all([project_name, vs_version, architecture, file_type, self.save_path]):
            self.status_label.configure(text="Please fill all fields and select a save location.")
            return

        # Create project structure
        project_path = os.path.join(self.save_path, project_name)
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, project_name), exist_ok=True)
        os.makedirs(os.path.join(project_path, architecture, "Debug"), exist_ok=True)

        # Generate solution file
        self.generate_sln_file(project_path, project_name, vs_version)

        # Generate project files
        self.generate_vcxproj_files(project_path, project_name, vs_version, architecture, file_type)

        # Generate main source file
        self.generate_main_file(project_path, project_name, file_type)

        self.status_label.configure(text="Project generated successfully!")

    def generate_sln_file(self, project_path, project_name, vs_version):
        vs_version_guid = {
            "Visual Studio 2017": "15.0.26730.12",
            "Visual Studio 2019": "16.0.29123.88",
            "Visual Studio 2022": "17.0.31903.59"
        }
        vs_version_year = vs_version.split()[-1]
        
        content = f"""
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version {vs_version_year[2:]}
VisualStudioVersion = {vs_version_guid[vs_version]}
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{project_name}", "{project_name}\\{project_name}.vcxproj", "{{{str(uuid.uuid4()).upper()}}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|x64 = Debug|x64
        Debug|x86 = Debug|x86
        Release|x64 = Release|x64
        Release|x86 = Release|x86
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {{{str(uuid.uuid4()).upper()}}}.Debug|x64.ActiveCfg = Debug|x64
        {{{str(uuid.uuid4()).upper()}}}.Debug|x64.Build.0 = Debug|x64
        {{{str(uuid.uuid4()).upper()}}}.Debug|x86.ActiveCfg = Debug|Win32
        {{{str(uuid.uuid4()).upper()}}}.Debug|x86.Build.0 = Debug|Win32
        {{{str(uuid.uuid4()).upper()}}}.Release|x64.ActiveCfg = Release|x64
        {{{str(uuid.uuid4()).upper()}}}.Release|x64.Build.0 = Release|x64
        {{{str(uuid.uuid4()).upper()}}}.Release|x86.ActiveCfg = Release|Win32
        {{{str(uuid.uuid4()).upper()}}}.Release|x86.Build.0 = Release|Win32
    EndGlobalSection
    GlobalSection(SolutionProperties) = preSolution
        HideSolutionNode = FALSE
    EndGlobalSection
    GlobalSection(ExtensibilityGlobals) = postSolution
        SolutionGuid = {{{str(uuid.uuid4()).upper()}}}
    EndGlobalSection
EndGlobal
"""
        with open(os.path.join(project_path, f"{project_name}.sln"), "w") as f:
            f.write(content.strip())

    def generate_vcxproj_files(self, project_path, project_name, vs_version, architecture, file_type):
        vs_toolset = {
            "Visual Studio 2017": "v141",
            "Visual Studio 2019": "v142",
            "Visual Studio 2022": "v143"
        }
        
        # Main .vcxproj file
        vcxproj_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Debug|x64">
      <Configuration>Debug</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|x64">
      <Configuration>Release</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <VCProjectVersion>16.0</VCProjectVersion>
    <Keyword>Win32Proj</Keyword>
    <ProjectGuid>{{{str(uuid.uuid4()).upper()}}}</ProjectGuid>
    <RootNamespace>{project_name}</RootNamespace>
    <WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>{vs_toolset[vs_version]}</PlatformToolset>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>{vs_toolset[vs_version]}</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>{vs_toolset[vs_version]}</PlatformToolset>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>{vs_toolset[vs_version]}</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>WIN32;_DEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>WIN32;NDEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>_DEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>NDEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemGroup>
    <ClCompile Include="main{file_type}" />
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>
"""
        with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj"), "w") as f:
            f.write(vcxproj_content)

        # .vcxproj.filters file
        filters_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <Filter Include="Source Files">
      <UniqueIdentifier>{{{str(uuid.uuid4()).upper()}}}</UniqueIdentifier>
      <Extensions>cpp;c;cc;cxx;c++;cppm;ixx;def;odl;idl;hpj;bat;asm;asmx</Extensions>
    </Filter>
    <Filter Include="Header Files">
      <UniqueIdentifier>{{{str(uuid.uuid4()).upper()}}}</UniqueIdentifier>
      <Extensions>h;hh;hpp;hxx;h++;hm;inl;inc;ipp;xsd</Extensions>
    </Filter>
    <Filter Include="Resource Files">
      <UniqueIdentifier>{{{str(uuid.uuid4()).upper()}}}</UniqueIdentifier>
      <Extensions>rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;resx;tiff;tif;png;wav;mfcribbon-ms</Extensions>
    </Filter>
  </ItemGroup>
  <ItemGroup>
    <ClCompile Include="main{file_type}">
      <Filter>Source Files</Filter>
    </ClCompile>
  </ItemGroup>
</Project>
"""
        with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj.filters"), "w") as f:
            f.write(filters_content)

        # .vcxproj.user file
        user_content = """<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="Current" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup />
</Project>
"""
        with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj.user"), "w") as f:
            f.write(user_content)

    def generate_main_file(self, project_path, project_name, file_type):
        positive_messages = [
            "Don't worry, it's going to be okay. You can do this!",
            "Believe in yourself. You've got this!",
            "Every expert was once a beginner. Keep going!",
            "You're making progress, even if you can't see it yet.",
            "Coding is a journey. Enjoy the process of learning!",
            "Mistakes are proof that you're trying. Keep it up!",
            "Your potential is limitless. Keep pushing forward!",
            "Success is the sum of small efforts repeated day in and day out.",
            "The only way to do great work is to love what you do.",
            "Your hard work will pay off. Stay focused and determined!"
        ]

        cpp_tips = [
            "Tip: Always initialize your variables to avoid unexpected behavior.",
            "Tip: Use const whenever possible to make your code more robust.",
            "Tip: Learn to use references (&) and pointers (*) effectively.",
            "Tip: Understand the difference between stack and heap memory allocation.",
            "Tip: Practice good memory management to avoid leaks.",
            "Tip: Use std::vector instead of C-style arrays when possible.",
            "Tip: Familiarize yourself with the Standard Template Library (STL).",
            "Tip: Use meaningful variable and function names for better readability.",
            "Tip: Comment your code, but remember that good code is self-documenting.",
            "Tip: Learn to use debuggers like the one in Visual Studio to find and fix issues."
        ]

        content = f"""#include <iostream>
#include <string>
#include <vector>
#include <random>

int main() {{
    std::vector<std::string> messages = {{
        {', '.join(f'"{msg}"' for msg in positive_messages)}
    }};

    std::vector<std::string> tips = {{
        {', '.join(f'"{tip}"' for tip in cpp_tips)}
    }};

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> msg_dist(0, messages.size() - 1);
    std::uniform_int_distribution<> tip_dist(0, tips.size() - 1);

    std::cout << messages[msg_dist(gen)] << std::endl;
    std::cout << std::endl;
    std::cout << tips[tip_dist(gen)] << std::endl;

    return 0;
}}
"""
        with open(os.path.join(project_path, project_name, f"main{file_type}"), "w") as f:
            f.write(content)

if __name__ == "__main__":
    app = VSProjectGenerator()
    app.mainloop()
