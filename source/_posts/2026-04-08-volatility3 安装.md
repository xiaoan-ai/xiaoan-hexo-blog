---
title: volatility3 安装
date: 2026-04-08T12:00:00+08:00
categories:
  - 安全工具
tags:
  - 工具
---

# volatility3 安装

**volatility3 需要 Python 3.6.0 或更高版本。**

使用 pip 进行包安装。

```
pip install volatility3
```

如果安装失败，进入 https://github.com/volatilityfoundation/volatility3/releases 选择`volatility3-2.0.0-py3-none-any.whl`进行下载

![img](images/github%20release.png)

通过以下指令进行自动化安装

```
pip3 wheel volatility3-2.0.0-py3-none-any.whl
```

若安装失败可直接下载源码后直接使用，但需要手动调用脚本 `vol.py`

```
python3 vol.py --help
```

> 可以通过以下指令达到与 `.whl` 安装同样的效果
>
> ```
> python3 setup.py build
> python3 setup.py install
> ```

如果需要使用 volatility3 完整功能，请保存文件 https://github.com/volatilityfoundation/volatility3/blob/develop/requirements.txt

然后运行以下指令安装 volatility3 所需依赖

```
pip3 install -r requirements.txt
```

# volatility3 使用

## 使用

通过 `-h` 指令获取帮助

```
vol.exe -h
```

![vol3help](/images/notes/取证分析-volatilitty3安装使用/images/vol3help.png)vol3help

同样地，可以对插件使用 `-h` 指令获取插件帮助

![layerwritehelp](/images/notes/取证分析-volatilitty3安装使用/images/layerwritehelp.png)layerwritehelp

## 插件

使用对应 linux / mac / windows 插件之前，请先下载对应的符号表（最好下载所有的符号包）：

- https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip
- https://downloads.volatilityfoundation.org/volatility3/symbols/mac.zip
- https://downloads.volatilityfoundation.org/volatility3/symbols/linux.zip

并将其解压在 `./volatility/symbols/` 目录下

![symbols](/images/notes/取证分析-volatilitty3安装使用/images/symbols.png)symbols

> 以下，部分插件可能出现不存在或者更名的情况，我并不会及时更新，请以官方帮助为准

