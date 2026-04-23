---
title: "Hex dump functions"
type: "post"
created_at: "2009-06-07T20:00:31"
original_url: "http://www.alexonlinux.com/hex-dump-functions"
categories: ["Code library"]
tags: []
---

This post starts a new category of posts called*Code library*. In this category I will post useful code snippets. I hope you’ll find them as useful as I do.

I use two functions below quiet often. Both functions do hexadecimal dump of given buffer. First function is in C. Second function is in Python. Enjoy.

```text
void hex_dump(char *data, int size, char *caption)
{
	int i; // index in data...
	int j; // index in line...
	char temp[8];
	char buffer[128];
	char *ascii;

	memset(buffer, 0, 128);

	printf("---------> %s <--------- (%d bytes from %p)\n", caption, size, data);

	// Printing the ruler...
	printf("        +0          +4          +8          +c            0   4   8   c   \n");

	// Hex portion of the line is 8 (the padding) + 3 * 16 = 52 chars long
	// We add another four bytes padding and place the ASCII version...
	ascii = buffer + 58;
	memset(buffer, ' ', 58 + 16);
	buffer[58 + 16] = '\n';
	buffer[58 + 17] = '\0';
	buffer[0] = '+';
	buffer[1] = '0';
	buffer[2] = '0';
	buffer[3] = '0';
	buffer[4] = '0';
	for (i = 0, j = 0; i < size; i++, j++)
	{
		if (j == 16)
		{
			printf("%s", buffer);
			memset(buffer, ' ', 58 + 16);

			sprintf(temp, "+%04x", i);
			memcpy(buffer, temp, 5);

			j = 0;
		}

		sprintf(temp, "%02x", 0xff & data[i]);
		memcpy(buffer + 8 + (j * 3), temp, 2);
		if ((data[i] > 31) && (data[i] < 127))
			ascii[j] = data[i];
		else
			ascii[j] = '.';
	}

	if (j != 0)
		printf("%s", buffer);
}
```

And the Python version. Python version is a bit smarter – it allows you to specify output stream.

```text
def DumpBuffer(self, buf, length, caption="", dest=sys.stdout):
	def GetPrintableChar(str):
		if str.isalpha():
			return str
		else:
			return '.'

	dest.write('---------> %s <--------- (%d bytes)\n' % (caption, length))
	dest.write('       +0          +4          +8          +c           0   4   8   c\n')
	i = 0
	while i < length:
		if length - i > 16:
			l = 16
		else:
			l = length - i

		dest.write('+%04x  ' % i)
		s = ' '.join(["%02x" % ord(c) for c in buf[i:i + l]])
		dest.write(s)
		sp = 49 - len(s)
		dest.write(' ' * sp)
		s = ''.join(["%c" % GetPrintableChar(c) for c in buf[i:i + l]])
		dest.write(s)
		dest.write('\n')

		i = i + 16
```
