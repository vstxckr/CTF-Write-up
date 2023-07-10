<?php
	$fix = "crew{php_1s_4";
	$table = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_{}()!@#$%^&*;<>\\/.,|\'\"~`=-+?:";
	$len = strlen($table);
	for ($i = 0 ; $i < $len ; $i++)
	{
		$str = $fix;
		$str.=$table[$i];
		$temp1 = $str;
		for ($j = 0 ; $j < $len ; $j++)
		{
			$str = $temp1;
			$str.=$table[$j];
			$temp2 = $str;
			for ($k = 0 ; $k < $len ; $k++)
			{
				$str = $temp2;
				$str.=$table[$k];
				$y= openssl_decrypt("wCX3NcMho0BZO0SxG2kHxA==", "aes-128-cbc", $str, 2,"\x5b\xa6\x65\x5c\x0f\x8d\xbd\x67\x0b\x55\xb4\x7b\x7e\xce\xba\x29");
				$str .= $y;
				if (in_array(array_sum([ctype_print($y), strpos(substr($str, 15, 17), $y)]), [2])) {
					printf("%s", $str.(base64_decode("BwdRVwUHBQVF")^ hash("sha256", $str)));	
				} 	
			}
		}
	}
?>
