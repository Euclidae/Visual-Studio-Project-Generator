import os
import uuid

visual_studio_versions = ('2017', "2019", '2022')
architectures = ('x86','x64')
formats = ('.cpp', '.cxx')

def load_config_from_file(filename="template.txt"):
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines:
            return None
        if len(lines) != 4:
            print(f"template.txt must have exactly 4 lines: project name, VS version, architecture, file extension")
            return None
        
        config = {
            'project_name': lines[0],
            'vs_version': lines[1],
            'architecture': lines[2], 
            'file_extension': lines[3]
        }
        
        return config
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

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

def generate_sln_file(project_path, project_name, vs_version):
    vs_version_guid = {
        "2017": "15.0.26730.12",
        "2019": "16.0.29123.88", 
        "2022": "17.0.31903.59"
    }
    vs_version_year = vs_version
    project_guid = str(uuid.uuid4()).upper()
    
    content = f"""Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version {vs_version_year[2:]}
VisualStudioVersion = {vs_version_guid[vs_version]}
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}}") = "{project_name}", "{project_name}\\{project_name}.vcxproj", "{{{project_guid}}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|x64 = Debug|x64
        Debug|x86 = Debug|x86
        Release|x64 = Release|x64
        Release|x86 = Release|x86
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        {{{project_guid}}}.Debug|x64.ActiveCfg = Debug|x64
        {{{project_guid}}}.Debug|x64.Build.0 = Debug|x64
        {{{project_guid}}}.Debug|x86.ActiveCfg = Debug|Win32
        {{{project_guid}}}.Debug|x86.Build.0 = Debug|Win32
        {{{project_guid}}}.Release|x64.ActiveCfg = Release|x64
        {{{project_guid}}}.Release|x64.Build.0 = Release|x64
        {{{project_guid}}}.Release|x86.ActiveCfg = Release|Win32
        {{{project_guid}}}.Release|x86.Build.0 = Release|Win32
    EndGlobalSection
    GlobalSection(SolutionProperties) = preSolution
        HideSolutionNode = FALSE
    EndGlobalSection
    GlobalSection(ExtensibilityGlobals) = postSolution
        SolutionGuid = {{{str(uuid.uuid4()).upper()}}}
    EndGlobalSection
EndGlobal"""

    
    with open(os.path.join(project_path, f"{project_name}.sln"), "w") as f:
        f.write(content)
    return project_guid

def generate_vcxproj_files(project_path, project_name, vs_version, architecture, file_type, project_guid):
    vs_toolset = {
        "2017": "v141",
        "2019": "v142", 
        "2022": "v143"
    }
 
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
    <ProjectGuid>{{{project_guid}}}</ProjectGuid>
    <RootNamespace>{project_name}</RootNamespace>
    <WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.Default.props" />
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
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
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
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>"""
    
    with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj"), "w") as f:
        f.write(vcxproj_content)

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
</Project>"""
    
    with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj.filters"), "w") as f:
        f.write(filters_content)

    user_content = """<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="Current" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup />
</Project>"""
    
    with open(os.path.join(project_path, project_name, f"{project_name}.vcxproj.user"), "w") as f:
        f.write(user_content)

def generate_main_file(project_path, project_name, file_type):
    content = """#include <iostream>
#include <string>

int main() {
    std::cout << "Hello from Visual Studio Project Generator!" << std::endl;
    std::cout << "Project created successfully." << std::endl;
    return 0;
}"""
    
    with open(os.path.join(project_path, project_name, f"main{file_type}"), "w") as f:
        f.write(content)

def main():
    print("Visual Studio Project Generator - CLI Version")
    print("=" * 45)

    config = load_config_from_file()
    
    if config:
        print("Using settings from template.txt")
        project_name = config['project_name']
        vs_version = config['vs_version']
        architecture = config['architecture']
        file_type = config['file_extension']
        
        print(f"Project: {project_name}")
        print(f"VS Version: {vs_version}")
        print(f"Architecture: {architecture}")
        print(f"File Extension: {file_type}")
    else:
        print("template.txt is empty - please edit it with your settings")
        print("Format (4 lines exactly):")
        print("  Line 1: Project name")
        print("  Line 2: VS version (2017/2019/2022)")
        print("  Line 3: Architecture (x86/x64)")
        print("  Line 4: File extension (.cpp/.cxx)")
        return
        
    
    if vs_version not in visual_studio_versions:
        print(f"Invalid VS version '{vs_version}', using 2017") # changed from 22 to 17 because uni students usually have bad devices
        vs_version = '2017'
    if architecture not in architectures:
        print(f"Invalid architecture '{architecture}', using x64")
        architecture = 'x64'
    if file_type not in formats:
        print(f"Invalid file extension '{file_type}', using .cpp")
        file_type = '.cpp'

    project_path = os.path.join(".", project_name)
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, project_name), exist_ok=True)
    os.makedirs(os.path.join(project_path, architecture, "Debug"), exist_ok=True)

    project_guid = generate_sln_file(project_path, project_name, vs_version)
    generate_vcxproj_files(project_path, project_name, vs_version, architecture, file_type, project_guid)
    generate_main_file(project_path, project_name, file_type)

    print(f"Project '{project_name}' created successfully!")

if __name__ == "__main__":
    main()
