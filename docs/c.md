# C

Parser needs to read _xxx.s file (_ means that it will use C doc parser. .proc name must be also with '_')

Sample :

```bash
.proc _recv
    ;;@proto int recv(unsigned char s, void *buf, unsigned char len, unsigned char flags);
    ;;@brief
    ;;@bug
    ;;@inputPARAM_flags
    ;;@explain
    ;;@returns
    ;;@```code
    ;;@`
    ;;@```':
.endproc
```

## @proto

Define the proto of the function

## @code



## @failure (Since 2026.1)

## @bug

## @note (Since 2026.1)