| 插件名                          | 用法                                                  |
| ------------------------------- | ----------------------------------------------------- |
| `layerwriter`                   | 列出内存镜像 platform 信息，分割 layers               |
| `linux.bash`                    | 从内存中恢复 bash 命令历史记录                        |
| `linux.check_afinfo`            | 验证网络协议的操作功能指针                            |
| `linux.check_syscall`           | 检查系统调用表中的挂钩                                |
| `linux.elfs`                    | 列出所有进程的所有内存映射ELF文件                     |
| `linux.lsmod`                   | 列出加载的内核模块                                    |
| `linux.lsof`                    | 列出所有进程的所有内存映射                            |
| `linux.malfind`                 | 列出可能包含注入代码的进程内存范围                    |
| `linux.proc`                    | 列出所有进程的所有内存映射                            |
| `linux.pslist`                  | 列出 linux 内存映像中存在的进程                       |
| `linux.pstree`                  | 列出进程树                                            |
| `mac.bash`                      | 从内存中恢复 bash 命令历史记录                        |
| `mac.check_syscall`             | 检查系统调用表中的挂钩                                |
| `mac.check_sysctl`              | 检查 sysctl 处理程序的挂钩                            |
| `mac.check_trap_table`          | 检查 trap 表中的挂钩                                  |
| `mac.ifconfig`                  | 列出网卡信息                                          |
| `mac.lsmod`                     | 列出加载的内核模块                                    |
| `mac.lsof`                      | 列出所有进程的所有内存映射                            |
| `mac.malfind`                   | 列出可能包含注入代码的进程内存范围                    |
| `mac.netstat`                   | 列出所有进程的所有网络连接                            |
| `mac.psaux`                     | 恢复程序命令行参数                                    |
| `mac.pslist`                    | 列出 mac 内存映像中存在的进程                         |
| `mac.pstree`                    | 列出进程树                                            |
| `mac.tasks`                     | 列出 mac 内存映像中存在的进程                         |
| `windows.info`                  | 显示正在分析的内存样本的 OS 和内核详细信息            |
| `windows.callbacks`             | 列出内核回调和通知例程                                |
| `windows.cmdline`               | 列出进程命令行参数                                    |
| `windows.dlldump`               | 将进程内存范围 DLL 转储                               |
| `windows.dlllist`               | 列出 Windows 内存映像中已加载的 dll 模块              |
| `windows.driverirp`             | 在 Windows 内存映像中列出驱动程序的 IRP               |
| `windows.driverscan`            | 扫描 Windows 内存映像中存在的驱动程序                 |
| `windows.filescan`              | 扫描 Windows 内存映像中存在的文件对象                 |
| `windows.handles`               | 列出进程打开的句柄                                    |
| `windows.malfind`               | 列出可能包含注入代码的进程内存范围                    |
| `windows.moddump`               | 转储内核模块                                          |
| `windows.modscan`               | 扫描 Windows 内存映像中存在的模块                     |
| `windows.mutantscan`            | 扫描 Windows 内存映像中存在的互斥锁                   |
| `windows.pslist`                | 列出 Windows 内存映像中存在的进程，转储处理可执行映像 |
| `windows.psscan`                | 扫描 Windows 内存映像中存在的进程                     |
| `windows.pstree`                | 列出进程树                                            |
| `windows.registry.certificates` | 列出注册表中存储的证书                                |
| `windows.registry.hivelist`     | 列出内存映像中存在的注册表配置单元                    |
| `windows.registry.hivescan`     | 扫描 Windows 内存映像中存在的注册表配置单元           |
| `windows.registry.printkey`     | 在配置单元或特定键值下列出注册表项                    |
| `windows.registry.userassist`   | 打印用户助手注册表项和信息                            |
| `windows.ssdt`                  | 列出系统调用表                                        |
| `windows.strings`               | 读取字符串命令的输出，并指示每个字符串属于哪个进程    |
| `windows.svcscan`               | 扫描 Windows 服务                                     |
| `windows.symlinkscan`           | 扫描 Windows 内存映像中存在的链接                     |

## 操作

### 查看映像信息

```
vol.exe -f xxx.raw windows.info
```

### 查看映像进程

```
vol.exe -f xxx.raw windows.pslist
vol.exe -f xxx.raw windows.psscan
vol.exe -f xxx.raw windows.pstree
```

**查看指定 pid 的进程**

```
vol.exe -f xxx.raw windows.pslist --pid 1234
```

### 进程转储

```
vol.exe -o ./outputdir/ -f xxx.raw windows.pslist --pid 1234 --dump
```

### 内存转储

```
vol.exe -o ./outputdir/ -f xxx.raw windows.memmap --pid 1234 --dump
```

### 查看句柄

```
vol.exe -f xxx.raw windows.handles
vol.exe -f xxx.raw windows.handles --pid 1234
```

### 查看 DLL

```
vol.exe -f xxx.raw windows.dlllist
vol.exe -f xxx.raw windows.dlllist --pid 1234
```

### DLL 转储

```
vol.exe -o ./outputdir/ -f xxx.raw windows.dlllist --pid 1234 --dump
```

### 查看命令行

```
vol.exe -f xxx.raw windows.cmdline
vol.exe -f xxx.raw windows.cmdline --pid 1234
```

### 查看网络端口

```
vol.exe -f xxx.raw windows.netscan
```

**查看完整的结果，但可能包含垃圾信息和虚假信息 (谨慎使用)**

```
vol.exe -f xxx.raw windows.netscan --include-corrupt
```

### 查看注册表信息

```
vol.exe -f xxx.raw windows.registry.hivescan
vol.exe -f xxx.raw windows.registry.hivelist
```

