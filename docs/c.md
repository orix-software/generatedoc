# C

Parser needs to read _xxx.s file (_ means that it will use C doc parser. .proc name must be also with '_')

Sample :

```bash
.proc _recv
    ;;@proto int recv(unsigned char s, void *buf, unsigned char len, unsigned char flags);
    ;;@brief
    ;;@file socket.h
    ;;@details 
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

## @Brief 

Short message to explain the usage

## @file

header it refers to

## details 

Longer comment to explain details

## @details

Since 2026.3, more description if necessary

## @bug

Describe a bug

## inputPARAM_

input param the string after "_" is the name of the variable

;;@inputPARAM_flags

The type can be added : 

;;@inputPARAM_flags_int

or 
;;@inputPARAM_flags_*Window

## explain

Explain how it works

## @code

## Returns

What does it returns

All lines beginning with ;;@` will be considered as a code syntax (when the block start with ;;@``` code and ends with ;;@```':

## @failure (Since 2026.1)


## @note (Since 2026.1)

