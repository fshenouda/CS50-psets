// Recover a deleted JPEG photo.

#include <stdio.h>
#include <stdlib.h>

// macro for JPEG header condition
#define JPEGFOUND memblock[0] == 0xff && memblock[1] == 0xd8 && memblock[2] == 0xff && (memblock[3] & 0xf0) == 0xe0

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover file\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // allocate 512 bytes into buffer
    unsigned char memblock[512];
    int filecount = 1, JPEGfound = 0;
    char filename[8];

    // read through the file until there's no more data
    while(fread(memblock, 512, 1, inptr) == 1)
    {
        // check if start of block contain JPEG header
        if (JPEGFOUND)
        {
            sprintf(filename, "%03d.jpg", filecount);
            FILE *outptr = fopen(filename, "w");

            while (fwrite(memblock, 512, 1, outptr) == 1)
            {
                fread(memblock, 512, 1, inptr);
                    // check if next image is found and stop if so
                    if (JPEGFOUND)
                    {
                        filecount++;
                        break;
                    }
            }
            fclose(outptr);
        }
    }
    // close infile
    fclose(inptr);

    // success
    return 0;
}