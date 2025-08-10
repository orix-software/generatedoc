# Assembly

A file must be named : xxxx.s without "_" at the beginning. '_' means that it's for C.

Parser detect ';;@' lines

```bash
.proc bind
    ;;@brief Bind sockets
    ;;@inputX Socket id
    ;;@inputA Low byte of port
    ;;@inputY High byte of port

    ;;@modifyMEM_XX Modify

    ;;@modifyA XX
    ;;@modifyX XX
    ;;@modifyY XX

    ;;@returnsA XX
    ;;@returnsX XX
    ;;@returnsY XX
    ;;@note bla
    ;;@failure bla
    ;;@bug bla
    ;;@```asm
    ;;@` lda bms_ptr
    ;;@` ldx bms_ptr + 1
    ;;@` jsr bms_free
    ;;@` rts
    ;;@```
    ;;@explain bla
.endproc
```

## @Brief

Defines description of the routine

    ;;@brief My beautiful function

## @inputX

Define X input register

Example :

```bash
;;@inputX Socket id
```

## @inputY

Define Y input register

Example :

```bash
;;@inputY Socket id
```

## @note

## @inputA

## @returnsX

## @returnsA

## @returnsY

## @modifyMEM_

@modifyMEM_XX : XX is the name of the memory (label)

;;@modifyMEM_TR0

It will displays that TR0 (memory offset will be modified)
