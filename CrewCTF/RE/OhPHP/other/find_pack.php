<?php
	srand(31337);
	$s = pack("L*", rand(), rand(), rand(), rand());
	$len = strlen($s);
	for ( $i = 0 ; $i < $len ; $i++ )
	{
		printf("\\x%02x", ord($s[$i]));
	}
?>
