<?php
	$arr = array('[', ']', '(', ')', ':', '?', '.', ',', '^');
	
	$len = sizeof($arr);
	for ( $i = 0 ; $i < $len ; $i++ )
	{
		for ( $j = 0 ; $j < $len ; $j++ )
		{
			$t = $arr[$i]^$arr[$j];
			if (ord($t) == 92 || ord($t) == 34)
				printf("\ts = s.replace(\"('%s'^'%s')\", \"'\%s'\")\n", $arr[$i], $arr[$j], $t);
			else if (ord($t) >= 32 && ord($t) <= 126)
				printf("\ts = s.replace(\"('%s'^'%s')\", \"'%s'\")\n", $arr[$i], $arr[$j], $t);

			for ( $k = 0 ; $k < $len ; $k++ )
			{
				$t = $arr[$i]^$arr[$j]^$arr[$k];
				if (ord($t) == 92 || ord($t) == 34)
					printf("\ts = s.replace(\"('%s'^'%s'^'%s')\", \"'\%s'\")\n", $arr[$i], $arr[$j], $arr[$k], $t);
				else if (ord($t) >= 32 && ord($t) <= 126)
					printf("\ts = s.replace(\"('%s'^'%s'^'%s')\", \"'%s'\")\n", $arr[$i], $arr[$j], $arr[$k], $t);

				for ( $l = 0 ; $l < $len ; $l++ )
				{
					$t = $arr[$i]^$arr[$j]^$arr[$k]^$arr[$l];
					if (ord($t) == 92 || ord($t) == 34)
						printf("\ts = s.replace(\"('%s'^'%s'^'%s'^'%s')\", \"'\%s'\")\n", $arr[$i], $arr[$j], $arr[$k], $arr[$l], $t);
					else if (ord($t) >= 32 && ord($t) <= 126)
						printf("\ts = s.replace(\"('%s'^'%s'^'%s'^'%s')\", \"'%s'\")\n", $arr[$i], $arr[$j], $arr[$k], $arr[$l], $t);
				}
			}
		}
	}
?>