**查看指定过滤器 (文件夹) 下的注册表信息**

```
vol.exe -f xxx.raw windows.registry.hivelist --filter FILTER
```

### 注册表信息转储

```
vol.exe -o ./outputdir/ -f xxx.raw windows.hivelist --filter FILTER --dump
```

### 查看注册表键值对

```
vol.exe -f xxx.raw windows.registry.printkey
```

**查看指定过滤器 (文件夹) 下的注册表信息，但需要 `hivelist` 提供的 `offset`**

```
vol.exe -f xxx.raw windows.registry.printkey --offset OFFSET
```

**查看指定键下的注册表值**

```
vol.exe -f xxx.raw windows.registry.printkey --key KEY
```

**打印所有键的信息**

```
vol.exe -f xxx.raw windows.registry.printkey --recurse
```

### 查看文件信息

```
vol.exe -f xxx.raw windows.filescan
```

> 建议通过 powershell 的 Select-String 或者 bash 的 grep 进行搜索，如：
>
> ```
> vol.exe -f xxx.raw windows.filescan | grep "flag"
> vol.exe -f xxx.raw windows.filescan | Select-String "flag"
> ```

### 文件转储

**需要 `pslist` 提供的 `pid`**

```
vol.exe -o ./outputdir/ -f xxx.raw windows.dumpfiles --pid 1234
```

**(推荐) 需要 `filescan` 提供的 `offset` (一般来说为 `physaddr`)**

```
vol.exe -o ./outputdir/ -f xxx.raw windows.dumpfiles --virtaddr 0xee1122
vol.exe -o ./outputdir/ -f xxx.raw windows.dumpfiles --physaddr 0xee1122
```

### 查找恶意注入代码

```
vol.exe -f xxx.raw windows.malfind
vol.exe -f xxx.raw windows.malfind --pid 1234
```

**恶意注入代码转储**

```
vol.exe -o ./outputdir/ -f xxx.raw windows.malfind --pid 1234 --dump
```

# 库使用方法

有时候我们想要使用 Python 调用 volatility3 来实现一些自动化取证的功能，故在这里记录一下个人经验。

在 volatility3 的文档和代码中，都十分推荐使用 cli 模块的书写方式来编写调用代码。

可以定位到 `.venv\Lib\site-packages\volatility3\cli\__init__.py`，观察 `run(self)` 代码

![clirun](/images/notes/取证分析-volatilitty3安装使用/images/clirun.png)clirun

```python
from volatility3.cli import (
    contexts,
    framework,
    volatility3,
    automagic,
    stacker,
    MuteProgress,
    CommandLine,
)
from volatility3.framework.plugins import construct_plugin
from dataclasses import dataclass
from pathlib import Path
import asyncio

@dataclass
class Project:
    """
    项目类
    """
    fileid: str
    filepath: Path
    projectpath: Path

# 初始化vol模块
failures = framework.import_files(volatility3.plugins, True)
if failures:
    print(f"Failed to import {len(failures)} plugins:")
    for failure in failures:
        print(f" - {failure}")
plugin_list = framework.list_plugins()
    
async def run_plugin(project: Project, plugin_name: str):
    """
    运行插件
    :param plugin_name: 插件名
    :param inpath: 输入文件路径
    :param outpath: 输出文件路径
    :param outfilename: 输出文件名
    """
    base_config_path = "plugins"
    ctx = contexts.Context()
    automagics = automagic.available(ctx)
    cmd = CommandLine()
    # 这里设置是为了方便之后调用file_handler_class_factory()
    cmd.output_dir = Path(project.projectpath).absolute()
    # 获取对应name的插件类，实际上也可以自行导入
    plugin = plugin_list[plugin_name]
    # 镜像文件的路径
    ctx.config["automagic.LayerStacker.single_location"] = project.filepath.absolute().as_uri()
    ctx.config["automagic.LayerStacker.stackers"] = stacker.choose_os_stackers(plugin)
    constructed = construct_plugin(ctx,
                                   automagics,
                                   plugin,
                                   base_config_path,
                                   MuteProgress(),
                                   cmd.file_handler_class_factory())
    return constructed.run()

grid = asyncio.run(run_plugin(project, "windows.info.Info"))
```

