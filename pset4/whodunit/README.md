# Questions

## What's `stdint.h`?

Header file that use aliases to define C/C++ primitive data types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

They help define size of integers that are used as a standard in different formats.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM

## What's the difference between `bfSize` and `biSize`?

First one is for size of file, latter for size of file headerin bytes.

## What does it mean if `biHeight` is negative?

The bitmap is a top-downbiBitCount DIB and its origin is the upper left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If a file cannot be located, it will return NULL.

## Why is the third argument to `fread` always `1` in our code?

The third argument is for how many elements in an array.
Since there is only one element, it should be 1.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

1

## What does `fseek` do?

Fast forward through the file.

## What is `SEEK_CUR`?

It moves a pointer position to a given location.

## Whodunit?

Professor Plum with the candlestick in the library.
