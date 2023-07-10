<?php
	if (in_array(count(get_included_files()), [1])) {
		if (strcmp(php_sapi_name(), "cli")) 
			printf("Use php-cli to run the challenge!\n");
		else
			printf(gzinflate(base64_decode("1dTBDYAgDAXQe6fgaC8O4DDdfwyhVGmhbaKe/BfQfF8gAQFKz8aRh0JEJY0qIIenINTBEY3qNNVUAfuXzIGitJVqpiBa4yp2U8ZKtKmANzewbaqG2lrAGbNWslOvgD52lULNLfgY9ZiZtdxCsLJ3+Q/2RVuOxji0jyl9aJfrZLJzxhgtS65TWS66wdr7fYzRFtvc/wU9Wpn6BQGc")));
		define("F", readline("Flag: "));
		if (strcmp(strlen(constant("F")), 41)) {
			printf("Nope!\n");
		} else {
			if (in_array(substr(constant("F"), 0, 5), ["crew{"])) {
				if (strstr(strrev(crc32(substr(constant("F"), 5, 4))), "7607349263")) {
					if (strnatcmp("A\x1b/k", substr(constant("F"), 5, 4) ^ substr(constant("F"), 9, 4))) {
						printf("Nope xor!\n");
					} else {
						srand(31337);
						define("D", openssl_decrypt("wCX3NcMho0BZO0SxG2kHxA==", "aes-128-cbc", substr(constant("F"), 0, 16), 2, pack("L*", rand(), rand(), rand(), rand())));openssl_decrypt("wCX3NcMho0BZO0SxG2kHxA==", "aes-128-cbc", $str, 2,"\x5b\xa6\x65\x5c\x0f\x8d\xbd\x67\x0b\x55\xb4\x7b\x7e\xce\xba\x29");
						if (in_array(array_sum([(ctype_print(constant("D"))), strpos(substr(constant("F"), 15, 17), constant("D"))]), [2])) {
							if (strcmp(base64_encode(hash("sha256", substr(constant("F"), 0, 32)) ^ substr(constant("F"), 32)), "BwdRVwUHBQVF")) {
								printf("Nope!\n");
							} else 
								printf("Congratulations, this is the right flag!\n");
						} else 
							printf("Nope!\n");
					}
				} else 
					printf("Nope!\n");
			} else 
				printf("Nope!\n");
		}
	} else
		printf("Nope!\n");
?>