需要注意的是，`plguin_list` 的键都是完整的类名，而 `construct_plugin` 的 `plugin` 参数必须是一个插件类（实现了接口 `interfaces.plugins.PluginInterface`），也可以自行导入

```
from volatility3.plugins.windows import pslist

plugin = pslist.PsList
```

> 这里没有高亮是因为 `pslist` 实际上在 `volatility3.framework.plugins` 中，`volatility3.plugins` 模块会动态导入（因为有些插件需要一些必要的模块支持）。

如果说需要输出到文件中，还可以使用 `volatility3.cli.text_renderer` 模块中的一些渲染器渲染 grid，由于该种使用方法书写较少，这边不在赘述。

# 插件编写

## 基本

volatility 的强大不仅在于其解析能力，还在于其可拓展性，即可以随心所欲的编写插件来扩展它的能力。

而其中，volatility3 不仅重构了逻辑，同时使得插件编写更为容易和简单。

对于一个插件，首先需要继承 `interfaces.plugins.PluginInterface`，接口要求实现一个 `run(self)` 成员函数，返回值必须是一个 `interfaces.renderers.TreeGrid`（这里只是一个接口，实际上返回值可以是实现了该接口的任何对象，下面为了方便一律使用标准实现 `renderers.TreeGrid`）；

其次还需给 `_required_framework_version` 赋值，这是用于检查插件所需 volatility3 版本的。由于目前 volatility3 的版本号是 2.x.x，故至少需要修改为 `(2, 0, 0)`。

基本代码框架如下

```
from volatility3.framework import interfaces, renderers

class Test(interfaces.plugins.PluginInterface):
    _required_framework_version = (2, 0, 0)

    def run(self):
        return renderers.TreeGrid([("Content", str)], [(0, ["test"])])
```

可以创建一个文件夹，将插件脚本放入，在这里我将文件夹命名为 `plugins`，而为了更好的代码规范（官方有提供插件代码规范）文件名是 `test.py`。

那么可以尝试运行插件，其中 `-p` 是指定额外插件文件夹

```
vol.exe -p .\plugins\ test
```

那么应该可以观察到回显

![测试插件输出](images/%E6%B5%8B%E8%AF%95%E6%8F%92%E4%BB%B6%E8%BE%93%E5%87%BA.png)测试插件输出

那么可以结合 `TreeGrid` 的注释将其理解为一个表格，第一个参数是一个列表，用来定义列名（Content）和列元素类型（str）；第二个参数是一个表格行列表，是一个元组，第一个整数（0）代表某一行的树形 Level，第二个是行元素的值（列表 `["test"]`）。

但是我们写插件，不是只是为了获取一个表格的输出，是想对内存镜像文件进行处理，那么这里需要编写第二个函数 `get_requirements(cls)`，这是一个 `classmethod`，修改后的框架如下

```python
from volatility3.framework import interfaces, renderers
from volatility3.framework.configuration import requirements

class Test(interfaces.plugins.PluginInterface):
    _required_framework_version = (2, 0, 0)

    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(
                name="kernel",
                description="Windows kernel",
                architectures=["Intel32", "Intel64"],
            ),]

    def run(self):
        return renderers.TreeGrid([("Content", str)], [(0, ["test"])])
```

这样可以定义插件需要的输入，比如说在这里，需要一个 `Module`（这里不具体描述 `Module` 在 volatility3 中是什么，仅需知道如果想要输入一个 Windows 内存镜像文件，必须这样书写，对于其他系统可以参考官方插件的编写）。

可以发现，返回值是一个列表，所以我们还可以定义多个要求，比如说需要额外的参数

