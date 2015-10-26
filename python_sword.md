# 这里主要包括了一些处理python、ipython等问题的技巧

## 文本处理
### 读取csv，excel 文件 
很多时候，我们会遇到读取文件乱码的情况。如果我们希望用utf-8等统一编码格式来进行文件读写的话，可以如下处理：

``` python 
import sys
import codecs
import csv

reload(sys)  
sys.setdefaultencoding('utf8')


with codecs.open(path+csvfile[0]+csvfile[1], 'rb','utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)# 解决超出field限制的问题



from xlsxwriter.workbook import Workbook
workbook = Workbook(new_path+csvfile[0] + '.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(row, col, col.decode('utf-8-sig')) # 写入编码
workbook.close()	

```


### pandas group data 
有时候我们想对数据进行分组划分，用groupby 命令会很方便

```python
# groupby test 
df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar','foo', 'bar', 'foo', 'foo'],'B' : ['one', 'one', 'two', 'three',
                          'two', 'two', 'one', 'three'],
                    'C' : np.random.randn(8), 'D' : np.random.randn(8)})
    
group_df=df.groupby(["A","B"])
group_df.get_group(('bar', 'one'))
```
### python pandas 数据合并：
这里数据合并，重新进行index

```python
# merge data 
ss=s.append(s2,ignore_index=True)
m_pd=pd.concat([s,s2],ignore_index=True)

```

### 判断pandas dataframe 中某一列是否有NaN：

```python

data_sm[pd.isnull(data_sm[u'地址'])]
data_sm[u'地址'].isnull

```

### 选取空字符串 
选取空字符串，进行文本操作，比如计算多少个空的

```python
ttt[ttt['lat']!=""]
len(ttt[ttt['lat']!=""])
```

### 替换字符

d=sm_industry[sm_industry[u'面积'].str.contains(u"亩")][u'面积'].str.replace(u"亩","").astype(float)*666.67

### 筛选多个字符串
sm_industry[~sm_industry[u'面积'].str.contains(r"亩|平方米")][u'面积']

### 取一个dataframe element string 前几个字符
fm_industry['电子监管号'].str[0:6]

### 正则表达式-提取有前后标志的字符

page_num = int(re.findall(r"(?<=_0_0_0_0_0___________)\d+(?=\.html)",str(next_page_link))[0])


## pandas 数据分析操作

### 删除多个列操作

```python
# 选择列，仅仅是指数
df.columns[[20]]

# 删除列
data_fm.drop(data_fm.columns[[1,2,20]], axis=1, inplace=True) 
```

### 删除重复列

```python
data_fm.T.drop_duplicates().T
````

### 从另一个列中索引值
有时候我们会遇到这个问题，在大数据列中有各种编码，我们需要对编码映射出相应的地址、区划。我们有另一个字典来存储这种映射，我们可以做的是：

```python
# code 为字典映射 
# df为大数据
tat=df['电子监管号'].str[0:6].astype(int).apply(lambda x:code[code[u'地址码']==x][u'对应地址'].values)
tat=list(tat)
tat=pd.DataFrame(tat,index=df.index)

#------------
#另一种方式
dic_code=dict(list(code.groupby(u'地址码')))
dic_code[320402][u'对应地址']

def mapp(x):
    if dic_code.has_key(x): 
        return dic_code[x][u'对应地址'].values[0] 
    else : 
        return ""
tatt=df['电子监管号'].str[0:6].astype(int).map(mapp)

tatt=pd.DataFrame(tatt)
tatt.columns=['add']  # 更改列的名称
tatt
```

### 读取hdf5 的数据

%timeit df.to_csv('test.csv',mode='w')
1 loops, best of 3: 12.7 s per loop

%timeit df.to_hdf('test.h5','df',mode='w')
1 loops, best of 3: 825 ms per loop

%timeit pd.read_csv('test.csv',index_col=0)
1 loops, best of 3: 2.35 s per loop

%timeit pd.read_hdf('test.h5','df')
10 loops, best of 3: 38 ms per loop

### 重新命名一个列

```python
df.rename(columns={'index':'mindex'}, inplace=True)

old_names = ['$a', '$b', '$c', '$d', '$e'] 
new_names = ['a', 'b', 'c', 'd', 'e']
df.rename(columns=dict(zip(old_names, new_names)), inplace=True)
```
