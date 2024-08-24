import os
import random
import customtkinter as ctk
from tkinter import filedialog, messagebox

def create_folder_structure(base_folder, structure):
    for item in structure:
        path = os.path.join(base_folder, item)
        os.makedirs(path, exist_ok=True)

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        file.write(content)

def create_empty_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').close()

def create_project():
    project_name = project_name_entry.get()
    vs_version = vs_version_entry.get()
    
    if not project_name or not vs_version:
        messagebox.showerror("Error", "Please enter both project name and Visual Studio version.")
        return

    base_folder = filedialog.askdirectory(title="Select directory to create project")
    if not base_folder:
        return

    base_folder = os.path.join(base_folder, project_name)
    
    folder_structure = [
        project_name,
        f"{project_name}/x64/Debug",
        "x64/Debug",
    ]

    create_folder_structure(base_folder, folder_structure)

    vcxproj_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
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
    <ProjectGuid>{{00000000-0000-0000-0000-000000000000}}</ProjectGuid>
    <RootNamespace>{project_name}</RootNamespace>
    <WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v143</PlatformToolset>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v143</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.props" />
  <ItemGroup>
    <ClCompile Include="Source.cpp" />
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.targets" />
</Project>
"""
    create_file(os.path.join(base_folder, project_name, f"{project_name}.vcxproj"), vcxproj_content)

    filters_content = f"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <Filter Include="Source Files">
      <UniqueIdentifier>{{4FC737F1-C7A5-4376-A066-2A32D752A2FF}}</UniqueIdentifier>
      <Extensions>cpp;c;cc;cxx;c++;cppm;ixx;def;odl;idl;hpj;bat;asm;asmx</Extensions>
    </Filter>
    <Filter Include="Header Files">
      <UniqueIdentifier>{{93995380-89BD-4b04-88EB-625FBE52EBFB}}</UniqueIdentifier>
      <Extensions>h;hh;hpp;hxx;h++;hm;inl;inc;ipp;xsd</Extensions>
    </Filter>
    <Filter Include="Resource Files">
      <UniqueIdentifier>{{67DA6AB6-F800-4c08-8B7A-83BB121AAD01}}</UniqueIdentifier>
      <Extensions>rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;resx;tiff;tif;png;wav;mfcribbon-ms</Extensions>
    </Filter>
  </ItemGroup>
  <ItemGroup>
    <ClCompile Include="Source.cpp">
      <Filter>Source Files</Filter>
    </ClCompile>
  </ItemGroup>
</Project>
"""
    create_file(os.path.join(base_folder, project_name, f"{project_name}.vcxproj.filters"), filters_content)

    sln_content = f"""
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version {vs_version}
VisualStudioVersion = {vs_version}.0.0.0
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{project_name}", "{project_name}\\{project_name}.vcxproj", "{{00000000-0000-0000-0000-000000000000}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|x64 = Debug|x64
        Release|x64 = Release|x64
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {{00000000-0000-0000-0000-000000000000}}.Debug|x64.ActiveCfg = Debug|x64
        {{00000000-0000-0000-0000-000000000000}}.Debug|x64.Build.0 = Debug|x64
        {{00000000-0000-0000-0000-000000000000}}.Release|x64.ActiveCfg = Release|x64
        {{00000000-0000-0000-0000-000000000000}}.Release|x64.Build.0 = Release|x64
    EndGlobalSection
    GlobalSection(SolutionProperties) = preSolution
        HideSolutionNode = FALSE
    EndGlobalSection
    GlobalSection(ExtensibilityGlobals) = postSolution
        SolutionGuid = {{00000000-0000-0000-0000-000000000000}}
    EndGlobalSection
EndGlobal
"""
    create_file(os.path.join(base_folder, f"{project_name}.sln"), sln_content)

    source_content = """#include <iostream>

int main() {
    std::cout << "Hi mom!" << std::endl;
    return 0;
}
"""
    create_file(os.path.join(base_folder, project_name, "Source.cpp"), source_content)

    debug_folder = os.path.join(base_folder, project_name, "x64", "Debug")
    create_empty_file(os.path.join(debug_folder, f"{project_name}.exe.recipe"))
    create_empty_file(os.path.join(debug_folder, f"{project_name}.ilk"))
    create_empty_file(os.path.join(debug_folder, f"{project_name}.log"))
    create_empty_file(os.path.join(debug_folder, "Source.obj"))
    create_empty_file(os.path.join(debug_folder, "vc143.idb"))
    create_empty_file(os.path.join(debug_folder, "vc143.pdb"))

    tlog_folder = os.path.join(debug_folder, f"{project_name[:8]}.{random.randint(10000000, 99999999)}.tlog")
    os.makedirs(tlog_folder, exist_ok=True)
    tlog_files = [
        "CL.command.1.tlog", "CL.read.1.tlog", "CL.write.1.tlog",
        "link.command.1.tlog", "link.read.1.tlog", "link.write.1.tlog",
        f"{project_name}.lastbuildstate"
    ]
    for tlog_file in tlog_files:
        create_empty_file(os.path.join(tlog_folder, tlog_file))

    messagebox.showinfo("Success", f"Project '{project_name}' created successfully with basic Visual Studio structure.")

# Initialize customtkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.title("Visual Studio Project Creator")
root.geometry("300x150")

ctk.CTkLabel(root, text="Project Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
project_name_entry = ctk.CTkEntry(root)
project_name_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(root, text="VS Version:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
vs_version_entry = ctk.CTkEntry(root)
vs_version_entry.grid(row=1, column=1, padx=5, pady=5)

create_button = ctk.CTkButton(root, text="Create Project", command=create_project)
create_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