```python
@classmethod
def get_requirements(cls):
    return [
        requirements.ModuleRequirement(
            name="kernel",
            description="Windows kernel",
            architectures=["Intel32", "Intel64"],
        ),
        requirements.BooleanRequirement(
            name="qsdzyyds",
            description="夸奖qsdz",
            default=True,
            optional=True
        )]
```

那么我们可以尝试输入一个镜像文件，且输入该插件参数。（也可以尝试不输入，volatility3 将会报错并终止插件运行）

![带有requirement的插件回显](images/%E5%B8%A6%E6%9C%89requirement%E7%9A%84%E6%8F%92%E4%BB%B6%E5%9B%9E%E6%98%BE.png)带有requirement的插件回显

想要获取参数值，可以从 `self.config` 中获取，例如可以尝试在 `run(self)` 中加入代码

```
flag = self.config["qsdzyyds"]
print(f"尝试查看输入的参数值：{flag = }")
```

![获取插件参数](images/%E8%8E%B7%E5%8F%96%E6%8F%92%E4%BB%B6%E5%8F%82%E6%95%B0.png)获取插件参数

也可以自行尝试打印整个 `config` 字典。

我们尝试获取 `Module`，这相当于 volatility3 分析后的内存镜像文件：

```
kernel = self.context.modules[self.config["kernel"]]
```

> ```
> kernel = <volatility3.framework.contexts.Module object at 0x0000017C7C2B2C90>
> ```

这里引出 volatility3 中一个十分重要的对象 `context`。

在 volatility3 的插件中，维护一个上下文（context），可以通过 context 访问 volatility3 帮助分析的一些内容，在我们的插件中也可以向上下文中修改或添加值来进行传递。

很多功能并不需要自己书写，就像 Python 调用其他库那样，volatility3 也可以很轻松的调用插件，比如说 `pslist.PsList` 插件。

```python
from volatility3.framework import interfaces, renderers
from volatility3.framework.configuration import requirements
from volatility3.framework.symbols.windows.extensions import EPROCESS
from volatility3.plugins.windows import pslist
from typing import Generator

class Test(interfaces.plugins.PluginInterface):
    ...
    def run(self):
        kernel = self.context.modules[self.config["kernel"]]
        procs: Generator[EPROCESS] = pslist.PsList.list_processes(
            self.context,
            kernel.layer_name,
            kernel.symbol_table_name
        )
        return renderers.TreeGrid([("Content", str)], [(0, ["test"])])
```

这里省略了一部分代码，只展示如何调用 pslist 插件的一些功能，比较常用的是 `list_processes`，它将返回一个 EPROCESS 结构体的迭代器，方便遍历内存中的所有进程。

对于其他的插件，用法是类似的，需要传递的参数通过函数注释就可以了解。

可以通过官方插件 `pslist` 的 `_generator` 函数学习一些用法。

![pslist的_generator函数](images/pslist%E7%9A%84_generator%E5%87%BD%E6%95%B0.png)

pslist的_generator函数

`objects` 中的类型可以称为 vol 对象类型，最基本的都遵循 `ObjectInterface` 接口，vol 对象是一种代理类，可以通过它直接获取内部表示的成员，例如说这里的 EPROCESS 的 UniqueProcessId 成员。

同时一个 vol 对象也可以转换为其他对象，可以使用 `cast` 方法进行转换，对于不同的类型所需的额外参数不相同。

至此一个 volatility3 插件的编写流程已经结束。

## vol 对象

每一个 vol 对象都会实现接口 `ObjectInterface`，接口满足存在一个成员 `vol` 会返回一个字典，其中包含一些必要的信息，可以编写代码进行查看

