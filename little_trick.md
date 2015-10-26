# python，ipython 小技巧
这里收录了一些处理python，ipython notebook 等的一些小技巧。方便研究者操作
---

## ipython notebook


### code cell中显示行数

快捷键为 先同时按下 ctrl+M 再按L 即可显示
若想设置为默认行为，可以通过在你的 custom.js file (位置依赖于你的OS)让
IPython.Cell.options_default.cm_config.lineNumbers = true;

如果你找不到*custom.js*，你可以全局搜索一下，一般来说在profile_default 文件下

最后，若还是不行，你可以在**site-packages/IPython/html/static/custom/**下编辑custom.js 文件


### ipython notebook 安装程序包： ! pip install sympy

### 设置random seed numpy.random.seed(123)

<script type="text/javascript"
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  TeX: { equationNumbers: { autoNumber: "AMS" } }
});
</script>

\begin{equation}
   E = mc^2
\end{equation}

$$E=mac^2$$


### ipython notebook 更改默认路径

1. 打开命令行, 键入
ipython profile create

2. 键入 , 根据这个地址, 打开profile所在的文件夹
ipython locate

3. 打开这个文件: ipython_notebook_config.py

4.1. 在其中修改这一项(Python2), 注意去掉前面的#
c.NotebookApp.notebook_dir = u'/path/to/your/notebooks'
4.2 Python3
c.FileNotebookManager.notebook_dir = u'/path/to/your/notebooks'<pre name="code" class="python">c.NotebookManager.notebook_dir = u'/path/to/your/notebooks'