```
def run(self):
    kernel = self.context.modules[self.config["kernel"]]
    procs: Generator[EPROCESS] = pslist.PsList.list_processes(
        self.context,
        kernel.layer_name,
        kernel.symbol_table_name
    )
    procs = list(procs)
	proc: EPROCESS = procs[5]
    peb: objects.StructType = proc.get_peb()
    print(dict(peb.vol))
    return renderers.TreeGrid([("Content", str)], [(0, ["qsdzyyds"])])
```

可以观察到回显为

```
{'size': 896, 'members': {...}, 'layer_name': 'layer_name_Process428', 'offset': 8796092887040, 'member_name': None, 'parent': None, 'native_layer_name': 'layer_name_Process428', 'type_name': 'symbol_table_name1!_PEB'}
```

这是一个字典，其中 `size` 代表的是该对象的大小；`members` 是该对象的成员（如果是结构体的话）；`offset` 是内存中的地址（即指针）；如果存在的话，`member_name` 和 `parent` 显示的是该对象作为某个 `parent` 结构体对象的成员名 `member_name`；`type_name` 是该对象类型在符号表中的名字。

符号表类型将由 `kernel.symbol_table_name` 和具体结构体名（在这里是 `_PEB`）通过 `constants.BANG` 拼接而成。

对于任意一个 vol 对象，都可以使用 `cast` 进行转换，转换后不一定可以成功，可以通过 `has_member`，`has_valid_member`，`has_valid_members` 函数进行验证是否转换成功。

比较特别的有 `Pointer` vol 对象，对于指针对象我们可以进行取值 `dereference()`，通常由于符号表中定义为 `VOID*` 指针类型，故经常与 `cast` 搭配使用，例如

```
# 从PEB中获取进程的默认堆(PHEAP)
heap: objects.StructType = peb.ProcessHeap.dereference().cast('_HEAP')
```

## kernel

在这里主要针对的是 `kernel = self.context.modules[self.config["kernel"]]`。

kernel 常用的函数有 `get_enumeration`，`get_type` 和 `get_symbol`，可以通过他们获取符号表中的具体类型。

## Notepad 插件实战

### 分析

在 volatility2 中，十分热门的一个插件是 `notepad` 插件，但这个插件在 volatility3 中是不存在的，我们可以通过模仿 volatility2 编写一个 volatility3 版本的 `notepad` 插件。

vol2-notepad 插件源码地址：https://github.com/volatilityfoundation/volatility/blob/master/volatility/plugins/notepad.py

首先对插件源码进行分析，基本逻辑如下

![vol2 notepad的generator函数](images/vol2%20notepad%E7%9A%84generator%E5%87%BD%E6%95%B0.png)

vol2 notepad的generator函数

简单而言可以概括为

1. 获取 EPROCESS 列表，遍历每一个进程 task
2. 获取 task 的 PEB，然后从 PEB 中获取堆（HEAP）
3. 遍历堆的段（HEAP_SEGMENT）
4. 遍历段的堆块头（HEAP_ENTRY），随后获取堆块的内容
5. 返回堆块的内容

### 遍历 EPROCESS 列表

在这里利用 pslist 的方法获取

```
class Notepad(interfaces.plugins.PluginInterface):
    ...
	def notepad_processes(self):
        """
        获取notepad进程，返回生成器
        """
        kernel = self.context.modules[self.config["kernel"]]
        procs: Generator[EPROCESS] = pslist.PsList.list_processes(
                                                self.context,
                                                kernel.layer_name,
                                                kernel.symbol_table_name
                                                )
        for proc in procs:
            name: str = proc.ImageFileName.cast("string",
                                                max_length=proc.ImageFileName.vol.count,
                                                errors='replace')
            if name.lower() == "notepad.exe":
                yield proc
```

### 获取堆

```
class Notepad(interfaces.plugins.PluginInterface):
    ...
    def heap(self, proc: EPROCESS):
        # 获取进程PEB
        peb: objects.StructType = proc.get_peb()
        # 从PEB中获取进程的默认堆(PHEAP)
        heap: objects.StructType = peb.ProcessHeap.dereference().cast('_HEAP')
        return heap
```

### 获取段

适当参考插件源码

![vol2 notepad的segments函数](images/vol2%20notepad%E7%9A%84segments%E5%87%BD%E6%95%B0.png)vol2 notepad的segments函数

```
class Notepad(interfaces.plugins.PluginInterface):
    ...
    def segments(self, heap: objects.StructType):
        kernel = self.context.modules[self.config["kernel"]]
        HEAP_SEGMENT = kernel.get_type("_HEAP_SEGMENT")
        return [seg.dereference().cast(HEAP_SEGMENT.vol.type_name) for seg in heap.Segments if seg != 0]
```

### 获取堆块头

适当参考插件源码

![vol2 notepad的entries函数](images/vol2%20notepad%E7%9A%84entries%E5%87%BD%E6%95%B0.png)vol2 notepad的entries函数

这里需要仿造 vol2 那样定义堆块头的一个 Flags 枚举值

```
from enum import IntFlag

class ENTRY_FLAGS(IntFlag):
    BUSY    = 0x01
    EXTRA   = 0x02
    FILL    = 0x04
    VIRTUAL = 0x08
    LAST    = 0x10
    FLAG1   = 0x20
    FLAG2   = 0x40
    FLAG3   = 0x80
    FLAGS   = FLAG1 | FLAG2 | FLAG3
```

那么可以编写代码

```python
class Notepad(interfaces.plugins.PluginInterface):
    ...
    def entries(self, segment: objects.StructType):
        kernel = self.context.modules[self.config["kernel"]]
        HEAP_ENTRY = kernel.get_type("_HEAP_ENTRY")
        offset: objects.Pointer = segment.FirstEntry
        end: objects.Pointer = segment.LastValidEntry
        while offset < end:
            entry: objects.StructType = self.context.object(HEAP_ENTRY, segment.vol.layer_name, offset)
            if not entry.has_valid_members(['Size', 'Flags']):
                break
            size = entry.Size
            flags = entry.Flags
            yield entry
            # 到最后一个堆块了
            if flags & ENTRY_FLAGS.LAST:
                break
            # 偏移到下一个堆块
            offset += size * HEAP_ENTRY.size
```

### 获取堆块内容

适当参考插件源码

![vol2 notepad的extra函数](images/vol2%20notepad%E7%9A%84extra%E5%87%BD%E6%95%B0.png)vol2 notepad的extra函数

```
def extra(self, entry: objects.StructType):
    kernel = self.context.modules[self.config["kernel"]]
    HEAP_ENTRY = kernel.get_type("_HEAP_ENTRY")
    trans_layer = self.context.layers[entry.vol.layer_name]
    size = entry.Size
    flags = entry.Flags
    if flags & ENTRY_FLAGS.EXTRA:
        data = trans_layer.read(entry.vol.offset + HEAP_ENTRY.size, (size - 1) * HEAP_ENTRY.size)
        return data.decode("ANSI", errors="ignore")
    return ''
```

### 输出

最后，我们编写完整 `_generator` 函数即可。

完整代码如下：

```python
from volatility3.framework import interfaces, renderers, objects
from volatility3.framework.configuration import requirements
from volatility3.framework.symbols.windows.extensions import EPROCESS
from volatility3.plugins.windows import pslist
from typing import Generator
from enum import IntFlag

class ENTRY_FLAGS(IntFlag):
    BUSY    = 0x01
    EXTRA   = 0x02
    FILL    = 0x04
    VIRTUAL = 0x08
    LAST    = 0x10
    FLAG1   = 0x20
    FLAG2   = 0x40
    FLAG3   = 0x80
    FLAGS   = FLAG1 | FLAG2 | FLAG3

class Notepad(interfaces.plugins.PluginInterface):
    _required_framework_version = (2, 0, 0)

    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(
                name="kernel",
                description="Windows kernel",
                architectures=["Intel32", "Intel64"],
            ),
            requirements.BooleanRequirement(
                name="qsdzyyds",
                description="夸奖qsdz",
                default=True,
                optional=True
            )]
    def notepad_processes(self):
        """
        获取notepad进程，返回生成器
        """
        kernel = self.context.modules[self.config["kernel"]]
        procs: Generator[EPROCESS] = pslist.PsList.list_processes(
                                                self.context,
                                                kernel.layer_name,
                                                kernel.symbol_table_name
                                                )
        for proc in procs:
            name: str = proc.ImageFileName.cast("string",
                                                max_length=proc.ImageFileName.vol.count,
                                                errors='replace')
            if name.lower() == "notepad.exe":
                yield proc
    
    def heap(self, proc: EPROCESS):
        # 获取进程PEB
        peb: objects.StructType = proc.get_peb()
        # 从PEB中获取进程的默认堆(PHEAP)
        heap: objects.StructType = peb.ProcessHeap.dereference().cast('_HEAP')
        return heap

    def segments(self, heap: objects.StructType):
        kernel = self.context.modules[self.config["kernel"]]
        HEAP_SEGMENT = kernel.get_type("_HEAP_SEGMENT")
        return [seg.dereference().cast(HEAP_SEGMENT.vol.type_name) for seg in heap.Segments if seg != 0]

    def entries(self, segment: objects.StructType):
        kernel = self.context.modules[self.config["kernel"]]
        HEAP_ENTRY = kernel.get_type("_HEAP_ENTRY")
        offset: objects.Pointer = segment.FirstEntry
        end: objects.Pointer = segment.LastValidEntry
        while offset < end:
            entry: objects.StructType = self.context.object(HEAP_ENTRY, segment.vol.layer_name, offset)
            if not entry.has_valid_members(['Size', 'Flags']):
                break
            size = entry.Size
            flags = entry.Flags
            yield entry
            # 到最后一个堆块了
            if flags & ENTRY_FLAGS.LAST:
                break
            # 偏移到下一个堆块
            offset += size * HEAP_ENTRY.size

    def extra(self, entry: objects.StructType):
        kernel = self.context.modules[self.config["kernel"]]
        HEAP_ENTRY = kernel.get_type("_HEAP_ENTRY")
        trans_layer = self.context.layers[entry.vol.layer_name]
        size = entry.Size
        flags = entry.Flags
        if flags & ENTRY_FLAGS.EXTRA:
            data = trans_layer.read(entry.vol.offset + HEAP_ENTRY.size, (size - 1) * HEAP_ENTRY.size)
            return data.decode("ANSI", errors="ignore")
        return ''

    def _generator(self):
        for proc in self.notepad_processes():
            heap = self.heap(proc)
            for seg in self.segments(heap):
                for entry in self.entries(seg):
                    data = self.extra(entry)
                    if data:
                        yield (0, [data])

    def run(self):
        return renderers.TreeGrid([("Content", str)], self._generator())
```

尝试运行得到回显如下

![vol3 notepad插件回显](images/vol3%20notepad%E6%8F%92%E4%BB%B6%E5%9B%9E%E6%98%BE.png)

vol3 notepad插件回显

> 更完善的版本已经放在 GitHub 上，实际上拥有 FLAGS 标签的才有可能是 USER 堆块。

# 错误解决方案

## 编码错误

有时由于内存转储文件存在错误，导致内容失效，此时可能导致文本渲染错误

![img](/images/notes/取证分析-volatilitty3安装使用/images/gbk.png)

打开异常最先出现的位置 `./volatility3/cli/text_renderer.py` 定位 `line 173`

![img](/images/notes/取证分析-volatilitty3安装使用/images/visitor.png)

修改代码为

![img](/images/notes/取证分析-volatilitty3安装使用/images/after.png)

此法为暴力破解，可以解决程序因抛出异常后中断执行问题（处理方式为不处理异常继续运行程序）。

除此之外更加推荐使用指令 `-r json` 切换渲染模式为 json 格式，随后输出到文件中。